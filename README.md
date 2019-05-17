# Tradfri Ikea Gateway Autoreboot

I want to restart IKEA Tradfri Gateway every day morning with Raspberry Zero W, 
the script with aiocoap creates a command for this idea.

-------------------------------------------------------------------------------------------------

source of my idea: https://github.com/ggravlingen/pytradfri 

requirements (pip install):
pip install aiocoap==0.4a1
pip install DTLSSocket==0.1.7
pip install typing>=3,<4

output command string:
coap-client -u XXXXXXXXXXXX -k XXXXXXXXX -v 0 -m post "coaps://XXXXXXXXXXX:5684/15011/9030"

-------------------------------------------------------------------------------------------------

For using you need install COAP-CLIENT:

sudo apt-get install libtool git build-essential autoconf automake -y
sudo git clone --recursive https://github.com/obgm/libcoap.git
cd libcoap
sudo git checkout dtls
sudo git submodule update --init --recursive
sudo ./autogen.sh
sudo ./configure --disable-documentation --disable-shared
sudo make
sudo make install
cd

-------------------------------------------------------------------------------------------------

create .sh file:
sudo nano /usr/local/bin/rebootTradfri.sh
    add line: 
    coap-client -u XXXXXXXXXXXX -k XXXXXXXXX -v 0 -m post "coaps://XXXXXXXXXXX:5684/15011/9030"

Add Execute permission:
sudo chmod +x /usr/local/bin/rebootTradfri.sh

sudo crontab -e
    and add new line for every day reboot at 5 o'clock:
    0 5 * * * /usr/bin/sudo -H /usr/local/bin/rebootTradfri.sh >> /dev/null 2>&1

sudo reboot

The quick and simple editor for cron schedule expressions by Cronitor:
https://crontab.guru/every-day 
