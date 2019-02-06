# telegram-pm-chat-bot

Telegram 私聊机器人
Telegram Private Message Chat Bot

**本项目已进入随缘更新状态，如您对使用 `.NET` 没有意见的话，可考虑使用 [pmcenter](https://github.com/Elepover/pmcenter) 作为PM机器人的解决方案**

## 安装 (Installation)

### 安装准备 (Preparation)
* 创建Telegram机器人，获取Token
* 一台外面的服务器，安装好Python和pip，并用pip安装`python-telegram-bot`

* Create a bot and get its token
* Install Python and pip, then use pip to install `python-telegram-bot`

### 配置 (Configuration)
打开`config.json`并配置
```json
{
    "Admin": 0,
    "//1": "管理员用户ID（数字ID）（可以先不设）",
    "Token": "",
    "//2": "机器人Token",
    "Lang": "zh",
    "//3": "语言包名称"
}
```
如果在前一步未设置管理员用户ID，第一个对机器人发送`/setadmin`的用户将成为管理员，之后可通过修改`config.json`修改管理员

Open `config.json` and configure
```json
{
    "Admin": 0,
    "//1": "Admin ID (A digital ID)",
    "Token": "",
    "//2": "Bot Token",
    "Lang": "en",
    "//3": "Language Pack Name (Be careful! It's 'en'!)"
}
```
If you didn't set admin's ID previously, the user who sends `/setadmin` to the bot first will become the admin. You can edit `config.json` to change admin later.

## 升级 (Upgrade)
替换`main.py`和`lang`文件夹，重新运行即可

Replace `main.py` and folder `lang`, then run `main.py`

## 运行 (Run)
```
python main.py
```

## 使用 (Usage)

### 回复 (Reply)
直接回复机器人转发过来的消息即可回复，支持文字、贴纸、图片、文件、音频和视频

Reply directly to the message forwarded by the robot to reply. You can reply text, sticker, photo, file, audio, voice and video.

### 查询用户身份 (Inquire sender identity)
部分转发来的消息不便于查看发送者身份，可以通过回复该消息`/info`查询

You can reply `/info` to the message which you want to get its sender's info more clearly.

### 消息发送提示 (Message sending notification)
向机器人发送指令`/togglenotification`可开启/关闭消息发送提示

效果：
* 对管理员：回复用户后，如无出错则不会提示“已回复”
* 对用户：发送消息后，机器人不会回复“已收到”

Send the command `/togglenotification` to the bot to enable/disable the message sending notification

Effect:
* For admin: After replying to the user, if there is no error, it will not prompt "replied"
* For users: After sending a message, the bot will not reply "received"

### 封禁与解禁 (Ban and unban)
向一条消息回复`/ban`可禁止其发送者再次发送消息

向一条消息回复`/unban`或发送`/unban <数字ID>`可解除对此用户的封禁

Reply `/ban` to a message to block the sender of the message from sending messages to you

Reply `unban` to a message or send `/unban <User ID>` to unban a user

## 可用指令 (Available commands)
| Command                   | 用途                   |
| :---                      | :---                   |
| /ping                     | 确认机器人是否正在运行   |
| /setadmin                 | 设置当前用户为管理员     |
| /togglenotification       | 切换消息发送提示开启状态 |
| /info                     | 查询用户身份            |
| /ban                      | 封禁用户                |
| /unban <数字ID (可选)>     | 解封用户                |

| Command                | Usage                                      |
| :---                   | :---                                       |
| /ping                  | Check if the bot is running                |
| /setadmin              | Set the current user as admin              |
| /togglenotification    | Toggle message sending notification status |
| /info                  | Inquire sender identity                    |
| /ban                   | Ban a user                                 |
| /unban <ID (optional)> | Unban a user                               |
