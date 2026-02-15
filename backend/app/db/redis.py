import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)

def get_or_set_cache(key, fetch_function, expiry=300):
    try:
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)

        data = fetch_function()
        redis_client.setex(key, expiry, json.dumps(data))
        return data
    except Exception:
        # Redis failure fallback
        return fetch_function()

