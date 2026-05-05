@'
from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "HyperStart"}
'@ | Set-Content app\routers\api.py -Encoding UTF8
