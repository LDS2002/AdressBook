from settings import LOG_ENABLED


def log(key, *args):
    if LOG_ENABLED:
        print(key, ': ',  ' '.join(args))
