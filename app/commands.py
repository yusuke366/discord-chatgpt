from typing import Optional

import discord
from discord import app_commands

from .personas import channel_personas, save_channel_personas

try:
    from .personas import channel_personas, save_channel_personas
except ImportError:
    from personas import channel_personas, save_channel_personas


def setup_commands(bot):
    @bot.tree.command(name="persona", description="人格を変更します")
    @app_commands.choices(
        persona=[
            app_commands.Choice(name="なし", value="なし"),
            app_commands.Choice(name="全員", value="全員"),
            app_commands.Choice(name="アシスタント", value="アシスタント"),
            app_commands.Choice(name="ソフトウェアエンジニア", value="ソフトウェアエンジニア"),
            app_commands.Choice(name="みさき", value="みさき"),
            app_commands.Choice(name="あや", value="あや"),
            app_commands.Choice(name="りん", value="りん"),
            app_commands.Choice(name="ゆい", value="ゆい"),
            app_commands.Choice(name="なぎさ", value="なぎさ"),
            app_commands.Choice(name="ことね", value="ことね"),
        ]
    )
    async def persona_command(
        interaction: discord.Interaction,
        persona: Optional[app_commands.Choice[str]] = None,
    ):
        if persona is None:
            current = channel_personas.get(interaction.channel_id)
            if current is None:
                message = "現在の人格設定: なし"
            else:
                message = f"現在の人格設定: {current}"

            await interaction.response.send_message(message, ephemeral=True)
            return

        if persona.value == "なし":
            channel_personas.pop(interaction.channel_id, None)
            save_channel_personas(channel_personas)

            await interaction.response.send_message("人格設定を解除しました。", ephemeral=True)
            return

        channel_personas[interaction.channel_id] = persona.value
        save_channel_personas(channel_personas)

        await interaction.response.send_message(
            f"人格を {persona.value} に変更しました。", ephemeral=True
        )