"""Template filters for use in jinja templates."""

import datetime
from src import app


@app.template_filter()
def timeformat(timedelta: datetime.timedelta) -> str:
    """Format timedelta object to HH:MM:SS.

    Timedelta shows days, this converts them into hours.
    """

    if timedelta is None:
        timedelta = datetime.timedelta(seconds=0)
    total_seconds = int(timedelta.total_seconds())
    sign = '-' if total_seconds < 0 else ''
    total_seconds = abs(total_seconds)
    hours = total_seconds // 3600
    minutes = total_seconds // 60 % 60
    seconds = total_seconds % 60
    return f'{sign}{hours:02}:{minutes:02}:{seconds:02}'
