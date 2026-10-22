import logging
import os
from pathlib import Path

logger = logging.getLogger()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | Line:%(lineno)d | %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

if os.getenv("TESTING") != "1":
    Path("logs").mkdir(exist_ok=True)

    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

logger.setLevel(logging.INFO)