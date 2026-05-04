from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db, User, StudentProgress
from app.auth import authenticate_user, create_token, hash_password, get_current_user
from datetime import timedelta

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

MASTER_EMAILS = ["sam@chronos-ai.net", "admin@hyperstart.net", "demo@hyperstart.net"]

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(email.lower().strip(), password, db)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password"
        })
    token = create_token({"sub": user.email, "role": user.role})
    redirect_url = "/admin/dashboard" if user.role in ("admin", "teacher") else "/student/home"
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie("hs_token", token, httponly=True, max_age=86400, samesite="lax")
    return response

@router.post("/api/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user = authenticate_user(data.get("email", "").lower().strip(), data.get("password", ""), db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.email, "role": user.role})
    return {"token": token, "role": user.role, "name": user.full_name}

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("hs_token")
    return response

@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    grade: int = Form(...),
    school: str = Form(...),
    zip_code: str = Form(default=""),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.email == email.lower()).first()
    if existing:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email already registered"
        })
    user = User(
        email=email.lower().strip(),
        hashed_password=hash_password(password),
        full_name=full_name,
        grade=grade,
        school=school,
        zip_code=zip_code,
        role="admin" if email.lower() in MASTER_EMAILS else "student"
    )
    db.add(user)
    db.flush()
    progress = StudentProgress(user_id=user.id)
    db.add(progress)
    db.commit()
    token = create_token({"sub": user.email, "role": user.role})
    redirect_url = "/admin/dashboard" if user.role == "admin" else "/student/home"
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie("hs_token", token, httponly=True, max_age=86400, samesite="lax")
    return response
