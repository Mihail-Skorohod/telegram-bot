import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Отримання змінних з середовища
TOKEN = os.environ.get("7738100977:AAFPyyWI4d7-sGysDJDPabkSrNO00RHjYmQ")
OWNER_ID = int(os.environ.get("5428375273", 0))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привіт, {user.mention_html()}! 👋\n\n"
        f"Я ваш особистий бот для зв'язку.\n"
        f"Надішліть мені повідомлення, і я передам його власнику."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /help."""
    await update.message.reply_text(
        "Доступні команди:\n"
        "/start - Почати роботу з ботом\n"
        "/help - Показати цю довідку\n\n"
        "Просто напишіть своє повідомлення, і я передам його власнику."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник звичайних повідомлень."""
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    user_message = update.message.text
    
    # Відправляємо повідомлення власнику бота
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"📨 Нове повідомлення:\n\n"
             f"👤 Від: {user_name} (ID: {user_id})\n"
             f"💬 Повідомлення: {user_message}"
    )
    
    # Відповідаємо користувачу
    await update.message.reply_text(
        "Дякую за ваше повідомлення! Воно було передане власнику."
    )

def main() -> None:
    """Запуск бота."""
    # Створюємо додаток
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаємо бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
# Додайте в кінці main() функції
port = int(os.environ.get('PORT', 5000))