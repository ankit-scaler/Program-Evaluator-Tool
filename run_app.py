import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uvicorn

# Ensure the root directory is on the python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == '__main__':
    print("=" * 70)
    print(">> STARTING SCALER PROGRAM EVALUATOR & SALES DECISION ENGINE")
    print("=" * 70)
    print(">> Empirical Funnel Matrix: 13,180 records precomputed")
    print(">> Interactive Web Dashboard: http://127.0.0.1:8000")
    print(">> Press Ctrl+C to stop the server")
    print("=" * 70)
    uvicorn.run("Program_Evaluator_Sales.src.server:app", host="127.0.0.1", port=8000, log_level="info")
