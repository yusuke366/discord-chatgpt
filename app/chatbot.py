import os
import discord
import random

from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv
from openai import (
    OpenAI,
    RateLimitError,
    APIError,
    AuthenticationError,
)

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
)

# チャンネルごとの人格設定
channel_personas = {}

def load_persona(filename: str) -> str:
    with open(
        os.path.join("personas", filename),
        encoding="utf-8"
    ) as f:
        return f.read()

async def get_webhook(channel):
    webhooks = await channel.webhooks()

    for webhook in webhooks:
        if webhook.name == "chatgptbot":
            return webhook

    return await channel.create_webhook(
        name="chatgptbot"
    )

PERSONA_FILES = {
    "全員": [
        {
            "name": "みさき",
            "file": "misaki.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/misaki.png",
            "chance": 0.5
        },
        {
            "name": "あや",
            "file": "aya.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/aya2.png",
            "chance": 0.5
        },
        {
            "name": "りん",
            "file": "rin.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/rin.png",
            "chance": 0.5
        },
        {
            "name": "ゆい",
            "file": "yui.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/yui.png",
            "chance": 0.5
        },
        {
            "name": "なぎさ",
            "file": "nagisa.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/nagisa2.png",
            "chance": 0.5
        },
        {
            "name": "ことね",
            "file": "kotone.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/kotone.png",
            "chance": 0.5
        }
    ],

    "アシスタント": [
        {
            "name": "あや",
            "file": "assistant.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/aya2.png",
            "chance": 1.0
        }
    ],

    "ソフトウェアエンジニア": [
        {
            "name": "りん",
            "file": "engineer.txt",
            "avatar": "https://raw.githubusercontent.com/yusuke366/discord-chatgpt/main/app/personas/avatars/rin.png",
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
}

@bot.tree.command(
    name="persona",
    description="人格を変更します"
)
@app_commands.choices(
    persona=[
        app_commands.Choice(
            name="全員",
            value="全員"
        ),
        app_commands.Choice(
            name="アシスタント",
            value="アシスタント"
        ),
        app_commands.Choice(
            name="ソフトウェアエンジニア",
            value="ソフトウェアエンジニア"
        ),
        app_commands.Choice(
            name="みさき",
            value="みさき"
        ),
        app_commands.Choice(
            name="あや",
            value="あや"
        ),
        app_commands.Choice(
            name="りん",
            value="りん"
        ),
        app_commands.Choice(
            name="ゆい",
            value="ゆい"
        ),
        app_commands.Choice(
            name="なぎさ",
            value="なぎさ"
        ),
        app_commands.Choice(
            name="ことね",
            value="ことね"
        ),
    ]
)
async def persona_command(
    interaction: discord.Interaction,
    persona: app_commands.Choice[str]
):
    channel_personas[
        interaction.channel_id
    ] = persona.value

    await interaction.response.send_message(
        f"人格を {persona.value} に変更しました。",
        ephemeral=True
    )

@bot.event
async def on_ready():
    synced = await bot.tree.sync()

    print("登録コマンド:")
    for cmd in synced:
        print(f"- {cmd.name}")

    print(f"ログイン成功: {bot.user}")
    print(f"{len(synced)} 個のコマンドを同期しました")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.mentions:
        return

    persona_group = channel_personas.get(
        message.channel.id
    )
    if persona_group is None:
        return

    personas = PERSONA_FILES[
        persona_group
    ]

    webhook = await get_webhook(
        message.channel
    )

    try:
        history = []
        async for msg in message.channel.history(limit=20):
            if msg.id == message.id:
                continue
            if not msg.content:
                continue

            history.append(
                {
                    "role": "user",
                    "content": msg.content
                }
            )
        history.reverse()        

        shuffled_personas = random.sample(
            personas,
            len(personas)
        )

        for persona in shuffled_personas:
            if random.random() > persona["chance"]:
                continue

            system_prompt = load_persona(
                persona["file"]
            )
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
            messages.extend(history)

            messages.append(
                {
                    "role": "user",
                    "content": message.content
                }
            )

            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply = response.choices[0].message.content.strip()
            if reply.upper().startswith("SKIP"):
                continue

            await webhook.send(
                content=response.choices[0].message.content,
                username=persona["name"],
                avatar_url=persona["avatar"]
            )

    except RateLimitError:
        await webhook.send(
            content="⚠️ OpenAI APIの利用枠が不足しています。",
            username="システム"
        )

    except AuthenticationError:
        await webhook.send(
            content="⚠️ OpenAI APIキーが無効です。",
            username="システム"
        )

    except APIError:
        await webhook.send(
            content="⚠️ OpenAI APIエラーが発生しました。",
            username="システム"
        )

    except Exception as e:
        print(e)

        await webhook.send(
            content="⚠️ 予期しないエラーが発生しました。",
            username="システム"
        )

bot.run(DISCORD_TOKEN)
