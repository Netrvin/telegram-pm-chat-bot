# telegram-pm-chat-bot

这是一个允许用户在 Telegram 上与你私聊的机器人。它易于安装并且可以根据你的需求进行自定义。

**注意**: 此项目目前正在开发者空闲时间内更新。如果你不介意使用
.NET，你可能希望考虑使用 [pmcenter](https://github.com/Elepover/pmcenter)

## 安装

### 安装准备

* 创建一个 Telegram 机器人并获取其 Token
* 安装 Python 和 pip
* 使用 pip 安装 python-telegram-bot==13.15

### 配置

打开`config.json`并配置

- admin: 管理员 ID
- token: 机器人 Token
- lang: 语言包名称（注意: 应为`en`或`zh_cn`或`zh_cn_moe`）

初始值

```json
{
  "Admin": 0,
  "Token": "",
  "Lang": "zh_cn"
}
```

示例

```json
{
  "admin": 5021485638,
  "token": "5775925834:AAHDw2Pt-7TeLEY4c6PjtJnbHiR4N1q8Dmk",
  "lang": "zh_cn"
}
```

如果在前一步未设置管理员用户ID，第一个对机器人发送`/setadmin`的用户将成为管理员，之后可通过修改`config.json`修改管理员

## 运行机器人

在项目目录下执行以下命令即可运行机器人

```
python main.py
```

## 使用

### 回复

直接回复机器人转发过来的消息即可回复，支持文字、贴纸、图片、文件、音频和视频

### 查询用户身份

部分转发来的消息不便于查看发送者身份，可以通过回复该消息`/info`查询

### 消息发送提示

向机器人发送指令`/notification`可开启或关闭消息发送提示

效果：

* 对管理员：回复用户后，如无出错则不会提示“已回复”
* 对用户：发送消息后，机器人不会回复“已收到”

### 封禁与解禁

向一条消息回复`/ban`可禁止其发送者再次发送消息

向一条消息回复`/unban`或发送`/unban <用户 ID>`可解除对此用户的封禁

## 可用指令

| Command        | 用途           |
|:---------------|:-------------|
| /start         | 开始使用机器人      |
| /help          | 显示帮助信息       |
| /ping          | 确认机器人是否正在运行  |
| /setadmin      | 设置当前用户为管理员   |
| /notification  | 切换消息发送提示开启状态 |
| /info          | 查询用户身份       |
| /ban           | 封禁用户         |
| /unban <用户 ID> | 解封用户         |
