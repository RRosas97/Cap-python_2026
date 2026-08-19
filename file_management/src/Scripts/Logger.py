import logging
import traceback
from pathlib import Path


class Logger:

    def configurar_logger():
        log_path = Path("utils/logs")
        log_path.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("mi_app")
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            log_file = log_path / "app.log"
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls.__set_logger(cls)

            if level == "critical":
                logger.critical(message)
            elif level == "debug":
                logger.debug(message)
            elif level == "error":
                logger.error(message)
            elif level == "info":
                logger.info(message)
            elif level == "warn":
                logger.warning(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)
