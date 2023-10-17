#!/usr/bin/python3
import os
import re
from time import sleep

import toml
from telegram import Bot, ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

# Load bot token from the TOML file
with open("config.toml", "r") as f:
    config = toml.load(f)
bot_token = config["telegram"]["bot_token"]

# Initialize the Telegram bot with python-telegram-bot
bot = Bot(token=bot_token, base_url="http://localhost:8081/bot")
updater = Updater(bot=bot, use_context=True)


def extract_episode_number(file_name):
    match = re.search(r"E(\d+)", file_name)
    if match:
        return int(match.group(1))
    return 0


print_list = lambda lst: print(*lst, sep=", ")

# Define a function to handle the "/start" command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi! I'm a bot that can upload video files. Just send me a video file and I'll do the rest."
    )


# Define a function to handle the video file upload
def handle_video_upload(update: Update, context: CallbackContext):
    # Get the video file ID from the message
    video_file_id = update.message.video.file_id
    # Download the video file to the local storage
    file_path = f"{update.message.video.file_id}.mp4"
    bot.get_file(video_file_id).download(file_path)
    # Send the video file back to the chat
    update.message.reply_document(open(file_path, "rb"))
    # Send a confirmation message
    update.message.reply_text("Video uploaded successfully!")


# Define a function to handle errors
def error_handler(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


# Define a function to handle the directory upload
def handle_directory_upload(update: Update, context: CallbackContext):
    undone = []
    # Get the directory name from the message
    directory_name = "".join(update.message.text.split()[1:])
    # Check if the directory exists
    if not os.path.exists(directory_name):
        update.message.reply_text("Directory not found!")
        return
    update.message.reply_text("Please wait uplaoding the files....")
    # Get the list of video files in the directory
    video_files = []
    for root, dirs, files in os.walk(directory_name):
        for file in files:
            if file.endswith(".mp4"):
                video_files.append(os.path.join(root, file))
    # print(video_files)

    sorted_episode_list = sorted(
        video_files, key=lambda file: extract_episode_number(file)
    )

    # Upload each video file in the directory
    for video_file in sorted_episode_list:
        print(f"Uploading: {video_file}")
        # abs_path = directory_name + video_file
        # Send the video file to the chat
        with open(video_file, "rb") as f:
            try:
                update.message.reply_document(
                    document=f,
                    caption=video_file.replace(
                        "/home/avik/Downloads/torrents/FamilyGuyFull/", ""
                    ),
                )
                # sleep(1)
            except:
                try:
                    update.message.reply_document(
                        document=f,
                        caption=video_file.replace(
                            "/home/avik/Downloads/torrents/FamilyGuyFull/", ""
                        ),
                    )
                except:
                    undone.append(video_file)
                    continue
        # Send a confirmation message
        # update.message.reply_text(f"Video '{video_file}' uploaded successfully!")
        if undone:
            try:
                update.message.reply_document(
                    document=f,
                    caption=video_file.replace(
                        "/home/avik/Downloads/torrents/FamilyGuyFull/", ""
                    ),
                )
            except:
                undone.append(video_file)
                continue

    update.message.reply_text(f"These are undone: {print_list(undone)}")


# Set up the event handlers and start the bot
def main():
    print("Bot Started!")
    # Add handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.video, handle_video_upload))
    updater.dispatcher.add_handler(
        CommandHandler("dir", handle_directory_upload, pass_args=True)
    )
    updater.dispatcher.add_error_handler(error_handler)
    # Start the bot
    updater.start_polling()
    updater.idle()


# Run the bot
if __name__ == "__main__":
    main()
