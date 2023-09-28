import functools
import logging
import time
from datetime import datetime

from pytz import UTC, timezone
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

from app.logger import RichHandler

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%x %X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


def sleep_pro(t: int, desc: str = "Sleeping..."):
    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task(f"[cyan]{desc}", total=t * 5)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(0.2)


def retry(retry_times=3, interval=0):
    """
    普通函数的重试装饰器
    Args:
        retry_times: 重试次数
        interval: 每次重试之间的间隔

    Returns:

    """
    def _retry(func):
        @functools.wraps(func)  # 将函数的原来属性付给新函数
        def wapper(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"[Retry] Function {func.__name__} failed to run, retrying {i + 1} time(s). error:"
                        f"\n{e}"
                    )
                    time.sleep(interval)
                    if i + 1 >= retry_times:
                        raise e

        return wapper

    return _retry


def get_local_now_ts(
    timezone_str: str = 'America/Toronto',
) -> datetime:
    """
    Get the current timestamp in a local timezone.

    Parameters
    ----------
    timezone_str : str, optional
        The timezone string in the format of 'Area/Location', by default 'America/Toronto'.

    Returns
    -------
    datetime
        The current timestamp in the specified local timezone.

    Examples
    --------
    >>> get_local_now_ts()
    datetime.datetime(2023, 2, 9, 15, 59, 59, tzinfo=<DstTzInfo 'America/Toronto' EST-1 day, 19:00:00 STD>)
    >>> get_local_now_ts('Asia/Shanghai')
    datetime.datetime(2023, 2, 9, 23, 59, 59, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
    """
    # Get aware timestamp of UTC (with timezone info)
    utc_now_ts = datetime.now(UTC)

    # Create a timezone instance for YYZ
    local_timezone = timezone(timezone_str)

    # Change the UTC aware time to YYZ aware time with YYZ timezone
    local_now_ts = utc_now_ts.astimezone(tz=local_timezone)
    return local_now_ts


def get_local_now_string(
    format: str = '%Y-%m-%d %H:%M:%S',
    timezone_str: str = 'America/Toronto',
) -> str:
    """
    Parameters
    ----------
    format : str, optional
        The format for the local time string, by default '%H:%M:%S'.
    timezone_str : str, optional
        The timezone string, by default 'America/Toronto'.

    Returns
    -------
    str
        A string with the specified format (`%H:%M:%S` by default) for 
        the current local time in the specified timezone (`America/Toronto` by default).
    """
    local_now_ts = get_local_now_ts(timezone_str=timezone_str)
    local_now_string = local_now_ts.strftime(format)
    return local_now_string


def get_emoji_color(value: int or datetime) -> str:
    if isinstance(value, int):
        color_ranges = {
            (350, 500): "⚪",  # White emoji
            # (11, 21): "🔵",  # Blue emoji
            (180, 350): "🟢",  # Green emoji
            # (31, 41): "🟡",  # Yellow emoji
            # (41, 51): "🟠",  # Orange emoji
            (0, 180): "🔴"  # Red emoji
        }
    elif isinstance(value, datetime):
        color_ranges = {
            (datetime(2024, 9, 1), datetime(2024, 12, 31)): "⚪",  # White emoji
            # (11, 21): "🔵",  # Blue emoji
            (datetime(2024, 5, 1), datetime(2024, 9, 1)): "🟢",  # Green emoji
            (datetime(2024, 2, 1), datetime(2024, 5, 1)): "🟡",  # Yellow emoji
            # (41, 51): "🟠",  # Orange emoji
            (datetime(2023, 9, 1), datetime(2024, 2, 1)): "🔴"  # Red emoji
        }

    for range_, emoji in color_ranges.items():
        if range_[0] <= value < range_[1]:
            return emoji

    return ""  # Unknown emoji (outside the specified ranges)
