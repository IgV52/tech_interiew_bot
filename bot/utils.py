from bot.addons.add_file import open_file_docx
from bot import constants, settings

def check_role(user_id: int):
    if str(user_id) in settings.ADMIN:
        return constants.ADMIN
    return constants.USER

def info_format_file(name_file):
    format_file = (name_file.split('.')[-1])
    name_vacan = (name_file.split('.')[0])
    if format_file == constants.FILE_DOCX:
        text_msg = open_file_docx(name_file, name_vacan)  
    else:
        text_msg = 'Данные не загружены в базу'
    return text_msg
