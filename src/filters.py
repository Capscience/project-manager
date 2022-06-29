import datetime
from src import app


@app.template_filter()
def timeformat(timedelta: datetime.timedelta) -> str:
    """Format timedelta object to HH:MM:SS.

    Timedelta shows days, this converts them into hours.
    """

    if timedelta is None:
        timedelta = datetime.timedelta(seconds=0)
    timedelta = int(timedelta.total_seconds())
    sign = '-' if timedelta < 0 else ''
    timedelta = abs(timedelta)
    hours = timedelta // 3600
    minutes = timedelta // 60 % 60
    seconds = timedelta % 60
    return f'{sign}{hours:02}:{minutes:02}:{seconds:02}'
