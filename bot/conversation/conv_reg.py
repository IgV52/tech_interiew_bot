from telegram.ext import ConversationHandler
from bot.database.db import db, get_or_create_user, reg_user
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversation.utils import (
    get_date,
    get_city,
    check_phone,
    inline_keyboard,
)


def reg(update, context):
    context.user_data.clear()
    user = get_or_create_user(db, update.effective_user, update.message)
    if user.get("reg_info", False):
        return ConversationHandler.END

    context.user_data["msg_bot"] = update.message.reply_text(
        """<b>Вы даете свое согласие на обработку персональных данных?</b>""",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard([("Да", "yes"), ("Нет", "stop")]),
    )
    return "personal_info"


def personal_info(update, context):
    answer = {"yes": "Да"}
    state = "personal_info"

    if not update.callback_query:
        update.message.delete()

    if update.callback_query and (text := answer.get(update.callback_query.data)):
        context.user_data["personal_info"] = text
        context.user_data["msg_bot"].edit_text(
            """Пожалуйста введите <b>ФИО</b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
            ),
        )
        state = "fio"
    else:
        context.user_data["msg_bot"].edit_text(
            """<b>Вы даете свое согласие на обработку персональных данных?</b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard([("Да", "yes"), ("Нет", "stop")]),
        )

    return state


def fio(update, context):
    state = "fio"
    answer = update.message.text
    update.message.delete()

    if len(answer.split()) < 3:
        try:
            context.user_data["msg_bot"].edit_text(
                f"Пожалуйста введите в формате <b>ФИО</b>\nВы ввели {answer}",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
                ),
            )
        except Exception as exp:
            print(exp)
            pass
    else:
        context.user_data["user_name"] = answer
        context.user_data["msg_bot"].edit_text(
            """Введите дату вашего рождения в формате <b>дд.мм.гггг</b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
            ),
        )
        state = "birth_date"

    return state


def birth_date(update, context):
    state = "birth_date"
    date = get_date(update.message.text)
    update.message.delete()

    if not date:
        context.user_data["msg_bot"].edit_text(
            """Введите дату вашего рождения в формате <b>дд.мм.гггг</b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
            ),
        )
    else:
        context.user_data["birth_date"] = date
        context.user_data["msg_bot"].edit_text(
            """<b>Из какого вы города?</b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
            ),
        )
        state = "location"

    return state


def location(update, context):
    city = get_city(update.message.text)
    context.user_data["location"] = update.message.text
    update.message.delete()

    if not city:
        context.user_data["msg_bot"].edit_text(
            """<b>Готовы ли вы переехать в Москву?</b>""",
            reply_markup=inline_keyboard([("Да", "yes_rel"), ("Нет", "no_rel")]),
            parse_mode=ParseMode.HTML,
        )
        state = "new_location"
    else:
        context.user_data["msg_bot"].edit_text(
            """<b>Какой формат работы вы рассматриваете?</b>""",
            reply_markup=inline_keyboard(
                [
                    ("Удаленка", "online"),
                    ("Офис", "office"),
                    ("Гибрид(удаленка+офис)", "online_office"),
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        state = "format_job"

    return state


def new_location(update, context):
    answer = {"yes_rel": "Да", "no_rel": "Нет"}
    state = "new_location"

    if not update.callback_query:
        update.message.delete()

    if update.callback_query and (text := answer.get(update.callback_query.data)):
        context.user_data["relocation"] = text
        context.user_data["msg_bot"].edit_text(
            """<b>Какой формат работы вы рассматриваете?</b>""",
            reply_markup=inline_keyboard(
                [
                    ("Удаленка", "online"),
                    ("Офис", "office"),
                    ("Гибрид(удаленка+офис)", "online_office"),
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        state = "format_job"
    else:
        try:
            context.user_data["msg_bot"].edit_text(
                """<b>Готовы ли вы переехать в Москву?</b>""",
                reply_markup=inline_keyboard([("Да", "yes_rel"), ("Нет", "no_rel")]),
                parse_mode=ParseMode.HTML,
            )
        except Exception as exp:
            print(exp)
            pass

    return state


def format_job(update, context):
    answer = {
        "online": "Удаленка",
        "office": "Офис",
        "online_office": "Гибрид(удаленка+офис)",
    }
    state = "format_job"

    if not update.callback_query:
        update.message.delete()

    if update.callback_query and (text := answer.get(update.callback_query.data)):
        context.user_data["format_job"] = text
        context.user_data["msg_bot"].edit_text(
            """Рассматриваемый уровень зарплаты: <b>минимум - комфорт</b>""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
            ),
            parse_mode=ParseMode.HTML,
        )
        state = "salary"

    else:
        try:
            context.user_data["msg_bot"].edit_text(
                """<b>Нажмите доступную кнопку</b>""",
                reply_markup=inline_keyboard(
                    [
                        ("Удаленка", "online"),
                        ("Офис", "office"),
                        ("Гибрид(удаленка+офис)", "online_office"),
                    ]
                ),
                parse_mode=ParseMode.HTML,
            )
        except Exception as exp:
            print(exp)
            pass

    return state


def salary(update, context):
    context.user_data["salary"] = update.message.text
    update.message.delete()
    context.user_data["msg_bot"].edit_text(
        """Напишите свой номер телефона в формате <b>+7</b>""",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
        ),
    )
    return "number_phone"


def number_phone(update, context):
    user_phone = update.message.text
    update.message.delete()
    check = check_phone(user_phone)

    if not check:
        context.user_data["msg_bot"].edit_text(
            """
            <b>Неправильно набран номер</b>
            Напишите свой номер телефона в формате <b>+7</b>
            """,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
            ),
        )
        return "number_phone"
    else:
        context.user_data["number_phone"] = user_phone
        context.user_data["user_id"] = update.effective_user.id
        data_user = context.user_data
        reg_user(db, data_user)
        context.user_data["msg_bot"].edit_text(
            """<b>Все ответы записаны, можем начать</b> /start""",
            parse_mode=ParseMode.HTML,
        )
        context.user_data.clear()
        return ConversationHandler.END


def dialogue_dontknow(update, context):
    context.user_data["msg_bot"].edit_text(
        """<b>Я вас не понимаю</b>""",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Выход", callback_data="stop")]]
        ),
    )


def end(update, context):
    context.user_data["msg_bot"].edit_text("Вы вышли /start")
    context.user_data.clear()
    return ConversationHandler.END
