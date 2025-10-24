#!/bin/bash
# Monitor OpenAQ download progress
# Usage: bash scripts/monitor_download.sh

clear
echo "=========================================="
echo "OpenAQ Download Monitor"
echo "=========================================="
echo ""

# Check if process is running
PROCESS=$(ps aux | grep download_openaq_full.sh | grep -v grep)
if [ -z "$PROCESS" ]; then
    echo "⚠️  Download process NOT running"
else
    echo "✓ Download process running (PID: $(echo $PROCESS | awk '{print $2}'))"
fi

echo ""
echo "=== Progress ==="
FILES=$(find data/raw/openaq -name "*.csv.gz" 2>/dev/null | wc -l)
SIZE=$(du -sh data/raw/openaq 2>/dev/null | cut -f1)
echo "Files downloaded: $FILES"
echo "Total size: $SIZE"

echo ""
echo "=== Recent Activity (last 10 lines) ==="
tail -10 logs/download_manual.log

echo ""
echo "=== Refresh ==="
echo "Run: bash scripts/monitor_download.sh"
