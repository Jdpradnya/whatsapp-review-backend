from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from .database import engine, get_db, Base
from .models import Review
from .schemas import ReviewResponse, ReviewCreate
from .whatsapp_handler import handle_whatsapp_message, reset_session

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WhatsApp Review Collector API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "WhatsApp Review Collector API"}

@app.get("/api/reviews", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    """Get all reviews"""
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    return reviews

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """Twilio WhatsApp webhook endpoint"""
    form_data = await request.form()
    from_number = form_data.get("From")
    message_body = form_data.get("Body", "").strip()
    
    # Handle conversation
    result = handle_whatsapp_message(from_number, message_body)
    
    # Save review if conversation complete
    if result.get("save_review"):
        review_data = result["data"]
        new_review = Review(**review_data)
        db.add(new_review)
        db.commit()
        reset_session(from_number)
    
    # Return TwiML response
    return result["response"]

@app.get("/health")
def health_check():
    return {"status": "healthy"}
