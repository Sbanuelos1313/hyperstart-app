import os

files = {
    'app/routers/admin.py': '''from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db, User, StudentProgress
from app.auth import require_admin
import csv, io
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, admin=Depends(require_admin), db: Session = Depends(get_db)):
    total_students = db.query(User).filter(User.role == "student").count()
    schools = db.query(User.school, func.count(User.id)).filter(User.role == "student").group_by(User.school).all()
    zips = db.query(User.zip_code, func.count(User.id)).filter(User.role == "student").group_by(User.zip_code).all()
    prog = db.query(StudentProgress).all()
    fields = ["conf", "aware", "money", "why"]
    pre_avg = {}
    post_avg = {}
    for f in fields:
        pre_vals = [getattr(p, f"pre_{f}") for p in prog if getattr(p, f"pre_{f}") > 0]
        post_vals = [getattr(p, f"post_{f}") for p in prog if getattr(p, f"post_{f}") > 0]
        pre_avg[f] = round(sum(pre_vals)/len(pre_vals), 1) if pre_vals else 0
        post_avg[f] = round(sum(post_vals)/len(post_vals), 1) if post_vals else 0
    sparks_done = db.query(StudentProgress).filter(StudentProgress.career_sparks_done == True).count()
    ai_started = db.query(StudentProgress).filter(StudentProgress.ai_mod > 0).count()
    eng_done = db.query(StudentProgress).filter(StudentProgress.eng_done == True).count()
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, "admin": admin, "total_students": total_students,
        "schools": schools, "zips": zips, "pre_avg": pre_avg, "post_avg": post_avg,
        "sparks_done": sparks_done, "ai_started": ai_started, "eng_done": eng_done, "fields": fields
    })

@router.get("/students", response_class=HTMLResponse)
async def students(request: Request, admin=Depends(require_admin), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").order_by(User.school, User.full_name).all()
    return templates.TemplateResponse("admin/students.html", {"request": request, "admin": admin, "students": students})

@router.get("/api/export/csv")
async def export_csv(admin=Depends(require_admin), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "School", "Grade", "Zip", "Cluster", "XP"])
    for s in students:
        writer.writerow([s.full_name, s.school, s.grade, s.zip_code, s.cluster or "", s.xp])
    return Response(content=output.getvalue(), media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=hyperstart.csv"})
''',

    'app/routers/auth.py': '''from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db, User, StudentProgress
from app.auth import authenticate_user, create_token, hash_password

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(email.lower().strip(), password, db)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})
    token = create_token({"sub": user.email, "role": user.role})
    redirect_url = "/admin/dashboard" if user.role in ("admin", "teacher") else "/student/home"
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie("hs_token", token, httponly=True, max_age=86400, samesite="lax")
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("hs_token")
    return response

@router.post("/register")
async def register(request: Request, email: str = Form(...), password: str = Form(...),
    full_name: str = Form(...), grade: int = Form(...), school: str = Form(...),
    zip_code: str = Form(default=""), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email.lower()).first()
    if existing:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email already registered"})
    user = User(email=email.lower().strip(), hashed_password=hash_password(password),
        full_name=full_name, grade=grade, school=school, zip_code=zip_code, role="student")
    db.add(user)
    db.flush()
    db.add(StudentProgress(user_id=user.id))
    db.commit()
    token = create_token({"sub": user.email, "role": user.role})
    response = RedirectResponse(url="/student/home", status_code=302)
    response.set_cookie("hs_token", token, httponly=True, max_age=86400, samesite="lax")
    return response
''',

    'app/routers/student.py': '''from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db, User, StudentProgress, SessionLog
from app.auth import require_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, user=Depends(require_user), db: Session = Depends(get_db)):
    if user.role in ("admin", "teacher"):
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    if not user.progress:
        db.add(StudentProgress(user_id=user.id))
        db.commit()
        db.refresh(user)
    return templates.TemplateResponse("student/portal.html", {
        "request": request, "user": user, "progress": user.progress,
        "pre_done": user.progress.pre_done if user.progress else False
    })

@router.post("/api/pre-assessment")
async def save_pre(request: Request, user=Depends(require_user), db: Session = Depends(get_db)):
    data = await request.json()
    p = user.progress or StudentProgress(user_id=user.id)
    if not user.progress:
        db.add(p)
    p.pre_conf = data.get("conf", 0)
    p.pre_aware = data.get("aware", 0)
    p.pre_money = data.get("money", 0)
    p.pre_why = data.get("why", 0)
    p.pre_done = True
    db.commit()
    return {"status": "ok"}

@router.post("/api/progress")
async def save_progress(request: Request, user=Depends(require_user), db: Session = Depends(get_db)):
    data = await request.json()
    p = user.progress
    if not p:
        p = StudentProgress(user_id=user.id)
        db.add(p)
    if "cluster" in data:
        user.cluster = data["cluster"]
        p.career_sparks_done = True
        p.career_sparks_cluster = data["cluster"]
    if "xp" in data:
        user.xp = max(user.xp, data["xp"])
    if "money_mod" in data:
        p.money_mod = max(p.money_mod, data["money_mod"])
    if "think_q" in data:
        p.think_q = max(p.think_q, data["think_q"])
    if "story_done" in data:
        p.story_done = data["story_done"]
    if "ai_mod" in data:
        p.ai_mod = max(p.ai_mod, data["ai_mod"])
    if "eng_done" in data:
        p.eng_done = data["eng_done"]
    if "reflections" in data:
        existing = p.reflections or {}
        existing.update(data["reflections"])
        p.reflections = existing
    db.add(SessionLog(user_id=user.id, school=user.school, zip_code=user.zip_code,
        action="progress", module=data.get("module", "general"), xp_earned=data.get("xp_delta", 0)))
    db.commit()
    return {"status": "ok", "xp": user.xp}

@router.get("/api/me")
async def get_me(user=Depends(require_user)):
    p = user.progress
    return {"id": user.id, "name": user.full_name, "grade": user.grade, "school": user.school,
        "xp": user.xp, "cluster": user.cluster, "role": user.role,
        "progress": {"pre_done": p.pre_done if p else False, "money_mod": p.money_mod if p else 0,
            "think_q": p.think_q if p else 0, "story_done": p.story_done if p else False,
            "ai_mod": p.ai_mod if p else 0, "eng_done": p.eng_done if p else False,
            "career_sparks_done": p.career_sparks_done if p else False,
            "reflections": p.reflections if p else {}} if p else {}}
''',

    'app/routers/api.py': '''from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "HyperStart"}
''',

    'app/routers/__init__.py': '',
    'app/__init__.py': '',
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {path}')

print('All done.')
