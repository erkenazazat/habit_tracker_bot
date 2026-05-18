import json
import os
from datetime import datetime, timedelta

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] Method called: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
