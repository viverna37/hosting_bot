from aiogram import F, Router
from aiogram.types import Message
from database.repository.main_repository import Repository
from keyboards.ikb import IKB

router = Router()

def build_client_cabinet_text(client, subscription) -> str:
    status_map = {
        "pending": "⏳ Ожидается",
        "paid": "✅ Оплачено",
        "overdue": "⚠️ Просрочено",
    }

    return (
        f"👤 <b>{client.full_name}</b>\n\n"
        f"💰 <b>Сумма:</b> {subscription.amount} ₽\n"
        f"📅 <b>Дата оплаты:</b> {subscription.due_date}\n"
        f"📌 <b>Статус:</b> {status_map.get(subscription.status, subscription.status)}"
    )

@router.message(F.text == "/start")
async def start_handler(
        message: Message,
        repository: Repository
):
    telegram_id = message.from_user.id

    client = await repository.clients_repo.get_by_telegram_id(telegram_id)

    # ❌ Клиент не найден
    if not client or client.status != "active":
        await message.answer(
            "⛔ У вас нет доступа к этому боту.\n\n"
            "Если это ошибка — обратитесь к администратору."
        )
        return

    subscription = await repository.subscriptions_repo.get_active_by_client(client.id)

    # Если подписки нет (редкий кейс)
    if not subscription:
        await message.answer(
            f"👤 {client.full_name}\n\n"
            "ℹ️ Для вас пока не назначена дата оплаты."
        )
        return

    # ✅ Личный кабинет
    await message.answer(
        build_client_cabinet_text(client, subscription),
        reply_markup=IKB.User.client_cabinet_keyboard(subscription)
    )
