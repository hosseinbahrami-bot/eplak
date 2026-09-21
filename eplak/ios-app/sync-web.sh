#!/usr/bin/env bash
# Copies the current web app (eplak/eplak-fixed) into Eplak/Web so the iOS
# bundle always ships the same front-end as the PWA / Android app.
# Usage: bash eplak/ios-app/sync-web.sh   (run from anywhere)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/../eplak-fixed"
DEST="$HERE/Eplak/Web"

rm -rf "$DEST"
mkdir -p "$DEST"
# Same front-end file set the Android app bundles (see android-app/app/build.gradle)
for item in index.html app.js manifest.json sw.js core modules views assets; do
  if [ -e "$SRC/$item" ]; then
    cp -R "$SRC/$item" "$DEST/$item"
  fi
done
find "$DEST" -name ".DS_Store" -delete
echo "Synced web app into $DEST"
du -sh "$DEST"
