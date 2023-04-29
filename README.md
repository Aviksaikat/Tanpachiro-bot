# Tanpachiro Bot 🤖🎥

![](media/banner_tanpachiro.png)

`Tanpachiro Bot` is a Telegram bot that can upload video files to a chat. It can also upload all the videos in a specified directory. With some slight modifications, you can make it upload as you want. With a [local bot API](https://github.com/tdlib/telegram-bot-api) server you can also make it support files upto 2GB in size.


# Working Demo 💻📱
https://user-images.githubusercontent.com/31238298/235325725-c2159cfe-399a-4139-9e5e-e40b2a9402f5.mp4


# Getting Started 🚀
1. Clone the repository.
2. Install the required packages:
```sh
git clone https://github.com/Aviksaikat/Tanpachiro-bot
cd Tanpachiro-bot
pip install -r requirements.txt
```

3. Create a `config.toml` file in the root directory of the project and add your Telegram bot token:

```toml
[telegram]
bot_token = "YOUR_BOT_TOKEN"
```

## Additional 
- Install [Telegram Bot API server](https://github.com/tdlib/telegram-bot-api) to increase the uplaod file size upto 2GB. Default is around `60 MB` which is useless. Check out the github page for instructions.


4. Run the bot: 
```py
python bot.py
```

# Commands 📝
- **/start**: Start the bot and get a welcome message.
- **/dir** <directory_name>: Upload all the video files in the specified directory.

# Usage 🎬
1. Send a video file to the bot to upload it to the chat.
2. Use the `/dir` command followed by the directory name to upload all the video files in that directory.

# Contributing 🤝
Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: 

`git checkout -b new-branch-name`

3. Make your changes and commit them: 

`git commit -m "Description of your changes"`

4. Push your changes to your fork: 

`git push origin new-branch-name`

5. Create a pull request.

## TODO

- [x] Recursively get all the video files
- [ ] Add for uploading in groups & channels
- [ ] Add more options


# Issues 🐛
If you find any bugs or issues with the bot, please report them on the Issues page of the repository.

# License 📜
This project is licensed under the MIT License.
