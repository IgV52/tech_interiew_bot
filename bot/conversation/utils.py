from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import re


def format_text(question: dict, num: str):
    user_text = f"""<b>Вопрос № {num}:</b>\n {question[num]}"""
    return user_text.replace("\\n", "\n")


def key_quest(dict_quest: dict):
    key = [key for key in dict_quest.keys()]
    return key


def get_date(date_usr: str):
    try:
        datetime.strptime(date_usr, "%d.%m.%Y").date()
    except (ValueError, TypeError):
        pass
    else:
        return date_usr


def get_city(city: str):
    job = ("moscow", "москва", "мск")
    city = ((str(city)).lower()).strip()
    if city in job:
        return True
    return False


def check_phone(phone: str):
    phone = str(phone)
    format_phone = re.sub(r"\b\D", "", phone)
    clear_phone = re.sub(r"[\ \(]?", "", format_phone)
    if re.findall(r"^[\+7|8]*?\d{10}$", clear_phone) or re.match(
        r"^\w+[\.]?(\w+)*\@(\w+\.)*\w{2,}$", phone
    ):
        return bool(phone)
    else:
        return False


def pincode(pincode: str):
    pincode = str(pincode)
    pincode = (pincode.strip()).split("-")
    return pincode


def search_vacan(vacan: list, pincodes: str):
    vacan = [v["slots"] for v in vacan if v["pincode"] == pincodes]
    return vacan


def format_dict(dicts: dict):
    good_dict = {
        "user_id": dicts["user_id"],
        "company": dicts["company"],
        "vacan": dicts["vacan"],
        "answer": dicts["answer"],
        "question": dicts["question"],
        "pincode": dicts["pincode"],
        "reg_info": dicts["reg_info"],
    }
    return good_dict


def get_use_code(user: dict, pincodes: str):
    use_pincode = [pin["pincode"] for pin in user["anketa"]]
    if pincodes in use_pincode:
        return True
    return False


def keyboard_add_button(list_info: list, button: str = None):
    keyboard = [[]]
    button = button
    list_info = list_info
    if button:
        keyboard = [[button]]
    keyboard.insert(0, list_info)
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


def inline_keyboard(button: list[tuple[str, ...]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=label, callback_data=data)
                for label, data in button
            ],
            [InlineKeyboardButton(text="Выход", callback_data="stop")],
        ]
    )
