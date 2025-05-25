import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import pathlib
from utils.log import setup_logger
from utils.db import DBFute
from scraping.tabelaData import getRodada
import logging


load_dotenv()
setup_logger()

TOKEN = os.getenv("DISCORD_TOKEN")


logger = logging.getLogger(__name__)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot logged as {bot.user}")
    await bot.tree.sync()
    

async def main():
    async with bot:
        try:
            DBFute()._create_table()
            DBFute().inserir_jogos(getRodada())
        except Exception as e:
            print(e)
        ext_path = pathlib.Path("src/extensions")
        for file in ext_path.glob("*.py"):
            if file.name.startswith("__"):
                continue
            module = f"extensions.{file.stem}"
            try:
                await bot.load_extension(module)
                logger.info(f"Extension carregada: {module}")
            except Exception as e:
                logger.info(f"Erro {module}: {e}")

        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())