import sys

def is_python3():
    return sys.version_info >= (3, 0)

def is_python26():
    return sys.version_info >= (2, 6) and sys.version_info <= (2, 7)

if is_python26():
    def total_seconds(timedelta):
        return ((timedelta.microseconds + (timedelta.seconds + timedelta.days * 24 * 3600) * 10**6.0) / 10**6.0)
else:
    def total_seconds(timedelta):
        return timedelta.total_seconds()
