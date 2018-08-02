# telegram-pm-chat-bot
Telegram 私聊机器人
Telegram Private Message Chat Bot

## 安装 (Installation)

### 安装准备 (Preparation)
* 创建Telegram机器人，获取Token
* 一台外面的服务器，安装好Python 2和pip，并运行指令`pip install python-telegram-bot --upgrade`

* Create a bot and get its token
* Install Python 2 and pip, then run command `pip install python-telegram-bot --upgrade`

### 配置 (Configuration)
打开`config.json`并配置
```json
{
    "Admin": 0,        // 管理员用户ID（数字ID）（可以先不设）
    "Token": "",       // 机器人Token
    "Lang": "zh"       // 语言包名称
}
```
如果在前一步未设置管理员用户ID，第一个对机器人发送`/setadmin`的用户将成为管理员，之后可通过修改`config.json`修改管理员

Open `config.json` and configure
```json
{
    "Admin": 0,        // Admin ID (A digital ID)
    "Token": "",       // Bot Token
    "Lang": "en"       // Language Pack Name (Be careful! It's "en"!)
}
```
If you didn't set admin's ID previously, the user who sends `/setadmin` to the bot firstly will become the admin. You can edit `config.json` to change admin later.

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

## 可用指令 (Available commands)
| Command             | 用途                   |
| :---                | :---                   |
| /ping               | 确认机器人是否正在运行   |
| /setadmin           | 设置当前用户为管理员     |
| /togglenotification | 切换消息发送提示开启状态 |
| /info               | 查询用户身份            |

| Command             | Usage                                      |
| :---                | :---                                       |
| /ping               | Check if the bot is running                |
| /setadmin           | Set the current user as admin              |
| /togglenotification | Toggle message sending notification status |
| /info               | Inquire sender identity                    |