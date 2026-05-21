#!/usr/bin/env bash
set -euo pipefail

python3 server.py --name task2-py1 --port 8011 &
python3 server.py --name task2-py2 --port 8012 &
python3 server.py --name task2-py3 --port 8013 &

echo "Started task 2 Python servers on ports 8011, 8012 and 8013."
echo "Run HAProxy with: sudo haproxy -f configs/task2-haproxy.cfg"
wait
