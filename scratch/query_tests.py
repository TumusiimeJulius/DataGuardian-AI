import requests
import time

url_base = "https://dataguardianai.onrender.com"

tests = [
    "/test_pandas_1",
    "/test_pandas_2",
    "/test_pandas_3",
    "/test_pandas_4",
    "/test_pandas_5",
    "/test_pandas_6"
]

print("Starting checks on Render...")
for check in tests:
    print(f"Testing {check}...")
    start = time.time()
    try:
        r = requests.get(f"{url_base}{check}", timeout=35)
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
