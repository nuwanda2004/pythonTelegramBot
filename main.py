from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram.ext import ContextTypes
import asyncio
import telegram
from telegram.ext import CallbackContext, ConversationHandler
from typing import List
import logging
from telegram.ext import Updater


TOKEN = '***'
ADMIN_USER_ID = '***'
users_name = {}
END = 3
WAITING_FOR_NAME, WAITING_FOR_FEEDBACK = range(2)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
FIRST = 4
SECOND = 5
THIRD = 6
FOURTH = 7
THANKS = 8

async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Здравствуйте! Меня зовут ***. Я бот по адаптации и помогу вам разобраться на новом месте работы!')
    await update.message.reply_text('Для того, чтобы начать, пожалуйста, представьтесь. Напишите своё имя.')
    return WAITING_FOR_NAME


async def save_name(update: Update, context: CallbackContext):
    words = update.message.text.split()
    if len(words) == 1:
        name = words[0]
        context.user_data['name'] = name
        await update.message.reply_text(f'Приятно познакомиться, {name}! Теперь я буду обращаться к вам так.')
        await asyncio.create_task(send_workday_reminder(update, context))
        return WAITING_FOR_FEEDBACK
    else:
        return await receive_feedback(update, context)


async def send_workday_reminder(update: Update, context):
    await update.message.reply_text('Напоминаю, что рабочий день начинается в 9:30!')
    await asyncio.sleep(33)
    await send_question_reminder(update, context)

async def send_question_reminder(update: Update, context):
    await update.message.reply_text('Вы можете задать мне вопросы, которые помогут понять в чем состоит работа сотрудника. Вы можете выбрать вопросы из меню.')
    await asyncio.sleep(33)
    await instruction_reminder(update, context)


async def instruction_reminder(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    await update.message.reply_text('Пришло время ознакомиться с корпоративным приложением, оно поможет вам быстрее узнать основные моменты рабочего процесса. Также в нем вы можете в дальнейшем найти важную информацию, свои расчетные листы')
    photo_path = '***'
    message_text = 'Это наше приложение! [Ссылка для скачивания](***)'
    with open(photo_path, 'rb') as photo:
        await context.bot.send_photo(chat_id=chat_id, photo=photo)
    await context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode='Markdown')
    await asyncio.sleep(33)
    await first_congrats(update, context)


async def first_congrats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Поздравляю вас с первым рабочим днём!')
    await asyncio.sleep(33)
    await rules_reminder(update, context)


async def rules_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Напоминаю о прохождении инструктажа по правилам безопасности, по охране труда, по соблюдению правил пожарной безопасности')
    await asyncio.sleep(33)
    await portal_reminder(update, context)


async def portal_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ссылка на вход в портал обучения, инструкция как получить логин и пароль. ***')
    await asyncio.sleep(33)
    await file_reminder(update, context)


async def file_reminder(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    document_path = '***'
    message_text = 'Файл с инструкцией по использованию корпоративного приложения, более подробная информация с расположением разделов и навигацией по использованию.'

    with open(document_path, 'rb') as document:
        await context.bot.send_document(chat_id=chat_id, document=document, caption=message_text, parse_mode='Markdown')

    await asyncio.sleep(33)

    await offer_feedback(update, context)


async def offer_feedback(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Хотите оставить отзыв о работе? Если да, пожалуйста, напишите ваш отзыв в личные сообщения.')
    return WAITING_FOR_FEEDBACK


async def receive_feedback(update: Update, context: CallbackContext):
    feedback = update.message.text
    await context.bot.send_message(chat_id=ADMIN_USER_ID, text=f'Новый отзыв:\n\n{feedback}')
    await update.message.reply_text('Спасибо за ваш отзыв! Он был отправлен администратору.')
    await asyncio.sleep(33)
    await meds_reminder(update, context)
    return ConversationHandler.END


async def cancel_feedback(update: Update, context: CallbackContext):
    await update.message.reply_text('Отзыв не был оставлен.')
    return ConversationHandler.END



async def meds_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text('Предоставляется возможность прохождения бесплатного медицинского осмотра для получения мед книжки, адреса стоит уточнить у наставника')
    await asyncio.sleep(33)
    await this_days_reminder(update, context)



async def this_days_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text('Я надеюсь, что ваши первые дни на новой работе проходят гладко. В случае возникновения проблем, не стесняйтесь обращаться за помощью к куратору по адресу: @***')
    await asyncio.sleep(33)
    await training_reminder(update, context)


async def training_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text('Надеюсь, что вы активно осваиваете обучающие материалы и уверенно усваиваете новую информацию. Если у вас возникают трудности, ваш куратор готов помочь  @***')
    await asyncio.sleep(33)
    await collegue_reminder(update, context)

# Исправьте collegue_reminder аналогично, если она использует update.message


async def collegue_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text('Мы надеемся, что вы успешно налаживаете контакты с коллегами. При возникновении каких-либо затруднений, пожалуйста, свяжитесь с куратором:  @***')
    await asyncio.sleep(33)
    await first_month_reminder(update, context)

async def first_month_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text('Поздравляю с завершением первого рабочего месяца! Желаю успехов!')
    await asyncio.sleep(33)
    await second_month_reminder(update, context)

async def second_month_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text("Поздравляю с завершением второго рабочего месяца, надеюсь, у вас всё хорошо и вы прошли всё обучение на образовательном портале!")





async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('У вас возникли какие-то трудности и не работает бот? \nСообщение о случившемся сейчас будет передано администратору, проблема будет решена в ближайшее время')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Совокупность практики и теоретических знаний: стажерские курсы, прохождение онлайн тренингов на портале обучения, очные тренинги.')


async def custom1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Компания Такая-то - занимается тем-то. - Качественная продукция - Удовлетворение потребностей клиентов - Профессионализм сотрудников - Инновации и развитие")


async def custom2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Необходимо узнать о наставнике, обратиться к руководителю с основными вопросами')


async def custom3_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Помимо устной речи в компании используются различные каналы коммуникации, такие как: электронная почта, внутренний телефон, внутренние чаты, корпоративные встречи и брифинги.')


async def custom4_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1. Финансовые стимулы. 2. Карьерное развитие.')

async def custom5_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("1. Упрощение системы адаптации новых сотрудников \n2. Ознакомление с основной информацией о компании \n3. Предоставлнние информации в адаптационный период \n4. Система напоминаний позволяет не забыть о важных задачах")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Update %s caused error %s', update, context.error)


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_file_reminder', file_reminder)],
        states={WAITING_FOR_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_feedback)]},
        fallbacks=[CommandHandler('cancel', cancel_feedback)]
    )


    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('first_question', custom_command))
    app.add_handler(CommandHandler('second_question', custom1_command))
    app.add_handler(CommandHandler('third_question', custom2_command))
    app.add_handler(CommandHandler('fourth_question', custom3_command))
    app.add_handler(CommandHandler('fifth_question', custom4_command))
    app.add_handler(CommandHandler('for_what_bot', custom5_command))

    app.add_handler(CommandHandler('feedback', file_reminder))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_name))

    app.add_error_handler(error)



    print('Polling...')
    app.run_polling(poll_interval=5)
