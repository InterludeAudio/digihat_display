# digihat_display

Shows the Raspberry Pi's IP address and the current playback sample rate on the 0.91" OLED of the Interlude Audio Digital Hat. It runs as the `interludeaudio` systemd service and reads the rate from the ALSA card `sndIADigitalHat` (`/proc/asound/sndIADigitalHat/pcm0p/sub0/hw_params`).

Works on stock Raspberry Pi OS (Bookworm or newer, 32- or 64-bit) on any Pi including the Pi 5. The Digital Hat driver is part of the standard Raspberry Pi kernel since 6.6.17 (March 2024), so no custom OS image is needed.

## Install (Debian package)

```sh
wget -N https://raw.githubusercontent.com/InterludeAudio/digihat_display/main/IA-digihat-display-service.deb
sudo apt install ./IA-digihat-display-service.deb
```

`apt install` pulls in the dependencies (`python3-smbus`, `python3-pil`), enables the service and starts it. The logo shows for ten seconds, then the IP address and sample rate (or "None" when nothing is playing).

Remove with `sudo apt remove interludeaudio-digital-display-service`.

## Install from source

```sh
git clone https://github.com/InterludeAudio/digihat_display.git
cd digihat_display
sudo apt install python3-smbus python3-pil
sudo ./install.sh
```

## Troubleshooting

- `systemctl status interludeaudio` and `journalctl -u interludeaudio` show what the service is doing.
- The display is on I2C address `0x3C`. `i2cdetect -y 1` (package `i2c-tools`) should list it when the hat is fitted. The hat's EEPROM overlay enables I2C; if you are not using a provisioned hat, enable I2C with `raspi-config`.
- Older driver builds used a different ALSA card name. If `aplay -l` shows the card as something other than `sndIADigitalHat`, set `IA_CARD_ID` in the service environment, e.g. `Environment=IA_CARD_ID=sndinterludeaud` in a `systemctl edit interludeaudio` drop-in.

## Building the package

```sh
packaging/build-deb.sh            # version from packaging/VERSION
packaging/build-deb.sh 1.2        # explicit version
```

The GitHub workflow builds the package on every push and attaches it to the release when a `v*` tag is pushed.
