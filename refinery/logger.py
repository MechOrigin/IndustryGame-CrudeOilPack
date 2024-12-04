# logger.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("game.log"),
        logging.StreamHandler()
    ]
)

def get_logger():
    return logging.getLogger("CrudeOilGame")
