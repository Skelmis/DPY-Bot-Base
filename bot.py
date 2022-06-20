import asyncio
import contextlib
import io
import logging
import os
import textwrap
from traceback import format_exception

import disnake as disnake
from disnake.ext import commands

from bot_base import BotBase
from bot_base.paginators.disnake_paginator import DisnakePaginator

logging.basicConfig(level=logging.INFO)
logging.getLogger("bot_base.cogs.invite_tracking").setLevel(logging.DEBUG)


async def main():
    bot = BotBase(
        command_prefix="t.",
        mongo_url=os.environ["MONGO_URL"],
        mongo_database_name="my_bot",
        load_builtin_commands=True,
        load_invite_tracking=True,
        intents=disnake.Intents.all(),
    )

    @bot.event
    async def on_ready():
        print("I'm up.")

    @bot.command()
    async def echo(ctx):
        await ctx.message.delete()

        text = await ctx.get_input("What should I say?", timeout=5)

        if not text:
            return await ctx.send("You said nothing!")

        await ctx.send(text)

    @bot.command()
    async def ping(ctx):
        await ctx.send_basic_embed("Pong!")

    bot.load_extension("bot_base.cogs.invite_tracking")
    await bot.start(os.environ["TOKEN"])


asyncio.run(main())
