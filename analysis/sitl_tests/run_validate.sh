#!/bin/bash
set -e
cd /home/david12daniel/.openclaw/agents/thermal-surveillance-drone/analysis/sitl_tests

# Kill any stale instances
pkill -f "apm.*instance 17" 2>/dev/null || true
sleep 1

# Start SITL in background
./bin/arducopter --home "42.3000,-83.7000,180,0" --model "+" --speedup 3 --instance 17 &
SITL_PID=$!
echo "SITL PID=$SITL_PID"
sleep 8

# Check if still running
kill -0 $SITL_PID 2>/dev/null && echo "SITL running" || { echo "SITL died!"; exit 1; }

# Check TCP port
ss -tlnp 2>/dev/null | grep 5770 && echo "Port 5770 open" || { echo "Port 5770 not open"; exit 1; }

echo "SITL IS READY"
wait $SITL_PID 2>/dev/null || true
