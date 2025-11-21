import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Inquiry, Order, Meeting, ChatMessage

app = FastAPI(title="Construction & Stone Co API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Construction & Stone Co Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Submit inquiry (contact form)
@app.post("/api/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        doc_id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Place an order from chatbot
@app.post("/api/orders")
def create_order(order: Order):
    try:
        doc_id = create_document("order", order)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Book a meeting from chatbot
@app.post("/api/meetings")
def create_meeting(meeting: Meeting):
    try:
        doc_id = create_document("meeting", meeting)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple rule-based chatbot endpoint (no external dependencies)
@app.post("/api/chat")
def chat_with_bot(payload: ChatMessage):
    user_msg = payload.message.lower()
    response = "I'm here to help with construction services, marble, and granite. Ask me about services, products, pricing, or book a meeting."

    if any(k in user_msg for k in ["hello", "hi", "hey"]):
        response = "Hello! How can I assist with your project today?"
    if "service" in user_msg or "construction" in user_msg:
        response = "We offer turnkey construction, renovation, civil works, and project management. Would you like a quick quote?"
    if "marble" in user_msg:
        response = "Our marble range includes Carrara, Calacatta, Emperador, and Nero Marquina. Tell me the variety and quantity you need."
    if "granite" in user_msg:
        response = "We stock Absolute Black, Baltic Brown, Blue Pearl, and Kashmir White granite. What thickness and finish do you prefer?"
    if "price" in user_msg or "quote" in user_msg:
        response = "Please share the product/service, dimensions or scope, and location. I can prepare a quote and email it to you."
    if "order" in user_msg:
        response = "To place an order, tell me product type (marble/granite/service), product name, and quantity. I'll create the order."
    if "meeting" in user_msg or "book" in user_msg:
        response = "I can schedule a site visit or consultation. Share your name, email, preferred date/time, and location."
    if "email" in user_msg or "contact" in user_msg:
        response = "You can reach us at info@buildstone.co or call +1 (555) 010-2020."

    return {"reply": response}

# Optional: list recent items for admin/testing
@app.get("/api/recent")
def get_recent():
    try:
        data = {
            "inquiries": get_documents("inquiry", {}, 5),
            "orders": get_documents("order", {}, 5),
            "meetings": get_documents("meeting", {}, 5),
        }
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
