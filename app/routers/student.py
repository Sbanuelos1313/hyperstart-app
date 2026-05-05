from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from app.database import get_db, User, StudentProgress, SessionLog
from app.auth import require_user
import os

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, user=Depends(require_user), db: Session = Depends(get_db)):
    if user.role in ("admin", "teacher"):
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    if not user.progress:
        db.add(StudentProgress(user_id=user.id))
        db.commit()
        db.refresh(user)
    # Serve as static file - bypasses Jinja2 template rendering
    portal_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "student", "portal.html")
    with open(portal_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

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

@router.get("/business-builder", response_class=HTMLResponse)
async def business_builder(request: Request, user=Depends(require_user), db: Session = Depends(get_db)):
    if user.role in ("admin", "teacher"):
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    
    if not user.progress:
        p = StudentProgress(user_id=user.id)
        db.add(p)
        db.commit()
        db.refresh(user)

    return templates.TemplateResponse("student/business_builder.html", {
        "request": request,
        "user": user,
        "progress": user.progress,
        "cluster": user.cluster or "Tech & Innovation"
    })