#!/bin/bash
# Build the Debian package for the Digital Hat display service.
# Usage: packaging/build-deb.sh [version]   -> IA-digihat-display-service.deb
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION="${1:-$(cat packaging/VERSION)}"
PKG=interludeaudio-digital-display-service
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

INSTALL_DIR="$STAGE/usr/interlude_audio/digihat_display"
install -d "$INSTALL_DIR/scripts" "$INSTALL_DIR/BRS_SSD1306" "$INSTALL_DIR/assets" "$STAGE/lib/systemd/system" "$STAGE/DEBIAN"
install -m 755 display.py "$INSTALL_DIR/display.py"
install -m 755 scripts/display_start.sh "$INSTALL_DIR/scripts/display_start.sh"
install -m 644 BRS_SSD1306/__init__.py BRS_SSD1306/SSD1306.py "$INSTALL_DIR/BRS_SSD1306/"
install -m 644 assets/Questrial-Regular.ttf assets/logo3.png "$INSTALL_DIR/assets/"
install -m 644 scripts/interludeaudio.service "$STAGE/lib/systemd/system/interludeaudio.service"

cat > "$STAGE/DEBIAN/control" <<CTRL
Package: $PKG
Version: $VERSION
Section: sound
Priority: optional
Architecture: all
Depends: python3, python3-smbus, python3-pil
Maintainer: Interlude Audio (Blue Rock Software) <ben@bluerocksoft.com>
Homepage: https://github.com/InterludeAudio/digihat_display
Description: Interlude Audio Digital Hat OLED display service
 Shows the Pi's IP address and the current playback sample rate on the
 0.91" SSD1306 OLED of the Interlude Audio Digital Hat. Runs as the
 interludeaudio systemd service.
CTRL

cat > "$STAGE/DEBIAN/postinst" <<'POST'
#!/bin/sh
set -e
if [ "$1" = "configure" ]; then
    systemctl daemon-reload || true
    systemctl enable interludeaudio.service || true
    systemctl restart interludeaudio.service || true
fi
exit 0
POST

cat > "$STAGE/DEBIAN/prerm" <<'PRERM'
#!/bin/sh
set -e
if [ "$1" = "remove" ]; then
    systemctl stop interludeaudio.service || true
    systemctl disable interludeaudio.service || true
fi
exit 0
PRERM

cat > "$STAGE/DEBIAN/postrm" <<'POSTRM'
#!/bin/sh
set -e
systemctl daemon-reload || true
exit 0
POSTRM
chmod 755 "$STAGE/DEBIAN/postinst" "$STAGE/DEBIAN/prerm" "$STAGE/DEBIAN/postrm"

OUT="IA-digihat-display-service.deb"
dpkg-deb --root-owner-group --build "$STAGE" "$OUT" >/dev/null
echo "built $OUT ($PKG $VERSION)"
