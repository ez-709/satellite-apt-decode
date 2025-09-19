# satellite-apt-decode
**Project Description**

Earth-orbiting meteorological satellites transmit signals that can be received by anyone with appropriate equipment. This includes NOAA and Meteor satellite groups, as well as occasional transmissions from the International Space Station (ISS). 

This project aims to create an autonomous system based on RTL-SDR and Raspberry Pi for:
1. Automatic reception of signals from meteorological satellites (NOAA/Meteor)
2. Decoding data into images
3. Sending results to a Telegram bot for convenient viewing

Satellites transmit on frequencies of 137 MHz and 1.7 GHz, using different signal types: APT, LRPT, and HRPT. Currently, the system is developed for 137 MHz frequency and APT signal type, although adaptation for LRPT signals is a matter of decoder implementation.

Due to the need for object position tracking, significant part of the work involves satellite tracking and orbital prediction.
