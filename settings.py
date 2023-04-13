import json
import logging
import os
import threading

import requests

VERSION = 'v2.0'

# Set path to the current file's directory
PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

# Load configuration file
CONFIG = json.loads(open(PATH + 'data/' + 'config.json', 'r').read())

# Load language file
LANG = json.loads(open(PATH + 'lang/' + CONFIG['lang'] + '.json', encoding='utf-8').read())

# Define locks for thread-safe access to message and preference lists
message_lock = threading.Lock()
preference_lock = threading.Lock()

# Load message data
message_list = json.loads(open(PATH + 'data/' + 'data.json', 'r').read())

# Load user profiles and settings
preference_list = json.loads(open(PATH + 'data/' + 'preference.json', 'r').read())


def save_data():
    """
    Save message data to file in a thread-safe manner
    """
    with message_lock:
        with open(PATH + 'data/' + 'data.json', 'w') as f:
            json.dump(message_list, f)


def save_preference():
    """
    Save user profiles and settings to file in a thread-safe manner
    """
    with preference_lock:
        with open(PATH + 'data/' + 'preference.json', 'w') as f:
            json.dump(preference_list, f)


def save_config():
    """
    Save configuration to file
    """
    with open(PATH + 'data/' + 'config.json', 'w') as f:
        json.dump(CONFIG, f, indent=4)


def init_user(user):
    """
    Initialize user profile if this is the first time the user is using the bot.
    Update user nickname if it has changed.
    """
    global preference_list
    if str(user.id) not in preference_list:
        preference_list[str(user.id)] = {}
        preference_list[str(user.id)]['notification'] = False
        preference_list[str(user.id)]['blocked'] = False
        preference_list[str(user.id)]['name'] = user.full_name
        threading.Thread(target=save_preference).start()
        return

    if 'blocked' not in preference_list[str(user.id)]:
        preference_list[str(user.id)]['blocked'] = False

    if preference_list[str(user.id)]['name'] != user.full_name:
        preference_list[str(user.id)]['name'] = user.full_name
        threading.Thread(target=save_preference).start()


def setup_logging():
    """
    Set up logging configuration
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_commands():
    """
    Set up bot commands
    """
    commands = [
        {'command': 'start', 'description': 'Start the bot'},
        {'command': 'help', 'description': 'Show help information'},
        {'command': 'ping', 'description': 'Check if the bot is alive'},
        {'command': 'setadmin', 'description': 'Set the bot admin'},
        {'command': 'notification', 'description': 'Toggle notification'},
        {'command': 'info', 'description': 'Show sender information'},
        {'command': 'ban', 'description': 'Ban a user'},
        {'command': 'unban', 'description': 'Unban a user'}
    ]

    data = {'commands': commands}
    url = f"https://api.telegram.org/bot{CONFIG['token']}/setMyCommands"
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print('Commands set successfully')
    else:
        print('Failed to set commands:', response.text)
