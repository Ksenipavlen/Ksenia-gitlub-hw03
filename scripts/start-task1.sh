#!/usr/bin/env bash
set -euo pipefail

python3 server.py --name task1-py1 --port 8001 &
python3 server.py --name task1-py2 --port 8002 &

echo "Started task 1 Python servers on ports 8001 and 8002."
echo "Run HAProxy with: sudo haproxy -f configs/task1-haproxy.cfg"
wait
