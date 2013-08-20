lcd-notification
================

Simple rotating status displays for the Adafruit 16x2 LCD on the Raspberry Pi

#### Requirements

	sudo pip install transmissionrpc psutil

#### Optional (See NotificationCenter.py)

	sudo apt-get install fortunes fortunes-min fortune-mod

#### Installing the RC script

    sudo cp lcd-notification.rc /etc/init.d/lcd-notification
    sudo cp lcd-notification.default /etc/default/lcd-notification

    sudo chmod 755 /etc/init.d/lcd-notification
    sudo update-rc.d lcd-notification defaults

#### Uninstalling

    sudo update-rc.d -f lcd-notification remove
    sudo rm /etc/init.d/lcd-notification
