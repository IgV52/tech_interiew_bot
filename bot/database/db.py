from pymongo import MongoClient
from bot.utils import check_role
from datetime import datetime
from bot import settings

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB] # MONGO_DB - название базы данных

def reg_user(db, data_user: dict):
    user = db.users.find_one({"user_id" : data_user['user_id']})
    del data_user['user_id']
    if not 'reg_info' in user:
        db.users.update_one({'_id': user['_id']}, {'$set': {'reg_info': data_user}})
    return user

def get_or_create_user(db, update):
    user = db.users.find_one({"user_id" : update.effective_user.id})
    if not user:
        user = {
            "user_id" : update.effective_user.id,
            "first_name" : update.effective_user.first_name,
            "last_name" : update.effective_user.last_name,
            "username" : update.effective_user.username,
            "chat_id" : update.message.chat_id,
            "date" : update.message.date,
            "role" : check_role(update.effective_user.id)
        }
        db.users.insert_one(user)
    return user

def save_anketa(db, anketa_data: dict):
    user = db.users.find_one({"user_id" : anketa_data['user_id']})
    anketa_data['time'] = datetime.now()
    reg_info = anketa_data["reg_info"]
    del anketa_data["reg_info"]
    del anketa_data['user_id']
    if not 'anketa' in user:
        db.users.update_one({'_id': user['_id']}, {'$set': {'anketa': [anketa_data]}})
    else:
        db.users.update_one({'_id': user['_id']}, {'$push': {'anketa': anketa_data}})
    anketa_data['reg_info'] = reg_info

def get_or_create_job(db, file: dict):
    #Ищет в базе компанию по названию
    #если не находит то создает и добавляет данные
    job = db.jobs.find_one({'company' : file['company']})
    if not job:
        job = {
            'company' : file['company'],
            'pincode': file['pincode'],
            'vacancy' : [file['vacancy']]
            }
        db.jobs.insert_one(job)
    #если находит то проверяет добавляемые вакансии по пинкоду
    else:
        use_pin = [pin['pincode'] for pin in job['vacancy']]
        #если находит использованный пинкод то не добавляет вакансию
        if file['vacancy']['pincode'] in use_pin:
            return None
        db.jobs.update_one({'_id': job['_id']}, {'$push': {'vacancy': file['vacancy']}})
    return job

def info_vacan_in_company(db, pincodes: list):
    job = db.jobs.find_one({'pincode' : pincodes[0]})
    return job

def check_company(db, company: str):
    company = db.jobs.find_one({'company': company})
    if not company:
        return [False]
    return [True, company]