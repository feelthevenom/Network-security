import logging
import os
from datetime import datetime

dirr = os.path.join("logs")

os.makedirs(dirr, exist_ok=True)

log_path = os.path.join(dirr, f"{datetime.now().strftime('%Y-%m-%d')}.log")


logging.basicConfig(
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    filename=log_path,
)

