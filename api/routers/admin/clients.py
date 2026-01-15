from fastapi import APIRouter, Depends, HTTPException

from api.deps import verify_admin, get_admin_service
from api.models.client import NewClientResponse, NewClientRequest
from api.services.admin_service import AdminService
from api.services.exceptions import ClientAlreadyExistsError, InvalidDueDateError, InvalidAmountError

router = APIRouter(
    prefix="/admin",
    tags=["Admin endpoints"]
)


@router.post(
    "/new-client",
    dependencies=[Depends(verify_admin)],
    response_model=NewClientResponse,
)
async def new_client(
    payload: NewClientRequest,
    service: AdminService = Depends(get_admin_service),
):
    try:
        result = await service.create_client(
            telegram_id=payload.telegram_id,
            full_name=payload.full_name,
            amount=payload.amount,
            due_date=payload.due_date,
        )
        return result

    except ClientAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Client already exists")

    except InvalidDueDateError:
        raise HTTPException(status_code=400, detail="Invalid due date")

    except InvalidAmountError:
        raise HTTPException(status_code=400, detail="Invalid amount")
