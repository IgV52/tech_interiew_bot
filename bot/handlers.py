import os
from bot import constants
from telegram import ParseMode

from bot.utils import info_format_file
from bot.database.db import db, get_or_create_user, get_all_pincode


def save_document(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text("Обрабатываем фaйл")
    name_file = update.message.document.file_name
    company_pincode = update.message.caption.strip().split("-")  # company-pincode
    file_name = os.path.join("downloads", name_file)
    if user["role"] == constants.ADMIN and len(company_pincode) == 2:
        os.makedirs("downloads", exist_ok=True)
        document_file = context.bot.getFile(update.message.document.file_id)
        document_file.download(file_name)
        text_msg = info_format_file(name_file, company_pincode)
        update.message.reply_text(f"Администратор, \n, {text_msg}")
    else:
        update.message.reply_text("Ошибка доступа")


def get_all_company_pincode(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)

    if user["role"] == constants.ADMIN:
        update.message.reply_text(f"Администратор, \n{get_all_pincode(db)}", parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Ошибка доступа")
