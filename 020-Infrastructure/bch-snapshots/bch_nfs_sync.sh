#!/bin/bash
# bch_nfs_sync.sh — Snapshot NFS tree and diff against previous
# Usage: SSH_AUTH_SOCK=/tmp/bch_ssh_agent.sock bash bch_nfs_sync.sh [scope]
# Scopes: workspace (default), data, projects, all
#
# Requires: VPN active (wg-bch), SSH agent with BCH key loaded

set -euo pipefail

SNAP_DIR="$(dirname "$0")"
DATE=$(date +%Y-%m-%d_%H%M)
BCH="daniel.barrerasmeraz@10.26.66.103"
MRI="/neuro/labs/grantlab/research/MRI_processing"
SCOPE="${1:-workspace}"

case "$SCOPE" in
  workspace) TARGET="$MRI/daniel.barrerasmeraz/" ; DEPTH=4 ;;
  data)      TARGET="$MRI/daniel.barrerasmeraz/data/" ; DEPTH=5 ;;
  projects)  TARGET="$MRI/daniel.barrerasmeraz/projects/" ; DEPTH=5 ;;
  shared)    TARGET="$MRI/Data/" ; DEPTH=3 ;;
  tools)     TARGET="$MRI/tools/" ; DEPTH=4 ;;
  all)       TARGET="$MRI/" ; DEPTH=3 ;;
  *)         echo "Unknown scope: $SCOPE"; exit 1 ;;
esac

CURR="$SNAP_DIR/snap_${SCOPE}_${DATE}.txt"
PREV=$(ls -t "$SNAP_DIR"/snap_${SCOPE}_*.txt 2>/dev/null | head -1)

echo "Scope: $SCOPE → $TARGET (depth $DEPTH)"
echo "Taking NFS snapshot..."

SSH_AUTH_SOCK="${SSH_AUTH_SOCK:-/tmp/bch_ssh_agent.sock}" \
  ssh -o ConnectTimeout=15 -o StrictHostKeyChecking=no "$BCH" \
  "find $TARGET -maxdepth $DEPTH -printf '%T@ %s %p\n' 2>/dev/null | sort -k3" \
  > "$CURR"

FILE_COUNT=$(wc -l < "$CURR")
echo "Captured $FILE_COUNT entries → $CURR"

if [ -z "$PREV" ] || [ "$PREV" = "$CURR" ]; then
  echo "First snapshot — no diff available."
  exit 0
fi

echo ""
echo "Comparing against $(basename "$PREV")..."
echo ""

# New files
NEW=$(diff <(awk '{print $3}' "$PREV") <(awk '{print $3}' "$CURR") | grep '^>' | sed 's/^> //' || true)
if [ -n "$NEW" ]; then
  echo "=== NEW FILES ==="
  echo "$NEW"
  echo ""
fi

# Removed files
REMOVED=$(diff <(awk '{print $3}' "$PREV") <(awk '{print $3}' "$CURR") | grep '^<' | sed 's/^< //' || true)
if [ -n "$REMOVED" ]; then
  echo "=== REMOVED ==="
  echo "$REMOVED"
  echo ""
fi

# Modified (size changed)
echo "=== MODIFIED (size changed) ==="
comm -12 <(awk '{print $3}' "$PREV" | sort) <(awk '{print $3}' "$CURR" | sort) | while read -r f; do
  old=$(grep " ${f}$" "$PREV" | awk '{print $2}')
  new=$(grep " ${f}$" "$CURR" | awk '{print $2}')
  if [ "$old" != "$new" ]; then
    echo "  $f ($old → $new bytes)"
  fi
done

echo ""
echo "Done. Snapshots in: $SNAP_DIR"
