from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db, User, StudentProgress
from app.auth import require_admin
from datetime import datetime
import csv, io

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, admin=Depends(require_admin), db: Session = Depends(get_db)):
    total_students = db.query(User).filter(User.role == "student").count()
    schools = db.query(User.school, func.count(User.id)).filter(User.role == "student").group_by(User.school).all()
    zips = db.query(User.zip_code, func.count(User.id)).filter(User.role == "student", User.zip_code != None).group_by(User.zip_code).all()
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
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "admin": admin, "total_students": total_students, "schools": schools, "zips": zips, "pre_avg": pre_avg, "post_avg": post_avg, "sparks_done": sparks_done, "ai_started": ai_started, "eng_done": eng_done, "fields": fields})

@router.get("/students", response_class=HTMLResponse)
async def students(request: Request, admin=Depends(require_admin), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").order_by(User.school, User.full_name).all()
    return templates.TemplateResponse("admin/students.html", {"request": request, "admin": admin, "students": students})

@router.get("/api/export/csv")
async def export_csv(admin=Depends(require_admin), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name","School","Grade","Zip","Cluster","XP","Pre Conf","Post Conf","Pre Aware","Post Aware","Sparks Done","AI Started","Eng Done"])
    for s in students:
        p = s.progress
        writer.writerow([s.full_name, s.school, s.grade, s.zip_code, s.cluster or "", s.xp, p.pre_conf if p else 0, p.post_conf if p else 0, p.pre_aware if p else 0, p.post_aware if p else 0, p.career_sparks_done if p else False, (p.ai_mod > 0) if p else False, p.eng_done if p else False])
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=hyperstart_{datetime.now().strftime('%Y%m%d')}.csv"})
