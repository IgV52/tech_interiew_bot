from telegram.ext import ConversationHandler
from bot.database.db import db, get_or_create_user, reg_user
from telegram import ParseMode
from bot.conversation.utils import get_date, get_city, check_phone, keyboard_add_button

def reg(update, context):
    user = get_or_create_user(db,update.effective_user, update.message)
    if user.get('reg_info', False):
        return ConversationHandler.END
    update.message.reply_text("""Пожалуйста введите <b>ФИО</b>""", parse_mode = ParseMode.HTML)
    return 'fio'

def fio(update, context):
    if len(update.message.text.split()) < 3:
        update.message.reply_text("""Пожалуйста введите <b>ФИО</b>""", parse_mode = ParseMode.HTML)
        return 'fio'
    else:
        context.user_data['user_name'] = update.message.text
        update.message.reply_text(
            """Введите дату вашего рождения в формате <b>дд.мм.гггг</b>""", parse_mode = ParseMode.HTML)
        return 'birth_date'

def birth_date(update, context):
    date = get_date(update.message.text)
    if not date:
        update.message.reply_text(
            """Введите дату вашего рождения в формате <b>дд.мм.гггг</b>""", parse_mode = ParseMode.HTML)
        return "birth_date"
    else:
        context.user_data['birth_date'] = update.message.text
        update.message.reply_text(
            """<b>Из какого вы города?</b>""", parse_mode = ParseMode.HTML)
        return 'location'

def location(update, context):
    city = get_city(update.message.text)
    context.user_data['location'] = update.message.text
    if not city:
        update.message.reply_text(
            """<b>Готовы ли вы переехать в Москву?</b>""",
        reply_markup=keyboard_add_button(['Да', 'Нет']), parse_mode = ParseMode.HTML)
        return 'new_location'
    else:
        update.message.reply_text(
            """<b>Какой формат работы вы рассматриваете?</b>""",
        reply_markup=keyboard_add_button(['Удаленка', 'Офис', 'Гибрид(удаленка+офис)']),
        parse_mode = ParseMode.HTML)
        return 'format_job'

def new_location(update, context):
    context.user_data['relocation'] = update.message.text.lower()
    answer = ('да', 'нет')
    if context.user_data['relocation'] not in answer:
        update.message.reply_text(
                """Скажите <b>Да</b> или <b>Нет</b>""",
            reply_markup=keyboard_add_button(['Да', 'Нет']), parse_mode = ParseMode.HTML)
        return 'new_location'
    else:
        update.message.reply_text(
            """<b>Какой формат работы вы рассматриваете?</b>""",
        reply_markup=keyboard_add_button(['Удаленка', 'Офис', 'Гибрид(удаленка+офис)']),
        parse_mode = ParseMode.HTML)
        return 'format_job'

def format_job(update, context):
    context.user_data['format_job'] = update.message.text
    variable = ('Удаленка', 'Офис', 'Гибрид(удаленка+офис)')
    if update.message.text not in variable:
        update.message.reply_text(
            """<b>Нажмите доступную кнопку</b>""",
        reply_markup=keyboard_add_button(['Удаленка', 'Офис', 'Гибрид(удаленка+офис)']),
        parse_mode = ParseMode.HTML)
        return 'format_job'
    else:
        update.message.reply_text(
            """Рассматриваемый уровень зарплаты: <b>минимум - комфорт</b>""", parse_mode = ParseMode.HTML)
        return 'salary'

def salary(update, context):
    context.user_data['salary'] = update.message.text
    update.message.reply_text(
            """Напишите свой номер телефона в формате <b>+7</b>""", parse_mode = ParseMode.HTML)
    return 'number_phone'

def number_phone(update, context):
    user_phone = update.message.text
    check = check_phone(user_phone)
    if not check:
        update.message.reply_text("""<b>Неправильно набран номер</b>""", parse_mode = ParseMode.HTML)
        return 'number_phone'
    else:
        context.user_data['number_phone'] = update.message.text
        context.user_data['user_id'] = update.effective_user.id
        data_user = context.user_data
        reg_user(db,data_user)
        update.message.reply_text("""<b>Все ответы записаны, можем начать</b>""",
        reply_markup=keyboard_add_button(['/start']),
        parse_mode = ParseMode.HTML)
        return ConversationHandler.END

def dialogue_dontknow(update, context):
    update.message.reply_text("""<b>Я вас не понимаю</b>""", parse_mode = ParseMode.HTML)
