#!/bin/bash

INSTALL_DIR=/usr/interlude_audio/digihat_display

mkdir -p $INSTALL_DIR/scripts

cp scripts/display_start.sh $INSTALL_DIR/scripts/display_start.sh
cp display.py $INSTALL_DIR
cp -a BRS_SSD1306 $INSTALL_DIR
cp -a assets $INSTALL_DIR

cp scripts/interludeaudio.service /lib/systemd/system

systemctl daemon-reload
systemctl enable interludeaudio.service
