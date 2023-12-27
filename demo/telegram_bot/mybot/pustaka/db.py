# -*-coding:utf8;-*-
import redis
import os
import chatrouter


REDIS_HOST = os.environ.get("REDIS_HOST", "insert your redis host here")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "insert your redis port here"))
REDIS_PASSWORD = os.environ.get(
    "REDIS_PASSWORD", "insert your redis password here")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)


def user_exists(id):
    return r.get(id) is not None


def get_user_session(id):
    return r.get(id).decode("utf-8")


def add_user(id):
    r.set(id, "main")


def update_user_session(id, loc):
    if not chatrouter.group_exists(loc):
        raise ValueError
    r.set(id, loc)
