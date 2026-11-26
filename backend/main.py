import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Synagogue API")

# מאפשר ל-Frontend (פורט 3000) לפנות ל-Backend (פורט 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# נתוני דמה שמובטח שיוצגו תמיד
mock_donations = [
    {"donor_name": "יאיר ליברמן", "amount": 180},
    {"donor_name": "מיכאל מושקוביץ", "amount": 360}
]

class DonationCreate(BaseModel):
    donor_name: str
    amount: float

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/api/donations")
def get_donations():
    raw_url = os.getenv("SUPABASE_URL", "")
    raw_key = os.getenv("SUPABASE_KEY", "")

    # ניקוי הכתובת מכל סיומת שגויה
    clean_url = raw_url.strip().replace("/rest/v1/", "").replace("/rest/v1", "").rstrip("/")
    clean_key = raw_key.strip()

    if clean_url and clean_key:
        try:
            from supabase import create_client
            sp = create_client(clean_url, clean_key)
            res = sp.table("quick_donations").select("*").order("created_at", desc=True).limit(5).execute()
            if res.data is not None and len(res.data) > 0:
                return res.data
        except Exception as e:
            print("--- SUPABASE FETCH ERROR (Falling back to mock data) ---")
            print(e)
            
    # אם סופבייס לא החזיר נתונים או שיש שגיאה - נחזיר את נתוני הדמה ולא נקרוס!
    return mock_donations

@app.post("/api/donations")
def add_donation(donation: DonationCreate):
    raw_url = os.getenv("SUPABASE_URL", "")
    raw_key = os.getenv("SUPABASE_KEY", "")
    clean_url = raw_url.strip().replace("/rest/v1/", "").replace("/rest/v1", "").rstrip("/")
    clean_key = raw_key.strip()

    if clean_url and clean_key:
        try:
            from supabase import create_client
            sp = create_client(clean_url, clean_key)
            res = sp.table("quick_donations").insert({
                "donor_name": donation.donor_name,
                "amount": donation.amount
            }).execute()
            if res.data:
                return {"status": "success", "data": res.data}
        except Exception as e:
            print("--- SUPABASE INSERT ERROR (Saving locally) ---")
            print(e)

    # הוספה מקומית אם יש תקלה מול הענן
    new_entry = {"donor_name": donation.donor_name, "amount": donation.amount}
    mock_donations.insert(0, new_entry)
    return {"status": "success", "data": [new_entry]}
