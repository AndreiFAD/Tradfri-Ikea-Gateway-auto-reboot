# Tradfri Ikea Gateway Autoreboot

I want to restart IKEA Tradfri Gateway every day morning with Raspberry Zero W, 
the script with aiocoap creates a command for this idea.

-------------------------------------------------------------------------------------------------

source of my idea: https://github.com/ggravlingen/pytradfri <br>

requirements (pip install):<br>

aiocoap==0.4a1<br>
DTLSSocket==0.1.7<br>
typing>=3,<4<br>

output command string:<br>
coap-client -u XXXXXXXXXXXX -k XXXXXXXXX -v 0 -m post "coaps://XXXXXXXXXXX:5684/15011/9030"<br>

-------------------------------------------------------------------------------------------------

For using you need install COAP-CLIENT:<br>

sudo apt-get install libtool git build-essential autoconf automake -y<br>
sudo git clone --recursive https://github.com/obgm/libcoap.git<br>
cd libcoap<br>
sudo git checkout dtls<br>
sudo git submodule update --init --recursive<br>
sudo ./autogen.sh<br>
sudo ./configure --disable-documentation --disable-shared<br>
sudo make<br>
sudo make install<br>
cd<br>

-------------------------------------------------------------------------------------------------

create .sh file:<br>
sudo nano /usr/local/bin/rebootTradfri.sh<br>
    add line:<br> 
    coap-client -u XXXXXXXXXXXX -k XXXXXXXXX -v 0 -m post "coaps://XXXXXXXXXXX:5684/15011/9030"<br>
<br>
Add Execute permission:<br>
sudo chmod +x /usr/local/bin/rebootTradfri.sh<br>

sudo crontab -e<br>
    and add new line for every day reboot at 5 o'clock:<br>
    0 5 * * * /usr/bin/sudo -H /usr/local/bin/rebootTradfri.sh >> /dev/null 2>&1<br>

sudo reboot<br>

The quick and simple editor for cron schedule expressions by Cronitor:<br>
https://crontab.guru/every-day <br>
