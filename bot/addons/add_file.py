import os
import logging
from docx import Document
from bot.database import db

import datetime

#Открывает документ который лежит в папке donwloads
def open_file_docx(name_file: str, company: str):
    basedir = os.path.join('downloads', name_file)
    doc = Document(basedir)
    dict_quest = dict()
#Читает документ
    try:
        for paragraph in doc.paragraphs:
            if paragraph.text:
                #Если в документе строка с ** то записывает
                #эту строку как пинкод
                if "**" in paragraph.text:
                    pincode = paragraph.text.replace("**",'')
                #Если в документе строка с * то записывает
                #эту строку как вакансию
                if '*' in paragraph.text:
                    vac = paragraph.text.replace("*",'')
                    num = 1
                    vacan = dict()
                    dict_quest['slots'] = {vac: vacan}
                #Строки без метки становятся вопросами
                else:
                    vacan[str(num)] = paragraph.text
                    num += 1
                #Формирует словарь с данными
                dict_quest['date'] = datetime.datetime.now()
                dict_quest['pincode'] = (str(pincode)).strip()
                dict_quest['slots'][vac] = vacan  
        text_msg = add_quest_vacan_slot(dict_quest, company)
    except UnboundLocalError as err:
        text_msg = 'Вы забыли поставить метку около вакансии "*"'
        logging.error(f'Ошибка {err} | from open_console_file')
    return text_msg

def add_quest_vacan_slot(info: dict, company: str):
    format_add_db_dict = create_dict_db(company, info)
    #Добавляет данные в базу или нет если есть совпадение по пинкоду
    answer_db = db.get_or_create_job(db.db, format_add_db_dict)
    if not answer_db:
        return 'Совпадение пинкодов данные не добавлены'
    return 'Данные успешно добавлены'

#Cоздает итоговый словарь для оправки в базу
def create_dict_db(company: str, blank: dict):
    db_dict = {'company': company, 'pincode': blank['pincode']+'!', 'vacancy': blank}
    return db_dict