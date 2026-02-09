from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from api_client.api_client import ApiClient
from bot.keyboards.ikb import IKB
from api.services.yookassa_client import create_subscription_payment

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
async def start_handler(message: Message, api: ApiClient):
    tg_id = message.from_user.id

    result = await api.user_start(tg_id)

    # ❌ Нет доступа
    if result.get("action") == "NO_ACCESS":
        await message.answer(
            "⛔ У вас нет доступа.\n"
            "Обратитесь к администратору."
        )
        return

    # 📞 Нужно запросить телефон
    if result.get("action") == "REQUEST_PHONE":
        await message.answer(
            "Для продолжения работы отправьте номер телефона 👇",
            reply_markup=IKB.User.get_contact_keyboard()
        )
        return

    # 🟢 Показать ЛК
    if result.get("action") == "SHOW_CABINET":
        client = result["client"]
        sub = result["subscription"]

        text = (
            f"👤 <b>{client['full_name']}</b>\n"
            f"📅 Дата оплаты: {sub['due_date']}\n"
            f"💳 Сумма: {sub['amount']} ₽\n"
            f"📌 Статус: {sub['status']}"
        )

        await message.answer(
            text,
            reply_markup=ReplyKeyboardRemove(),
        )



@router.message(F.contact)
async def contact_handler(message: Message, api: ApiClient):
    tg_id = message.from_user.id
    phone = message.contact.phone_number

    await api.save_phone(
        telegram_id=tg_id,
        phone_number=phone,
    )

    # после сохранения — снова /start
    await start_handler(message, api)

@router.callback_query(F.data.startswith("pay_"))
async def pay_subscription_handler(
        callback: CallbackQuery
):
    telegram_id = callback.from_user.id
    subscription_id = int(callback.data.split("_")[1])

    # 1️⃣ Проверяем клиента
    client = await repository.clients_repo.get_by_telegram_id(telegram_id)
    if not client or client.status != "active":
        await callback.answer("Нет доступа", show_alert=True)
        return

    # 2️⃣ Проверяем подписку
    subscription = await repository.subscriptions_repo.get_by_id(subscription_id)
    if not subscription or subscription.client_id != client.id:
        await callback.answer("Подписка не найдена", show_alert=True)
        return

    # 3️⃣ Если уже оплачено (маловероятно, но защита)
    if subscription.status == "paid":
        await callback.answer("Уже оплачено", show_alert=True)
        return

    # 4️⃣ Проверка на pending-платёж
    existing_payment = await repository.payments_repo.get_pending_by_subscription(subscription.id)
    if existing_payment:
        await callback.message.answer(
            "💳 <b>Оплата</b>\n\n"
            f"Сумма: <b>{subscription.amount} ₽</b>\n\n"
            "У вас уже есть активная ссылка для оплаты:",
            reply_markup=IKB.User.payment_link(existing_payment.payment_url)
        )
        await callback.answer()
        return

    # 5️⃣ Создаём платёж в ЮKassa
    payment_data = await create_subscription_payment(
        amount=subscription.amount,
        subscription_id=subscription.id,
        client_id=client.id,
        return_url="https://t.me/bozdyrevdev_hosting_bot",
        phone_number=client.phone_number
    )

    # 6️⃣ Сохраняем платёж в БД
    await repository.payments_repo.create(
        client_id=client.id,
        subscription_id=subscription.id,
        payment_id=payment_data["payment_id"],
        payment_url=payment_data["payment_url"],
        amount=subscription.amount,
    )

    # 7️⃣ Отдаём ссылку клиенту
    await callback.message.answer(
        "💳 <b>Оплата</b>\n\n"
        f"Сумма: <b>{subscription.amount} ₽</b>\n\n"
        "Нажмите кнопку ниже для оплаты:",
        reply_markup=IKB.User.payment_link(payment_data["payment_url"])
    )

    await callback.answer()
