import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Synagogue API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")

supabase = None

# ניסיון התחברות ל-Supabase רק אם הוזן מפתח JWT תקין שמתחיל ב-ey
if url and key and key.startswith("ey"):
    try:
        from supabase import create_client
        supabase = create_client(url, key)
        print("Connected to Supabase successfully!")
    except Exception as e:
        print(f"Supabase connection error: {e}")
else:
    print("Running in local mock mode (Supabase not configured or key invalid).")

# רשימת דמה מקומית לגיבוי במידה ו-Supabase עדיין לא מוגדר
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
    if supabase:
        try:
            res = supabase.table("quick_donations").select("*").order("created_at", desc=True).limit(5).execute()
            return res.data
        except Exception as e:
            print(f"DB Error: {e}")
    return mock_donations

@app.post("/api/donations")
def add_donation(donation: DonationCreate):
    if supabase:
        try:
            res = supabase.table("quick_donations").insert({
                "donor_name": donation.donor_name,
                "amount": donation.amount
            }).execute()
            return {"status": "success", "data": res.data}
        except Exception as e:
            print(f"DB Error: {e}")
            
    # שמירה מקומית אם אין DB פעיל כרגע
    new_entry = {"donor_name": donation.donor_name, "amount": donation.amount}
    mock_donations.insert(0, new_entry)
    return {"status": "success", "data": [new_entry]}
