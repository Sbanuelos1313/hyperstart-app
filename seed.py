"""
Run once to seed admin accounts and demo student profiles.
Usage: python seed.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, SessionLocal, User, StudentProgress
from app.auth import hash_password
from datetime import datetime

Base.metadata.create_all(bind=engine)
db = SessionLocal()

ADMINS = [
    {"email": "sam@chronos-ai.net", "name": "Sam Banuelos", "password": "HyperStart2026!"},
    {"email": "admin@hyperstart.net", "name": "HyperStart Admin", "password": "HyperStart2026!"},
    {"email": "demo@hyperstart.net", "name": "Demo Admin", "password": "Demo2026!"},
]

DEMO_STUDENTS = [
    {"email": "zara@demo.hyperstart.net", "name": "Zara Williams", "grade": 7, "school": "F.D. Moon Middle School", "zip": "73111", "xp": 0},
    {"email": "mateo@demo.hyperstart.net", "name": "Mateo Rivera", "grade": 8, "school": "Classen SAS", "zip": "73103", "xp": 150, "cluster": "Tech & Innovation"},
    {"email": "destiny@demo.hyperstart.net", "name": "Destiny Brown", "grade": 6, "school": "Millwood Public Schools", "zip": "73110", "xp": 280, "cluster": "Health Sciences"},
    {"email": "kai@demo.hyperstart.net", "name": "Kai Nguyen", "grade": 7, "school": "F.D. Moon Middle School", "zip": "73111", "xp": 420, "cluster": "Engineering & Design"},
]

created = 0

for a in ADMINS:
    if not db.query(User).filter(User.email == a["email"]).first():
        user = User(email=a["email"], hashed_password=hash_password(a["password"]), full_name=a["name"], role="admin", grade=0, school="Chronos AI")
        db.add(user)
        print(f"Created admin: {a['email']}")
        created += 1

for s in DEMO_STUDENTS:
    if not db.query(User).filter(User.email == s["email"]).first():
        user = User(
            email=s["email"],
            hashed_password=hash_password("Demo2026!"),
            full_name=s["name"],
            role="student",
            grade=s["grade"],
            school=s["school"],
            zip_code=s["zip"],
            xp=s.get("xp", 0),
            cluster=s.get("cluster")
        )
        db.add(user)
        db.flush()
        prog = StudentProgress(
            user_id=user.id,
            pre_done=s.get("xp", 0) > 0,
            pre_conf=2 if s.get("xp", 0) > 0 else 0,
            pre_aware=2 if s.get("xp", 0) > 0 else 0,
            pre_money=1 if s.get("xp", 0) > 0 else 0,
            pre_why=2 if s.get("xp", 0) > 0 else 0,
            career_sparks_done=bool(s.get("cluster")),
            career_sparks_cluster=s.get("cluster"),
            money_mod=2 if s.get("xp", 0) >= 280 else (1 if s.get("xp", 0) >= 150 else 0),
            ai_mod=1 if s.get("xp", 0) >= 280 else 0,
        )
        db.add(prog)
        print(f"Created student: {s['name']} ({s['school']})")
        created += 1

db.commit()
print(f"\n✅ Seeded {created} accounts.")
print("\nAdmin login:")
print("  Email: demo@hyperstart.net")
print("  Password: Demo2026!")
print("\nDemo student logins (all password: Demo2026!):")
for s in DEMO_STUDENTS:
    print(f"  {s['name']}: {s['email']}")
db.close()
