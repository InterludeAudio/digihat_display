# digihat_display
Code to control the DigiHat's Display

To install as Debian Pacakge use the following commands

`wget -N https://raw.githubusercontent.com/InterludeAudio/digihat_display/main/IA-digihat-display-service.deb`

`sudo dpkg -i IA-digihat-display-service.deb`

This python code update the i2c OLED display on the DigiHat with the current sample rate of content that is playing.  

To install on Raspian just extract a tarball of this source and run the `install.sh` script as root.

`sudo install.sh`

Then reboot and the display should start working after the kernel loads.  

When you play or record audio the sample rate will be displayed on the OLED display.  
