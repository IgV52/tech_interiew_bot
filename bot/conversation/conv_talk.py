from telegram.ext import ConversationHandler
from bot.addons.format_add_blank_user import create_word_file
from bot.database.db import db, info_vacan_in_company, get_or_create_user
from telegram import ParseMode, ReplyKeyboardRemove
from bot.conversation.utils import (
    key_quest,
    format_text,
    pincode,
    search_vacan,
    format_dict,
    keyboard_add_button,
    get_use_code,
)


def start(update, context):
    # Добавляет пользователя или возвращает
    # данные о нем если он уже есть в базе
    context.user_data.clear()
    user = get_or_create_user(db, update.effective_user, update.message)
    context.user_data["user"] = user
    # Если у пользователя есть словарь с ключом "reg_info"
    # то просит ввести пинкод
    # если такого ключа нету, то просит зарегистрироваться
    if user.get("reg_info", False):
        context.user_data["user_id"] = update.effective_user.id
        context.user_data["reg_info"] = user["reg_info"]
        update.message.reply_text(
            f"Привет\n{context.user_data['reg_info']['user_name']}\nНапишите пинкод",
            reply_markup=keyboard_add_button(["Выход"]),
        )
        return "company_vacan"
    reply_text = "Привет я БОТ для проведения интервью и cначала нам надо познакомиться, нажмите кнопку Регистрация"
    update.message.reply_text(
        reply_text, reply_markup=keyboard_add_button(["Регистрация"])
    )
    return ConversationHandler.END


def company_vacan(update, context):
    context.user_data["pincode"] = update.message.text.strip()
    pincodes = pincode(update.message.text)

    if len(pincodes) == 2:
        # Проверяет использовал этот пинкод пользователь или нет
        # если пинкод уже им был использован, то возвращает в начало
        # если нет, то присылает анкету с вопросами
        if get_use_code(context.user_data["user"], update.message.text):
            update.message.reply_text(
                "Вы уже проходили это", reply_markup=keyboard_add_button(["Выход"])
            )
            return "company_vacan"
        else:
            context.user_data["info"] = info_vacan_in_company(db, pincodes)
            if context.user_data["info"] == None:
                update.message.reply_text(
                    "Ничего не найдено", reply_markup=keyboard_add_button(["Выход"])
                )
                return "company_vacan"
            # Создание словарей с нужными данными в памяти бота для пользователя
            context.user_data["company"] = context.user_data["info"]["company"]
            context.user_data["vacan_list"] = (
                search_vacan(context.user_data["info"]["vacancy"], pincodes[1])
            )[0]
            context.user_data["vacan"] = (
                [key for key in (context.user_data["vacan_list"]).keys()]
            )[0]
            context.user_data["answer"] = dict()
            context.user_data["question"] = context.user_data["vacan_list"][
                context.user_data["vacan"]
            ]
            context.user_data["num"] = key_quest(context.user_data["question"])
            update.message.reply_text(
                format_text(context.user_data["question"], context.user_data["num"][0]),
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardRemove(),
            )
            return "quest"
    update.message.reply_text(
        "Неверный формат пинкода", reply_markup=keyboard_add_button(["Выход"])
    )
    return "company_vacan"


def quest(update, context):
    context.user_data["answer"][context.user_data["num"][0]] = update.message.text
    context.user_data["num"] = context.user_data["num"][1:]

    if len(context.user_data["num"]) == 0:
        data_good = format_dict(context.user_data)
        update.message.reply_text(
            "Спасибо за ответы", reply_markup=ReplyKeyboardRemove()
        )
        # Создание файла с анкетой и отправка ее на почту
        create_word_file(data_good)
        context.user_data.clear()
        return ConversationHandler.END

    update.message.reply_text(
        format_text(context.user_data["question"], context.user_data["num"][0]),
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove(),
    )
    return "quest"


def end_talk(update, context):
    update.message.reply_text("Вы завершили беседу")
    context.user_data.clear()
    return ConversationHandler.END


def dialogue_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю")
