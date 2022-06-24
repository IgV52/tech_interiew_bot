from telegram.ext import ConversationHandler
from bot.addons.format_add_blank_user import create_word_file
from bot.database.db import db, user_profile, user_info, info_vacan_in_company
from telegram import ParseMode, ReplyKeyboardRemove
from bot.conversation.utils import key_quest, format_text, pincode, search_vacan, format_dict, keyboard_add_button

def start(update, context):
    info = user_info(db,update.effective_user.id)
    if info[0]:
        context.user_data['user_id'] = update.effective_user.id
        context.user_data['user_name'] = info[1]['reg_info']['user_name']
        context.user_data['number_phone'] = info[1]['reg_info']['number_phone']
        update.message.reply_text(
        f"Привет\n{context.user_data['user_name']}\nНапишите пинкод",
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
    if user_profile(db,update.effective_user.id, msg):
        update.message.reply_text("Вы уже проходили это",
        reply_markup=keyboard_add_button(['Выход']))
        return 'company_vacan'
    else:
        user_data['info'] = info_vacan_in_company(db, pincodes)
        if user_data['info'] == None:
            update.message.reply_text("Ничего не найдено",
        reply_markup=keyboard_add_button(['Выход']))
            return 'company_vacan'
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
            create_word_file(data_good)
            return ConversationHandler.END
        reply_text(format_text(question,user_data['num'][0]), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        return 'quest'

def end_talk(update, context):
    update.message.reply_text('Вы завершили беседу')
    return ConversationHandler.END

def dialogue_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю")