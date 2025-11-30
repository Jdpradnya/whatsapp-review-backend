# WhatsApp Product Review Collector - Backend

FastAPI backend with PostgreSQL for collecting product reviews via WhatsApp.

## 🚀 Features

- WhatsApp conversation flow via Twilio
- PostgreSQL database for review storage
- RESTful API for frontend consumption
- Automatic conversation state management

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Twilio account with WhatsApp sandbox

## 🛠️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/Jdpradnya/whatsapp-review-backend.git
cd whatsapp-review-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/whatsapp_reviews
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 5. Setup PostgreSQL Database
```sql
CREATE DATABASE whatsapp_reviews;
```

The tables will be created automatically when you run the app.

### 6. Run the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 7. Configure Twilio Webhook
1. Go to Twilio Console → WhatsApp Sandbox
2. Set webhook URL to: `https://your-domain.com/webhook/whatsapp`
3. Use ngrok for local testing: `ngrok http 8000`

## 📡 API Endpoints

### GET /api/reviews
Returns all reviews in JSON format.

**Response:**
```json
[
  {
    "id": 1,
    "contact_number": "+1415XXXXXXX",
    "user_name": "Aditi",
    "product_name": "iPhone 15",
    "product_review": "Amazing battery life",
    "created_at": "2025-11-17T12:34:56Z"
  }
]
```

### POST /webhook/whatsapp
Twilio webhook endpoint (internal use only)

### GET /health
Health check endpoint

## 💬 WhatsApp Conversation Flow

```
User: Hi
Server: Which product is this review for?

User: iPhone 15
Server: What's your name?

User: Aditi
Server: Please send your review for iPhone 15.

User: Amazing battery life, very satisfied.
Server: Thanks Aditi -- your review for iPhone 15 has been recorded.
```

## 🗄️ Database Schema

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    contact_number TEXT NOT NULL,
    user_name TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_review TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚢 Deployment

### Railway
```bash
railway login
railway init
railway add
railway up
```

### Render
1. Connect GitHub repo
2. Set environment variables
3. Deploy

### Heroku
```bash
heroku create
git push heroku main
```

## 📝 License

MIT License
