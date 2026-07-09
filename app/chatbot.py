import os
import discord
import random
import re
import requests

from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv
from openai import (
    OpenAI,
    RateLimitError,
    APIError,
    AuthenticationError,
)
from bs4 import BeautifulSoup

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

WEBHOOK_CACHE = {}
async def get_webhook(channel):
    webhook = WEBHOOK_CACHE.get(
        channel.id
    )
    if webhook:
        try:
            await webhook.fetch()
            return webhook
        except Exception:
            pass

    webhooks = await channel.webhooks()
    for webhook in webhooks:
        if webhook.name == "chatgptbot":
            WEBHOOK_CACHE[channel.id] = webhook
            return webhook

    webhook = await channel.create_webhook(
        name="chatgptbot"
    )
    WEBHOOK_CACHE[channel.id] = webhook

    return webhook

chance_for_all = 0.3
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
}

@bot.tree.command(
    name="persona",
    description="人格を変更します"
)
@app_commands.choices(
    persona=[
        app_commands.Choice(
            name="なし",
            value="なし"
        ),
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
    if persona.value == "なし":
        channel_personas.pop(
            interaction.channel_id,
            None
        )
        await interaction.response.send_message(
            "人格設定を解除しました。",
            ephemeral=True
        )

        return

    channel_personas[
        interaction.channel_id
    ] = persona.value
    await interaction.response.send_message(
        f"人格を {persona.value} に変更しました。",
        ephemeral=True
    )

def fetch_url_content(url):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return soup.get_text(
        separator=" ",
        strip=True
    )[:2000]

@bot.event
async def on_ready():
    synced = await bot.tree.sync()

    print("登録コマンド:")
    for cmd in synced:
        print(f"- {cmd.name}")
        print(cmd.to_dict())

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
            if msg.author.bot:
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

        #メッセージにURLが含まれる場合は要約
        summary = None
        urls = re.findall(
            r'https?://\S+',
            message.content
        )
        if urls:
            url = urls[0]
            try:
                article_text = fetch_url_content(url)
                summary_response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "以下の記事を200文字程度で要約してください。"
                        },
                        {
                            "role": "user",
                            "content": article_text
                        }
                    ]
                )
                summary = summary_response.choices[0].message.content
            
            except Exception as e:
                print(f"URL取得失敗: {e}")
        
        #画像が投稿された場合
        images = []
        for attachment in message.attachments:
            if attachment.content_type and \
            attachment.content_type.startswith("image/"):
                images.append(attachment.url)

        shuffled_personas = random.sample(
            personas,
            len(personas)
        )

        selected_personas = []
        for persona in shuffled_personas:
            if persona["name"] in message.content:
                selected_personas.append(persona)
            elif random.random() <= persona["chance"]:
                selected_personas.append(persona)

        if not selected_personas:
            selected_personas.append(
                shuffled_personas[0]
            )

        for persona in selected_personas:
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

            if summary:
                messages.append(
                    {
                        "role": "user",
                        "content": f"共有されたURLの要約:\n{summary}"
                    }
                )

            if images:
                image_content = [
                    {
                        "type": "text",
                        "text": "画像が投稿されました"
                    }
                ]
                for image_url in images:
                    image_content.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    )
                messages.append(
                    {
                        "role": "user",
                        "content": image_content
                    }
                )

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
