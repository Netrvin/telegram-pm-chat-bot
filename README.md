# telegram-pm-chat-bot
Telegram 私聊机器人
Telegram Private Message Chat Bot

## 安装

### 安装准备
* 申请Telegram机器人，获取Token
* 一台外面的服务器，安装好Python 2和pip，并运行指令`pip install python-telegram-bot --upgrade`

### 配置
打开`config.json`并配置
```
{
    "Admin": 0,        # 管理员用户ID（数字ID）（可以先不设）
    "Token": "",       # 机器人Token
    "Lang": "zh"       # 语言包名称
}
```
如果在前一步未设置管理员用户ID，第一个对机器人发送`/setadmin`的用户将成为管理员，之后可通过修改`config.json`修改管理员

## 运行
```
python main.py
```

## 使用

### 回复
直接回复机器人转发过来的消息即可回复，支持文字、贴纸、图片、文件、音频和视频

### 查询用户身份
部分转发来的消息不便于查看发送者身份，可以通过回复该消息`/info`查询

### 消息发送提示
向机器人发送指令`/togglenotification`可开启/关闭消息发送提示

效果：
* 对管理员：回复用户后，如无出错则不会提示“已回复”
* 对用户：发送消息后，机器人不会回复“已收到”