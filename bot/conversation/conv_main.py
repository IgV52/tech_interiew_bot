from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from bot.conversation.conv_reg import (
    format_job,
    number_phone,
    fio,
    birth_date,
    location,
    new_location,
    reg,
    salary,
    end,
    personal_info,
)
from bot.conversation.conv_talk import (
    company_vacan,
    start,
    dialogue_dontknow,
    quest,
    end_talk,
)

conv_talk = ConversationHandler(
    conversation_timeout=50 * 60,
    entry_points=[CommandHandler("start", start)],
    states={
        "company_vacan": [
            MessageHandler(Filters.regex("^(Выход)$"), end_talk),
            MessageHandler(Filters.text, company_vacan),
        ],
        "quest": [MessageHandler(Filters.text, quest)],
    },
    fallbacks=[
        MessageHandler(
            Filters.video | Filters.photo | Filters.document | Filters.location,
            dialogue_dontknow,
        )
    ],
)

conv_reg = ConversationHandler(
    conversation_timeout=20 * 60,
    entry_points=[
        MessageHandler(Filters.regex("^(Регистрация)$"), reg),
        CommandHandler("reg", reg),
    ],
    states={
        "personal_info": [
            MessageHandler(Filters.text, personal_info),
            CallbackQueryHandler(personal_info, pattern="^yes$"),
        ],
        "fio": [MessageHandler(Filters.text, fio)],
        "birth_date": [MessageHandler(Filters.text, birth_date)],
        "location": [MessageHandler(Filters.text, location)],
        "new_location": [
            MessageHandler(Filters.text, new_location),
            CallbackQueryHandler(new_location, pattern="^(yes_rel|no_rel)$"),
        ],
        "format_job": [
            MessageHandler(Filters.text, format_job),
            CallbackQueryHandler(format_job, pattern="^(online|office|online_office)$"),
        ],
        "salary": [MessageHandler(Filters.text, salary)],
        "number_phone": [MessageHandler(Filters.text, number_phone)],
    },
    fallbacks=[
        MessageHandler(
            Filters.video | Filters.photo | Filters.document | Filters.location,
            dialogue_dontknow,
        ),
        CallbackQueryHandler(end, pattern="^stop$"),
    ],
)
