from typing import Dict
from twilio.twiml.messaging_response import MessagingResponse

# In-memory session storage (use Redis in production)
user_sessions: Dict[str, dict] = {}

def handle_whatsapp_message(from_number: str, message_body: str) -> dict:
    """Handle WhatsApp conversation flow"""
    
    # Initialize session if new user
    if from_number not in user_sessions:
        user_sessions[from_number] = {"step": 0}
    
    session = user_sessions[from_number]
    response = MessagingResponse()
    msg = response.message()
    
    # Step 0: Ask for product name
    if session["step"] == 0:
        session["step"] = 1
        msg.body("Which product is this review for?")
    
    # Step 1: Receive product name, ask for user name
    elif session["step"] == 1:
        session["product_name"] = message_body
        session["step"] = 2
        msg.body("What's your name?")
    
    # Step 2: Receive user name, ask for review
    elif session["step"] == 2:
        session["user_name"] = message_body
        session["step"] = 3
        msg.body(f"Please send your review for {session['product_name']}.")
    
    # Step 3: Receive review, save and confirm
    elif session["step"] == 3:
        session["product_review"] = message_body
        session["step"] = 4
        msg.body(f"Thanks {session['user_name']} -- your review for {session['product_name']} has been recorded.")
        
        # Return session data to save in database
        return {
            "save_review": True,
            "data": {
                "contact_number": from_number,
                "user_name": session["user_name"],
                "product_name": session["product_name"],
                "product_review": session["product_review"]
            },
            "response": str(response)
        }
    
    return {"save_review": False, "response": str(response)}

def reset_session(from_number: str):
    """Reset user session after saving review"""
    if from_number in user_sessions:
        del user_sessions[from_number]
