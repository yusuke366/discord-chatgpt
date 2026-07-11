import os

import discord
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

PERSONA_SAVE_FILE = "channel_personas.json"

chance_for_all = 0.2
PERSONA_FILES = {
    "全員": [
        {
            "name": "みさき",
            "file": "misaki.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/misaki.png",
            "chance": chance_for_all
        },
        {
            "name": "あや",
            "file": "aya.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/aya.png",
            "chance": chance_for_all
        },
        {
            "name": "りん",
            "file": "rin.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/rin.png",
            "chance": chance_for_all
        },
        {
            "name": "ゆい",
            "file": "yui.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/yui.png",
            "chance": chance_for_all
        },
        {
            "name": "なぎさ",
            "file": "nagisa.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/nagisa.png",
            "chance": chance_for_all
        },
        {
            "name": "ことね",
            "file": "kotone.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/kotone.png",
            "chance": chance_for_all
        },
        {
            "name": "はる",
            "file": "haru.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/haru.png",
            "chance": chance_for_all
        },
        {
            "name": "かなで",
            "file": "kanade.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/kanade.png",
            "chance": chance_for_all
        },
        {
            "name": "めぐ",
            "file": "megu.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/megu.png",
            "chance": chance_for_all
        },
        {
            "name": "みお",
            "file": "mio.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/mio.png",
            "chance": chance_for_all
        }
    ],
    "アシスタント": [
        {
            "name": "あや",
            "file": "assistant.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/aya.png",
            "chance": 1.0
        }
    ],
    "ソフトウェアエンジニア": [
        {
            "name": "りん",
            "file": "engineer.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/rin.png",
            "chance": 1.0
        }
    ],
    "みさき": [
        {
            "name": "みさき",
            "file": "misaki.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/misaki.png",
            "chance": 1.0
        }
    ],
    "あや": [
        {
            "name": "あや",
            "file": "aya.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/aya2.png",
            "chance": 1.0
        }
    ],
    "りん": [
        {
            "name": "りん",
            "file": "rin.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/rin.png",
            "chance": 1.0
        }
    ],
    "ゆい": [
        {
            "name": "ゆい",
            "file": "yui.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/yui.png",
            "chance": 1.0
        }
    ],
    "なぎさ": [
        {
            "name": "なぎさ",
            "file": "nagisa.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/nagisa2.png",
            "chance": 1.0
        }
    ],
    "ことね": [
        {
            "name": "ことね",
            "file": "kotone.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/kotone.png",
            "chance": 1.0
        }
    ],
    "はる": [
        {
            "name": "はる",
            "file": "haru.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/haru.png",
            "chance": 1.0
        }
    ],
    "かなで": [
        {
            "name": "かなで",
            "file": "kanade.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/kanade.png",
            "chance": 1.0
        }
    ],
    "めぐ": [
        {
            "name": "めぐ",
            "file": "megu.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/megu.png",
            "chance": 1.0
        }
    ],
    "みお": [
        {
            "name": "みお",
            "file": "mio.txt",
            "avatar": "https://yusuke366.github.io/discord-chatgpt/avatars/mio.png",
            "chance": 1.0
        }
    ]
}