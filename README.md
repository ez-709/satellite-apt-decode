
# satellite-apt-decode - Project Description

This project creates an autonomous system to receive and decode weather satellite signals using an RTL-SDR receiver and a Raspberry Pi. The system is designed to capture transmissions from NOAA and Meteor satellites on the 137 MHz frequency using the APT signal format, convert them into visible images, and send the results to a Telegram bot for easy viewing.

Currently, the following components are functional:
- A Telegram bot that receives decoded images and provides basic control.
- A satellite pass tracker that calculates when satellites will be visible overhead, with filtering options for satellite name, time, and elevation.
- A database of satellite orbital data (TLEs) that can be updated and sorted.
- A working APT decoder that converts raw radio signals into grayscale weather images.

<img width="600" alt="изображение" src="https://github.com/user-attachments/assets/6ed76a88-6079-4a9c-ad49-5c330f60e0ad" />


The system is designed to run automatically. When a satellite passes overhead, it records the signal, decodes it, and sends the image to the user via Telegram.

The next development steps include:
- Refactoring the system architecture so that the Telegram bot and image decoding run on a virtual machine, while the Raspberry Pi handles only signal reception. This improves stability and makes updates easier.
- Ensuring reliable and continuous signal recording during satellite passes, with automatic restarts if errors occur.
- All main configuration settings - including the Telegram bot token, satellite list, file paths, and pass thresholds - are stored in a single configuration file: config.json.

The goal is to build a simple, reliable, and fully autonomous system that requires no daily intervention. It is suitable for learning about satellite communications, signal processing, and embedded systems, and can serve as a strong project for those interested in aerospace or robotics.
