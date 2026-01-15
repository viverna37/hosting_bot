from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.repository.main_repository import Repository
from bot.states.create_client import CreateClientState

router = Router()


@router.callback_query(F.data == "create_client")
async def create_client_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CreateClientState.full_name)

    await callback.message.answer(
        "Введите <b>имя клиента</b>:"
    )
    await callback.answer()


@router.message(CreateClientState.full_name)
async def create_client_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await state.set_state(CreateClientState.telegram_id)

    await message.answer(
        "Введите <b>Telegram ID</b> клиента:"
    )


@router.message(CreateClientState.telegram_id)
async def create_client_telegram_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Telegram ID должен быть числом")
        return

    await state.update_data(telegram_id=int(message.text))
    await state.set_state(CreateClientState.amount)

    await message.answer(
        "Введите <b>сумму оплаты</b> (в рублях):"
    )


@router.message(CreateClientState.amount)
async def create_client_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Сумма должна быть числом")
        return

    await state.update_data(amount=int(message.text))
    await state.set_state(CreateClientState.due_date)

    await message.answer(
        "Введите <b>дату оплаты</b> в формате:\n"
        "`YYYY-MM-DD`"
    )


@router.message(CreateClientState.due_date)
async def create_client_finish(
        message: Message,
        state: FSMContext,
        repository: Repository,
):
    try:
        due_date = datetime.strptime(message.text, "%Y-%m-%d")
    except ValueError:
        await message.answer("Неверный формат даты. Используй YYYY-MM-DD")
        return

    data = await state.get_data()

    # 1️⃣Создаём клиента
    client = await repository.clients_repo.create(
        telegram_id=data["telegram_id"],
        full_name=data["full_name"],
    )

    # 2️⃣ создаём подписку
    subscription = await repository.subscriptions_repo.create(
        client_id=client.id,
        amount=data["amount"],
        due_date=due_date,
    )

    await state.clear()

    await message.answer(
        "✅ <b>Клиент успешно добавлен</b>\n\n"
        f"👤 {client.full_name}\n"
        f"🆔 {client.telegram_id}\n"
        f"💰 {subscription.amount} ₽\n"
        f"📅 {subscription.due_date.strftime('%d.%m.%Y')}"
    )
