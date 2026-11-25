import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI(title="Synagogue API")

# אפשור CORS כדי שה-Frontend יוכל לדבר עם ה-Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")
supabase: Client = create_client(url, key)

class DonationCreate(BaseModel):
    donor_name: str
    amount: float

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

# בקשת קריאה מה-DB
@app.get("/api/donations")
def get_donations():
    response = supabase.table("quick_donations").select("*").order("created_at", desc=True).limit(5).execute()
    return response.data

# בקשת כתיבה ל-DB (המשימה שלך לבדיקת תשתית!)
@app.post("/api/donations")
def add_donation(donation: DonationCreate):
    response = supabase.table("quick_donations").insert({
        "donor_name": donation.donor_name,
        "amount": donation.amount
    }).execute()
    return {"status": "success", "data": response.data}
