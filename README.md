# Tradfri Ikea Gateway auto reboot<br>

I want to restart IKEA Tradfri Gateway every day morning with Raspberry Zero W, <br>
the script with aiocoap creates a command for this idea.<br>

source of my idea: https://github.com/ggravlingen/pytradfri <br>

-------------------------------------------------------------------------------------------------

requirements (aiocoap requires Python '>=3.4.4'):<br>

for all requirements install, use this: $ pip3 install pytradfri[async] typing==3.6.6 <br>
or details:<br>
$ pip3 install aiocoap==0.4a1 DTLSSocket==0.1.7 typing==3.6.6<br>
<br>
if you run without aiocoap-tinydtls ignores error/warrning messages: <br>
$ python3 TradfriGatewayAutoreboot.py 2> /dev/null<br>

#TODO: Change securityid and ip:<br>
securityid = "Asd1Asd2Asd3Asd4" # Security Code - from Gateway (16 characters)<br>
ip = "111.111.1.111"            # your device local ip<br>
<br>
and run :)<br>
<br>
pi@raspberrypi:~ $ python3 TradfriGatewayAutoreboot.py  2> /dev/null <br>
----- HERE IS YOUR COMMAND: coap-client -u XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX -k XXXXXXXXXXXXXXXX -v 0 -m post "coaps://192.168.1.127:5684/15011/9030" ----- <br><br>

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
