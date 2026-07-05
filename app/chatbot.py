import os

import discord
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


PERSONA_FILES = {
    "女友達": "girl_friend.txt",
    "アシスタント": "assistant.txt",
    "ソフトウェアエンジニア": "engineer.txt",
}

@bot.tree.command(
    name="persona",
    description="人格を変更します"
)
@app_commands.choices(
    persona=[
        app_commands.Choice(
            name="女友達",
            value="女友達"
        ),
        app_commands.Choice(
            name="アシスタント",
            value="アシスタント"
        ),
        app_commands.Choice(
            name="ソフトウェアエンジニア",
            value="ソフトウェアエンジニア"
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

    persona_name = channel_personas.get(
        message.channel.id,
        "女友達"
    )

    persona_file = PERSONA_FILES[persona_name]
    system_prompt = load_persona(persona_file)

    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message.content
                }
            ]
        )

        await message.channel.send(
            response.choices[0].message.content
        )

    except RateLimitError:
        await message.channel.send(
            "⚠️ OpenAI APIの利用枠が不足しています。"
        )

    except AuthenticationError:
        await message.channel.send(
            "⚠️ OpenAI APIキーが無効です。"
        )

    except APIError:
        await message.channel.send(
            "⚠️ OpenAI APIエラーが発生しました。"
        )

    except Exception as e:
        print(f"Unexpected Error: {e}")

        await message.channel.send(
            "⚠️ 予期しないエラーが発生しました。"
        )

bot.run(DISCORD_TOKEN)
