from fastapi import APIRouter, Depends

from api.deps import verify_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin endpoints"]
)

@router.post(
    "/access",
    dependencies=[Depends(verify_admin)]
)
async def auth():
    return {"ok": True}


