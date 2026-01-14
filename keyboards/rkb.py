from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class RKB:
    class User:
        @staticmethod
        def get_main_menu() -> types.ReplyKeyboardMarkup:
            """Главное меню клиента"""
            builder = ReplyKeyboardBuilder()
            btn_list = ["♻️ Каталог", "⚙️ Мой кабинет", "🤷‍♂️ Поддержка", "📨 Отзывы (2437)"]

            for i in btn_list:
                builder.button(text=i)

            # Оптимальное расположение
            builder.adjust(2)

            return builder.as_markup(
                resize_keyboard=True
            )

        @staticmethod
        def get_support_menu() -> types.ReplyKeyboardMarkup:
            """Главное меню клиента"""
            builder = ReplyKeyboardBuilder()

            builder.button(text="💬 Вопрос")
            builder.button(text="🆘 Проблема")
            builder.button(text="❗️ У меня проблема с платежом")

            # Оптимальное расположение
            builder.adjust(2)

            return builder.as_markup(
                resize_keyboard=True
            )

        @staticmethod
        def get_top_up_keyboard() -> types.ReplyKeyboardMarkup:
            """Главное меню клиента"""
            builder = ReplyKeyboardBuilder()


            builder.button(text=f"USDT TRC20")
            builder.button(text=f"BTC")
            builder.button(text=f"LTC")
            builder.button(text=f"СБП")
            builder.button(text=f"Альфа-Банк")
            builder.button(text=f"Банковская карта")
            builder.button(text=f"Трансгран")

            # Оптимальное расположение
            builder.adjust(3, 4)

            return builder.as_markup(
                resize_keyboard=True
            )