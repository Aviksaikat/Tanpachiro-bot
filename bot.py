import asyncio
import os

import toml
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Load bot token from the TOML file
with open("config.toml", "r") as f:
    config = toml.load(f)
bot_token = config["telegram"]["bot_token"]

# Initialize the Telegram bot with aiogram
bot = Bot(token=bot_token, base_url="http://localhost:8081")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define a function to handle the "/start" command
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Hi! I'm a bot that can upload video files. Just send me a video file and I'll do the rest."
    )


# Define a function to handle the video file upload
@dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def handle_video_upload(message: types.Message):
    # Get the video file ID from the message
    video_file_id = message.video.file_id
    # Download the video file to the local storage
    file_path = f"{message.video.file_id}.mp4"
    await bot.download_file_by_id(video_file_id, file_path)
    # Send the video file back to the chat
    await bot.send_video(message.chat.id, video=open(file_path, "rb"))
    # Send a confirmation message
    await message.reply("Video uploaded successfully!")


# Define a function to handle errors
async def error_handler(update, exception):
    print(f"Update {update} caused error {exception}")


# Define a function to handle the directory upload
@dp.message_handler(commands=["dir"], content_types=types.ContentTypes.TEXT)
async def handle_directory_upload(message: types.Message):
    # Get the directory name from the message
    directory_name = "".join(message.text.split()[1:])
    # print(directory_name)

    # Check if the directory exists
    if not os.path.exists(directory_name):
        await message.reply("Directory not found!")
        return
    # Get the list of video files in the directory
    video_files = [
        f
        for f in os.listdir(directory_name)
        if os.path.isfile(os.path.join(directory_name, f)) and f.endswith(".mp4")
    ]
    # Upload each video file in the directory
    print(video_files)
    for video_file in video_files:
        print(f"Uploading: {video_file}")
        # Send the video file to the chat
        await bot.send_video(message.chat.id, video=video_file_id, caption=video_file)
        # Send a confirmation message
        await message.reply(f"Video '{video_file}' uploaded successfully!")


# Set up the event loop and start the bot
async def main():
    print("Bot Started!")
    # Start the bot
    await dp.start_polling()


# Run the bot
asyncio.run(main())
