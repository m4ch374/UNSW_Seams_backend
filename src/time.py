from datetime import timezone
import datetime as dt

def get_time():
    return ((dt.datetime.now(timezone.utc)).replace(tzinfo=timezone.utc)).timestamp()

