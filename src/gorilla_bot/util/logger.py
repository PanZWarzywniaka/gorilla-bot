import logging
# from discord_logger import DiscordLogger

logging.basicConfig(filename='gorilla-bot.log', level=logging.INFO,
                    format='%(asctime)s%(levelname)s %(message)s')


def log_info(message: str):
    print(message)
    logging.info(message)
