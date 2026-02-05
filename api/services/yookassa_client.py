import uuid
from typing import TypedDict

from yookassa import Payment, Configuration

from config.config import load_config

config = load_config()
Configuration.account_id = config.yookassa.account_id
Configuration.secret_key = config.yookassa.secret_key



class CreatedPayment(TypedDict):
    payment_id: str
    payment_url: str


async def create_subscription_payment(
    *,
    amount: int,
    subscription_id: int,
    client_id: int,
    return_url: str,
phone_number: str
) -> CreatedPayment:
    """
    Создание платежа для ежемесячной подписки
    (ЮKassa, СБП)

    amount — сумма в рублях
    subscription_id — ID подписки (для webhook)
    client_id — ID клиента (для логов / аналитики)
    """

    payment = Payment.create(
        {
            "amount": {
                "value": f"{amount}.00",
                "currency": "RUB",
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url,
            },
            "capture": True,
            "description": "Ежемесячная оплата услуг",
            "metadata": {
                "subscription_id": subscription_id,
                "client_id": client_id,
            },
            "receipt": {
                "customer": {
                    "phone": phone_number
                },
                "items": [
                    {
                        "description": "Абонентская плата",
                        "quantity": "1.00",
                        "amount": {
                            "value": amount,
                            "currency": "RUB"
                        },
                        "vat_code": 1,
                        "payment_mode": "full_payment",
                        "payment_subject": "commodity"
                    }
                ]
            }
        },
        uuid.uuid4().hex,  # idempotency key
    )

    return {
        "payment_id": payment.id,
        "payment_url": payment.confirmation.confirmation_url,
    }
