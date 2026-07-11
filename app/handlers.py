import logging
import random
import re

import aiohttp
from bs4 import BeautifulSoup
from openai import APIError, AuthenticationError, RateLimitError

from .personas import channel_personas, load_persona
from .constants import PERSONA_FILES
from .webhooks import get_webhook

try:
    from .personas import channel_personas, load_persona
    from .constants import PERSONA_FILES
    from .webhooks import get_webhook
except ImportError:
    from personas import channel_personas, load_persona
    from constants import PERSONA_FILES
    from webhooks import get_webhook


async def fetch_url_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        ) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text[:2000]


def setup_event_handlers(bot, client_ai):
    async def handle_on_ready():
        synced = await bot.tree.sync()

        logging.info("登録コマンド:")
        for cmd in synced:
            logging.info(f"- {cmd.name}")

        for channel_id, persona in channel_personas.items():
            channel = bot.get_channel(channel_id)
            if channel is None:
                continue

            logging.info(f"再起動後の人格設定を復元しました: {channel_id}/{persona}")

        print(f"ログイン成功: {bot.user}")
        logging.info(f"ログイン成功: {bot.user}")
        logging.info(f"{len(synced)} 個のコマンドを同期しました")

    async def handle_on_message(message):
        await process_message(bot, message, client_ai)

    bot.add_listener(handle_on_ready, "on_ready")
    bot.add_listener(handle_on_message, "on_message")


async def process_message(bot, message, client_ai):
    if message.author.bot:
        return

    if message.mentions:
        return

    persona_group = channel_personas.get(message.channel.id)
    if persona_group is None:
        return

    personas = PERSONA_FILES[persona_group]

    webhook = await get_webhook(message.channel)

    try:
        history = []
        async for msg in message.channel.history(limit=20):
            if msg.id == message.id:
                continue
            if msg.author.bot:
                continue
            if not msg.content:
                continue

            history.append({"role": "user", "content": msg.content})
        history.reverse()

        summary = None
        urls = re.findall(r"https?://\S+", message.content)
        if urls:
            url = urls[0]
            try:
                article_text = await fetch_url_content(url)
                summary_response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "以下の記事を200文字程度で要約してください。",
                        },
                        {
                            "role": "user",
                            "content": article_text,
                        },
                    ],
                )
                summary = summary_response.choices[0].message.content
            except Exception as e:
                logging.error(f"URL取得失敗: {e}")

        images = []
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                images.append(attachment.url)

        shuffled_personas = random.sample(personas, len(personas))

        selected_personas = []
        for persona in shuffled_personas:
            if persona["name"] in message.content:
                selected_personas.append(persona)
            elif random.random() <= persona["chance"]:
                selected_personas.append(persona)

        if not selected_personas:
            selected_personas.append(shuffled_personas[0])

        for persona in selected_personas:
            logging.info(f"{persona['name']} が回答します")

            system_prompt = load_persona(persona["file"])
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)

            if summary:
                messages.append(
                    {
                        "role": "user",
                        "content": f"共有されたURLの要約:\n{summary}",
                    }
                )

            if images:
                image_content = [{"type": "text", "text": "画像が投稿されました"}]
                for image_url in images:
                    image_content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        }
                    )
                messages.append({"role": "user", "content": image_content})

            messages.append({"role": "user", "content": message.content})

            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            await webhook.send(
                content=response.choices[0].message.content,
                username=persona["name"],
                avatar_url=persona["avatar"],
            )
            logging.info(f"{persona['name']} が回答しました")

    except RateLimitError:
        await webhook.send(
            content="⚠️ OpenAI APIの利用枠が不足しています。",
            username="システム",
        )

    except AuthenticationError:
        await webhook.send(
            content="⚠️ OpenAI APIキーが無効です。",
            username="システム",
        )

    except APIError:
        await webhook.send(
            content="⚠️ OpenAI APIエラーが発生しました。",
            username="システム",
        )

    except Exception as e:
        logging.exception(e)

        await webhook.send(
            content="⚠️ 予期しないエラーが発生しました。",
            username="システム",
        )