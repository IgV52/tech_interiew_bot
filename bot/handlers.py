import os
from bot import constants

from bot.utils import info_format_file
from bot.database.db import db, get_or_create_user

def save_document(update, context):
    user = get_or_create_user(db, update)
    update.message.reply_text('Обрабатываем фaйл')
    name_file = update.message.document.file_name
    file_name = os.path.join('downloads', name_file)
    if user['role'] == constants.ADMIN:
        os.makedirs('downloads', exist_ok=True)
        document_file = context.bot.getFile(update.message.document.file_id)
        document_file.download(file_name)
        text_msg = info_format_file(name_file)
        update.message.reply_text(f'Администратор, {text_msg}')
    else:
        update.message.reply_text('Ошибка доступа')