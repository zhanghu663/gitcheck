# coding=utf-8


def settings(init=False, basedir=None, configfile=None):
    global _instance
    if _instance is not None:
        if init:
            raise ValueError("Settings Manager already initialized")
    else:
        if init:
            _instance = Settings(configfile=configfile, basedir=basedir)
        else:
            raise ValueError("Settings not initialized yet")
    return _instance