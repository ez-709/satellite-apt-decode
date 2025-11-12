# satellite-apt-decode - Project Description

This project creates an autonomous system to receive and decode weather satellite signals using an RTL-SDR receiver and a Raspberry Pi. The system is designed to capture transmissions from NOAA and Meteor satellites on the 137 MHz frequency using the APT signal format, convert them into visible images, and send the results to a Telegram bot for easy viewing.

Currently, the following components are functional:

- Automated Satellite Pass Prediction: The system accurately calculates upcoming satellite passes (rise time, culmination, set time, maximum elevation) based on real-time TLE data fetched via HTTP requests from Celestrak, ensuring predictions align with actual satellite positions.
- Integrated Telegram Bot: Provides a user interface for receiving decoded satellite images and accessing system information. The bot allows users to view real-time orbital data, see upcoming satellite passes, and browse the satellite database with filtering and sorting options (by name, time, elevation).
- APT Signal Decoder: Implements decoding logic for the APT signal format used by NOAA satellites, converting wav file into grayscale weather imagery.
- SDR Control Functions: Includes implemented software functions for controlling the RTL-SDR receiver, managing recording parameters, and capturing raw satellite signal data during predicted passes.
- Centralized Configuration Management: All main operational parameters (e.g., bot token, satellite list, pass thresholds, file paths, SDR settings) are managed through a single, operational `config.json` file.

<img width="600" alt="изображение" src="https://github.com/user-attachments/assets/b7f39b9b-4f48-46aa-a0fe-3e165e5d629a" />

*Example output: result of apt decoder work*

The system is designed to run automatically. When a satellite passes overhead, it records the signal, decodes it, and saves the resulting image. The user can then access and view the decoded images and other system information, such as pass logs and satellite data, through the Telegram bot interface.

<img width="599" alt="изображение" src="https://github.com/user-attachments/assets/7af2664c-ceb7-4c6e-b3a9-27a3461e767c" />

*Screenshot: list of upcoming passes with time, satellite name, and maximum elevation and map with orbits.*

<img width="500" alt="изображение" src="https://github.com/user-attachments/assets/13554af8-887e-4082-b5ae-14d3b9b437c3" />

*Screenshot: real-time position and trajectory of active satellites on a world map.*

The next development steps include:

- Refactoring the system architecture so that the Telegram bot and image decoding run on a virtual machine, while the Raspberry Pi handles only signal reception. This improves stability and makes updates easier.
- Ensuring reliable and continuous signal recording during satellite passes, including automatic restarts in case of software or hardware errors.  
- Designing and implementing a suitable antenna for the 137 MHz band to maximize signal quality and reception stability.  
- Optimizing the entire signal reception chain (antenna, RTL-SDR, gain settings, and grounding) to achieve stable and consistent signal capture from weather satellites.

The goal is to build a simple, reliable, and fully autonomous system that requires no daily intervention. It is suitable for learning about satellite communications, signal processing, and embedded systems.
