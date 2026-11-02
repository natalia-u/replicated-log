import time
import httpx

MASTER_URL = "http://127.0.0.1:8000/messages"

start_time = time.time()

response = httpx.post(
    MASTER_URL,
    params={"message": "integration-test"},
    timeout=15.0
)

end_time = time.time()

duration = end_time - start_time

print("Response:", response.json())
print("Duration:", round(duration, 2), "seconds")

assert response.status_code == 200
assert response.json()["status"] == "ok"
assert duration < 10