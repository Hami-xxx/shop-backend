import logging

logger = logging.getLogger()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | Line:%(lineno)d | %(message)s"
)

file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
