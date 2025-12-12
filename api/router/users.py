from fastapi import APIRouter, Response

from api.db.mongo import user_db

router = APIRouter(prefix="/users")


@router.get("/get_user")
async def get_user(
        telegram_id: str
):
    user = await user_db.get_user(telegram_id)
    if not user.telegram_id:
        return Response(status_code=403)
    return user
