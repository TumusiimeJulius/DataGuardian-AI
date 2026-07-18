import urllib.request
import time
from datetime import datetime

URL = "https://dataguardianai.onrender.com/investigate?question=test"
OUT = "backend/investigate_poll.log"

with open(OUT, "w", encoding="utf-8") as f:
    for i in range(10):
        ts = datetime.utcnow().isoformat() + "Z"
        try:
            req = urllib.request.Request(URL)
            with urllib.request.urlopen(req, timeout=20) as resp:
                status = resp.getcode()
                body = resp.read(2000).decode('utf-8', errors='replace')
        except Exception as e:
            status = getattr(e, 'code', 'EXC')
            body = str(e)
        f.write(f"{ts} | attempt={i+1} | status={status}\n")
        f.write(body + "\n---\n")
        f.flush()
        if i < 9:
            time.sleep(30)
print('Done polling, log:', OUT)
