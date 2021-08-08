from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
import os

TOKEN = os.environ.get('TOKEN')

def manage_hooks(d):
    if d['status'] == "finished":
        global video_name
        video_name = d['filename']

ydl_opts = {
    'progress_hooks': [manage_hooks],
}

# commands
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def download_yt(update, context):
    url = update.message.text
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    send_video_to_user(update, context)

def send_video_to_user(update, context):
    chat_id = update.effective_chat.id
    with open(video_name, 'rb') as video:
        context.bot.send_video(
            chat_id=chat_id,
            video=video,
         #   repply_to_message_id=update.message.id
        )

# main func
def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # handlers
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & (~Filters.command), download_yt)

    # add handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    # start
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
