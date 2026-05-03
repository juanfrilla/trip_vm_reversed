import logging
import random


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;213m"
    PURPLE = "\033[38;5;141m"
    LIME = "\033[38;5;154m"
    TEAL = "\033[38;5;43m"
    GOLD = "\033[38;5;220m"
    CORAL = "\033[38;5;203m"
    SKY = "\033[38;5;117m"

    _ALL = [
        GREEN,
        YELLOW,
        BLUE,
        CYAN,
        MAGENTA,
        WHITE,
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_YELLOW,
        BRIGHT_BLUE,
        BRIGHT_MAGENTA,
        BRIGHT_CYAN,
        BRIGHT_WHITE,
        ORANGE,
        PINK,
        PURPLE,
        LIME,
        TEAL,
        GOLD,
        CORAL,
        SKY,
    ]

    @classmethod
    def random(cls):
        return random.choice(cls._ALL)


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = Colors.random()
        log_format = f"{color}[%(asctime)s] [%(levelname)s]{Colors.RESET} %(message)s"
        formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
        return formatter.format(record)


def get_logger(name="TripVMReversed"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())

        logger.addHandler(console_handler)

    return logger
