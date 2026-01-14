from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



class IKB:
    class User:
        @staticmethod
        def client_cabinet_keyboard(subscription):
            builder = InlineKeyboardBuilder()


            if subscription.status != "paid":
                builder.button(text="💳 Оплатить", callback_data=f"pay_{subscription.id}")
            builder.button(text="📄 История платежей", callback_data=f"payments_history")
            builder.adjust(1)

            return builder.as_markup()


    class Admin:
        @staticmethod
        def get_main_menu()-> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(text="Новый клиент", callback_data="create_client")

            builder.adjust(1)

            return builder.as_markup()