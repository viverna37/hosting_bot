from fastapi import APIRouter, Depends, HTTPException

from api.models.user import UserStartResponse, UserStartRequest, SavePhoneResponse, SavePhoneRequest
from api.services.user_service import UserService, UserNotFoundError
from api.deps import get_user_service


router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.post(
    "/start",
    response_model=UserStartResponse,
)
async def user_start(
    payload: UserStartRequest,
    service: UserService = Depends(get_user_service),
):
    try:
        result = await service.handle_start(payload.telegram_id)
        return result

    except UserNotFoundError:
        raise HTTPException(status_code=403, detail="Access denied")


@router.post(
    "/phone",
    response_model=SavePhoneResponse,
)
async def save_phone(
    payload: SavePhoneRequest,
    service: UserService = Depends(get_user_service),
):
    try:
        await service.save_phone(
            telegram_id=payload.telegram_id,
            phone_number=payload.phone_number,
        )
        return SavePhoneResponse(success=True)

    except UserNotFoundError:
        raise HTTPException(status_code=403, detail="Access denied")
