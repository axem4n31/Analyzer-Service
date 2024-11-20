import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

URL_OPENAI = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}
DATA_OPENAI = {
    "model": "gpt-4",
    "messages": [
        {"role": "user", "content": "назови всех животных в алфавитном порядке"}
    ],
    "temperature": 0.5,
}
LOGS_PATH = Path("./logs/")


# logging
log_filename = LOGS_PATH / f"log_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    filename=log_filename,
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)

handler = RotatingFileHandler(
    LOGS_PATH / "log.log",  # Имя файла журнала
    maxBytes=1024 * 1024 * 5,  # Максимальный размер файла в байтах (например, 5 MB)
    backupCount=3,  # Количество резервных файлов
)


def get_logger(name_module: str):
    logger = logging.getLogger(name_module)
    logger.addHandler(handler)
    return logger
