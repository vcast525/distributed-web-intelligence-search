import logging

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    noisy_loggers = [
        "celery",
        "kombu",
        "amqp",
        "pymongo",
        "httpx",
        "elastic_transport",
    ]

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)