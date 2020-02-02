import settings


def param_shortcut(f):
    def wrapper(*args, **kwargs):
        d = kwargs.copy()
        for k, v in kwargs.items():
            if k in settings.PARAM_SHORTCUTS:
                d[settings.PARAM_SHORTCUTS[k]] = v
        return f(*args, **d)
    return wrapper


def shortcut(obj):
    for f in dir(obj):
        if not callable(getattr(obj, f)) or f.startswith("__"):
            continue
        setattr(obj, f, param_shortcut(getattr(obj, f)))
    for k, v in settings.CMD_SHORTCUTS.items():
        setattr(obj, k, getattr(obj, settings.CMD_SHORTCUTS[k]))
    return obj
