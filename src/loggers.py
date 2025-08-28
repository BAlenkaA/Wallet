import logging

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] [{levelname:<8}] {pathname}:{funcName}:{lineno}: {message}",  # noqa: E501
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)

logger = logging
