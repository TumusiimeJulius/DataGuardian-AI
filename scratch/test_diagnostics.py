import requests
import time

url_base = "https://dataguardianai.onrender.com/diagnose_investigate"

for limit in range(1, 19):
    print(f"Testing step_limit={limit}...")
    start = time.time()
    try:
        r = requests.get(f"{url_base}?question=test&step_limit={limit}", timeout=35)
        elapsed = time.time() - start
        print(f"  Status: {r.status_code}")
        print(f"  Time elapsed: {elapsed:.2f}s")
        if r.status_code == 200:
            print(f"  Response: {r.json()}")
        else:
            print(f"  Response (first 100 chars): {r.text[:100]}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"  Request failed: {str(e)} (elapsed: {elapsed:.2f}s)")
    print("-" * 50)
