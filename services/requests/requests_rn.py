import random
import time

import requests

URL = "http://ml_service:8000/api/prediction/{item_id}"

def _generate_random_data():

    age = random.randint(29, 77)

    return {
        "age": age,                                   # 29–77
        "sex": random.randint(0, 1),                  # 0–1
        "cp": random.randint(0, 3),                   # 0–3
        "trestbps": random.randint(94, 200),          # 94–200
        "chol": random.randint(126, 564),             # 126–564
        "fbs": random.randint(0, 1),                  # 0–1
        "restecg": random.randint(0, 2),              # 0–2
        "thalach": random.randint(71, 202),           # 71–202
        "exang": random.randint(0, 1),                # 0–1
        "oldpeak": round(random.uniform(0.0, 6.2), 1),# 0.0–6.2
        "slope": random.randint(0, 2),                # 0–2
        "ca": random.randint(0, 4),                   # 0–4
        "thal": random.randint(0, 3),                 # 0–3
        "high_age": int(age > 60)                     # 1, если age > 60
    }

def send_request(item_id: int):
    try:
        response = requests.post(URL.format(item_id=item_id), json=_generate_random_data())
        print(f"[{item_id}] Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"[{item_id}] Request failed: {e}")

def run():
    item_id = 1
    while True:
        send_request(item_id)
        item_id += 1
        sleep_time = random.uniform(0, 5)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    run()