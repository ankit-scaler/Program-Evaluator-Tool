import os
import sys

# Ensure UTF-8 output on console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uvicorn

# Ensure the root directory is on the python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("=" * 70)
    print(">> STARTING SCALER PROGRAM EVALUATOR & SALES DECISION ENGINE")
    print("=" * 70)
    print(">> Empirical Funnel Matrix: 13,180 records precomputed")
    print(f">> Server listening on: http://{host}:{port}")
    print("=" * 70)
    uvicorn.run("src.server:app", host=host, port=port, log_level="info")
