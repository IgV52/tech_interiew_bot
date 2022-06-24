from bot.database.db import db, get_or_create_job

def add_quest_vacan_slot(info: dict, company: str):
    format_add_db_dict = create_dict_db(company, info)
    answer_db = get_or_create_job(db, format_add_db_dict)
    if not answer_db:
        return 'Совпадение пинкодов данные не добавлены'
    return 'Данные успешно добавлены'

def create_dict_db(company: str, blank: dict):
    db_dict = {'company': company, 'pincode': blank['pincode']+'!', 'vacancy': blank}
    return db_dict