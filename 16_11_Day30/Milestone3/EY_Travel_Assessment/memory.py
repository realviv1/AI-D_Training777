import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    decode_responses=True
)

def save_session(session_id,data):

    redis_client.set(
        session_id,
        json.dumps(data)
    )

def get_session(session_id):

    data = redis_client.get(session_id)

    if not data:
        return {}

    return json.loads(data)