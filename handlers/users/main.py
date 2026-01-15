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
    await message.answer("""<b>ℹ️ Информация о сервисе</b>
    
Исполнитель:
<b>ИП Боздырев Глеб Валерьевич</b>
<b>ИНН: 245737897093</b>

<b>🖥 Оказываемая услуга</b>
Предоставление вычислительных ресурсов (аренда сервера) для размещения и работы Telegram-ботов клиентов.
Бот является закрытым сервисом. Доступ предоставляется только пользователям, добавленным администратором вручную.

<b>💳 Стоимость услуги</b>
Абонентская плата за аренду сервера для размещения Telegram-бота.
Стоимость — от 500 руб. в месяц.
Размер абонентской платы зависит от потребляемых ресурсов и согласовывается индивидуально.

<b>🔄 Порядок оказания услуги</b>
Клиент добавляется администратором в систему
Клиент получает доступ к боту
В боте отображается информация об услуге и стоимости
Клиент вносит ежемесячный платёж за аренду сервера
При своевременной оплате сервис продолжает работу

<b>⚠️ Дополнительно</b>
Услуга предоставляется по модели ежемесячной подписки
Напоминания о необходимости оплаты отправляются автоматически
При отсутствии оплаты доступ к сервису может быть ограничен""")
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
