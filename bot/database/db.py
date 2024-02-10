from pymongo import MongoClient
from bot.utils import check_role
from datetime import datetime
from bot import settings

client = MongoClient(settings.MONGO_LINK)
print(settings.MONGO_DB, 3423423234)
db = client[settings.MONGO_DB]  # MONGO_DB - название базы данных


def reg_user(db, data_user: dict):
    user = db.users.find_one({"user_id": data_user["user_id"]})
    if not "reg_info" in user:
        db.users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "reg_info": {
                        "user_name": data_user["user_name"],
                        "birth_date": data_user["birth_date"],
                        "location": data_user["location"],
                        "relocation": data_user["relocation"],
                        "format_job": data_user["format_job"],
                        "salary": data_user["salary"],
                        "number_phone": data_user["number_phone"],
                        "personal_info": data_user["personal_info"],
                    }
                }
            },
        )
    return user


def get_or_create_user(db, effective_user, message):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": message.chat_id,
            "date": message.date,
            "role": check_role(effective_user.id),
        }
        db.users.insert_one(user)
    return user


def save_anketa(db, anketa_data: dict):
    user = db.users.find_one({"user_id": anketa_data["user_id"]})
    add_anketa = {
        "company": anketa_data["company"],
        "vacan": anketa_data["vacan"],
        "answer": anketa_data["answer"],
        "question": anketa_data["question"],
        "pincode": anketa_data["pincode"],
        "userfile": anketa_data["userfile"],
        "time": datetime.now(),
    }
    if not "anketa" in user:
        db.users.update_one({"_id": user["_id"]}, {"$set": {"anketa": [add_anketa]}})
    else:
        db.users.update_one({"_id": user["_id"]}, {"$push": {"anketa": add_anketa}})


def get_or_create_job(db, file: dict):
    # Ищет в базе компанию по названию
    # если не находит то создает и добавляет данные
    job = db.jobs.find_one({"company": file["company"]})
    if not job:
        job = {
            "company": file["company"],
            "pincode": file["pincode"],
            "vacancy": [file["vacancy"]],
        }
        db.jobs.insert_one(job)
    # если находит то проверяет добавляемые вакансии по пинкоду
    else:
        use_pin = [pin["pincode"] for pin in job["vacancy"]]
        # если находит использованный пинкод то не добавляет вакансию
        if file["vacancy"]["pincode"] in use_pin:
            return None
        db.jobs.update_one({"_id": job["_id"]}, {"$push": {"vacancy": file["vacancy"]}})
    return job


def info_vacan_in_company(db, pincodes: list):
    job = db.jobs.find_one({"pincode": pincodes[0]})
    return job


def check_company(db, company: str):
    company = db.jobs.find_one({"company": company})
    if not company:
        return [False]
    return [True, company]
