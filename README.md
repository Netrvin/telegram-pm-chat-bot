# telegram-pm-chat-bot

English | [简体中文](/README_CN.md)

This is a chatbot that allows users to have private conversations with you on Telegram. It is easy to set up and can be
customized to suit your needs.

**Note**: This project is currently being updated in the developer's free time. If you do not mind using .NET, you may
want to consider using [pmcenter](https://github.com/Elepover/pmcenter) instead.

## Installation

### Preparation

* Create a Telegram bot and get its token
* Install Python and pip
* Use pip to install `python-telegram-bot==13.15`, `requests`

### Configuration

Open `config.json` and configure

- admin: admin ID (a numeric ID)
- token: bot token
- lang: language pack name (be careful, it should be 'en' or 'zh_cn' or 'zh_cn_moe')

Initial value

```json
{
  "admin": 0,
  "token": "",
  "lang": "en"
}
```

Example

```json
{
  "admin": 5021485638,
  "token": "5775925834:AAHDw2Pt-7TeLEY4c6PjtJnbHiR4N1q8Dmk",
  "lang": "en"
}
```

If you didn't set admin's ID previously, the user who sends `/setadmin` to the bot first will become the admin. You can
edit `config.json` to change admin later.

## Run The Bot

Run the bot by executing the following command in the project directory

```
python main.py
```

## Usage

### Reply to bot a message

Reply directly to the message forwarded by the robot to reply. You can reply text, sticker, photo, file, audio, voice
and video.

### Inquire sender identity

You can reply `/info` to the message which you want to get its sender's info more clearly.

### Message sending notification

Send the command `/notification` to the bot to enable or disable the message sending notification

Effect:

* For admin: After replying to the user, if there is no error, it will not prompt "replied"
* For users: After sending a message, the bot will not reply "received"

### Ban and unban

Reply `/ban` to a message to block the sender of the message from sending messages to you

Reply `/unban` to a message or send `/unban <User ID>` to unban a user

## Available commands

| Command           | Usage                                      |
|:------------------|:-------------------------------------------|
| /start            | Start the bot                              |
| /help             | Show help message                          |
| /ping             | Check if the bot is running                |
| /setadmin         | Set the current user as admin              |
| /notification     | Toggle message sending notification status |
| /info             | Inquire sender identity                    |
| /ban              | Ban a user                                 |
| /unban \<User ID> | Unban a user                               |
