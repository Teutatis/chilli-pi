# chilli-pi
Chilli-Pi Project - Automated support and monitoring of a chilli plant.

*****BLURP*****

PREREQUISITES

1) Clean install of latest Raspien build
- Ensure latest build
sudo apt-get update
sudo apt-get dist-upgrade
2) Install drivers for Adafruit breakout boards
- Install Adafruit_Python_GPIO package with;
sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
- Install Adafruit BME280 package with;
****clone command for git *****
https://github.com/adafruit/Adafruit_Python_BME280 ******
****check its working with ***** python Adafruit_BME280_Example.py


??? Is it worth adding test as you build steps, to ensure that once
the part has been wired up and the drivers installed, that it works.
Should help with bad build skills. e.g. If BME280 fails to respond to
a basic test program then the wiring should be checked.
