"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Branding demo schemas kept for reference
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# App-specific schemas
class Inquiry(BaseModel):
    name: str = Field(..., description="Customer name")
    email: EmailStr = Field(..., description="Customer email")
    phone: Optional[str] = Field(None, description="Phone number")
    subject: str = Field(..., description="Subject of inquiry")
    message: str = Field(..., description="Inquiry message")
    preferred_time: Optional[str] = Field(None, description="Preferred contact time")

class Order(BaseModel):
    customer_name: str
    email: EmailStr
    phone: Optional[str] = None
    product_type: str = Field(..., description="marble | granite | construction-service")
    product_name: Optional[str] = Field(None, description="Specific marble/granite variety or service name")
    quantity: Optional[str] = Field(None, description="Requested quantity or scope")
    notes: Optional[str] = None

class Meeting(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    date: str = Field(..., description="Requested meeting date (string)")
    time: str = Field(..., description="Requested meeting time (string)")
    topic: Optional[str] = Field(None, description="Meeting topic or project name")
    location: Optional[str] = Field(None, description="On-site / office / virtual platform")

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[str]] = Field(default_factory=list)
    # Basic structure; we keep it simple for the rule-based bot

class Timestamped(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
