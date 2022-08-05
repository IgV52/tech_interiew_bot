from telegram.ext import ConversationHandler
from bot.addons.format_add_blank_user import create_word_file
from bot.database.db import db, info_vacan_in_company, get_or_create_user
from telegram import ParseMode, ReplyKeyboardRemove
from bot.conversation.utils import key_quest, format_text, pincode, search_vacan, format_dict, keyboard_add_button, get_use_code

def start(update, context):
    #Добавляет пользователя или возврвщает
    #данные о нем если он уже есть в базе
    user = get_or_create_user(db,update.effective_user, update.message)
    context.user_data['user'] = user
    #Если у пользователя есть словарь с ключом "reg_info"
    #то просит ввести пинкод
    #если такого ключа нету, то просит зарегистрироваться
    if user.get('reg_info', False):
        context.user_data['user_id'] = update.effective_user.id
        context.user_data['reg_info'] = user['reg_info']
        update.message.reply_text(
        f"Привет\n{context.user_data['reg_info']['user_name']}\nНапишите пинкод",
        reply_markup=keyboard_add_button(['Выход']))
        return 'company_vacan'
    reply_text = "Привет я БОТ для проведения интервью и cначала нам надо познакомиться, нажмите кнопку Регистрация"
    update.message.reply_text(reply_text, reply_markup=keyboard_add_button(['Регистрация']))
    return ConversationHandler.END

def company_vacan(update, context):
    user_data = context.user_data
    msg = update.message.text
    user_data['pincode'] = msg.strip()
    pincodes = pincode(msg)
    #Проверяет использовал этот пинкод пользователь или нет
    #если пинкод уже им был использован, то возвращает в начало
    #если нет, то присылает анкету с вопросами
    if get_use_code(context.user_data['user'], msg):
        update.message.reply_text("Вы уже проходили это",
        reply_markup=keyboard_add_button(['Выход']))
        return 'company_vacan'
    else:
        user_data['info'] = info_vacan_in_company(db, pincodes)
        if user_data['info'] == None:
            update.message.reply_text("Ничего не найдено",
        reply_markup=keyboard_add_button(['Выход']))
            return 'company_vacan'
        #Создание словарей с нужными данными в памяти бота для пользователя
        user_data['company'] = user_data['info']['company']
        user_data['vacan_list'] = (search_vacan(user_data['info']['vacancy'], pincodes[1]))[0]
        user_data['vacan'] = ([key for key in (user_data['vacan_list']).keys()])[0]
        user_data['answer'] = dict()
        user_data['start'] = ['start']
        user_data['question'] = user_data['vacan_list'][user_data['vacan']]
        user_data['num'] = key_quest(user_data['question'])
        update.message.reply_text(f"Информация о правилах опроса, если вы готовы отправте боту любое сообщение",
        reply_markup=ReplyKeyboardRemove())
        return 'quest'

def quest(update, context):
    user_data = context.user_data
    question = user_data['question']
    msg = update.message.text
    reply_text = update.message.reply_text
    if 'start' in user_data:
        del user_data['start']
        reply_text(format_text(question,user_data['num'][0]), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        return 'quest'
    else:
        user_data['answer'][user_data['num'][0]] = msg
        del user_data['num'][0]
        if not user_data['num']:
            data_good = format_dict(user_data)
            reply_text("Спасибо за ответы", reply_markup=ReplyKeyboardRemove())
            #Создание файла с анкетой и отправка ее на почту
            create_word_file(data_good)
            return ConversationHandler.END
        reply_text(format_text(question,user_data['num'][0]), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        return 'quest'

def end_talk(update, context):
    update.message.reply_text('Вы завершили беседу')
    return ConversationHandler.END

def dialogue_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю")