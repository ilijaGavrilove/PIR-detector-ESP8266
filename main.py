import asyncio
import logging
import sys
import bot.bot as bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(bot.main())
