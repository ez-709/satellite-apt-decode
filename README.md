# satellite-apt-decode - Project Description
This project creates an autonomous system to receive and decode weather satellite signals using an RTL-SDR receiver and a Raspberry Pi. The system is designed to capture transmissions from NOAA and Meteor satellites on the 137 MHz frequency using the APT signal format, convert them into visible images, and send the results to a Telegram bot for easy viewing.

Currently, the following components are functional:
- Automated Satellite Pass Prediction: The system accurately calculates upcoming satellite passes (rise time, culmination, set time, maximum elevation) based on real-time TLE data fetched via HTTP requests from Celestrak, ensuring predictions align with actual satellite positions.
- Integrated Telegram Bot: Provides a user interface for receiving decoded satellite images and accessing system information. The bot allows users to view real-time orbital data, see upcoming satellite passes, and browse the satellite database with filtering and sorting options (by name, time, elevation).
- APT Signal Decoder: Implements decoding logic for the APT signal format used by NOAA satellites, converting wav file into grayscale weather imagery.
- SDR Control Functions: Includes implemented software functions for controlling the RTL-SDR receiver, managing recording parameters, and capturing raw satellite signal data during predicted passes.
- Centralized Configuration Management: All main operational parameters (e.g., bot token, satellite list, pass thresholds, file paths, SDR settings) are managed through a single, operational `config.json` file.

<img width="600" alt="изображение" src="https://github.com/user-attachments/assets/b7f39b9b-4f48-46aa-a0fe-3e165e5d629a" />

Example output: result of apt decoder work

The system is designed to run automatically. When a satellite passes overhead, it records the signal, decodes it, and saves the resulting image. The user can then access and view the decoded images and other system information, such as pass logs and satellite data, through the Telegram bot interface.

<img width="599" alt="изображение" src="https://github.com/user-attachments/assets/7af2664c-ceb7-4c6e-b3a9-27a3461e767c" />

*Screenshot: list of upcoming passes with time, satellite name, and maximum elevation and map with orbits.*

<img width="500" alt="изображение" src="https://github.com/user-attachments/assets/13554af8-887e-4082-b5ae-14d3b9b437c3" />

Screenshot: real-time position and trajectory of active satellites on a world map.

## Installation & Launch

The system is started by running `main.py`:

```bash
python main.py
```

### Configuration

Before the first launch, all operational parameters must be set in `config.json`, located in the project root. This includes your observer coordinates, timezone, calculation parameters, your Telegram bot token, and the name of the Python virtual environment to use.

Example `config.json`:

```json
{
  "observer longitude": 37.6176,
  "observer latitude": 55.7558,
  "observer altitude": 150.0,
  "time zone utc": 3,
  "step": 120,
  "calculations for next (hours)": 48,
  "telegram bot token": "YOUR_TELEGRAM_BOT_TOKEN",
  "venv name": ".venv"
}
```

Field description:

| Field | Description |
|---|---|
| `observer longitude` / `observer latitude` | Coordinates of your receiving station (degrees) |
| `observer altitude` | Altitude of your station above sea level (meters) |
| `time zone utc` | UTC offset used for displaying pass times |
| `step` | Time step (in seconds) used for pass calculation |
| `calculations for next (hours)` | Prediction horizon for upcoming satellite passes |
| `telegram bot token` | Token of your Telegram bot, obtained from [@BotFather](https://t.me/BotFather) |
| `venv name` | Name/path of the Python virtual environment used to run the project |

## Next development steps

- Refactoring the system architecture so that the Telegram bot and image decoding run on a virtual machine, while the Raspberry Pi handles only signal reception. This improves stability and makes updates easier.
- Ensuring reliable and continuous signal recording during satellite passes, including automatic restarts in case of software or hardware errors.
- Designing and implementing a suitable antenna for the 137 MHz band to maximize signal quality and reception stability.
- Optimizing the entire signal reception chain (antenna, RTL-SDR, gain settings, and grounding) to achieve stable and consistent signal capture from weather satellites.
  
---

# satellite-apt-decode - Описание проекта

Этот проект представляет собой автономную систему приёма и декодирования сигналов метеорологических спутников с помощью RTL-SDR приёмника и Raspberry Pi. Система принимает передачи спутников NOAA и Meteor на частоте 137 МГц в формате APT, преобразует их в изображения и отправляет результат в Telegram-бота для удобного просмотра.

На данный момент реализованы следующие компоненты:
- Автоматический расчёт пролётов спутников: система точно рассчитывает время восхода, кульминации и захода, а также максимальную элевацию предстоящих пролётов на основе актуальных TLE-данных, получаемых по HTTP с Celestrak.
- Встроенный Telegram-бот: предоставляет интерфейс для получения декодированных изображений и информации о системе. Бот позволяет просматривать актуальные орбитальные данные, список ближайших пролётов, а также базу спутников с фильтрацией и сортировкой (по имени, времени, элевации).
- Декодер сигнала APT: реализует логику декодирования формата APT, используемого спутниками NOAA, преобразуя wav-файл в чёрно-белое изображение.
- Функции управления SDR: реализованы функции управления RTL-SDR приёмником, настройки параметров записи и захвата сырых данных сигнала во время предсказанных пролётов.
- Централизованное управление конфигурацией: все основные параметры работы (токен бота, список спутников, пороги пролётов, пути к файлам, настройки SDR) хранятся в едином файле `config.json`.

<img width="600" alt="изображение" src="https://github.com/user-attachments/assets/b7f39b9b-4f48-46aa-a0fe-3e165e5d629a" />

Пример результата работы декодера APT

Система работает полностью автоматически. Когда спутник пролетает над станцией, система записывает сигнал, декодирует его и сохраняет полученное изображение. Пользователь может просматривать изображения и другую информацию о системе — журналы пролётов, данные спутников — через интерфейс Telegram-бота.

<img width="599" alt="изображение" src="https://github.com/user-attachments/assets/7af2664c-ceb7-4c6e-b3a9-27a3461e767c" />

*Скриншот: список предстоящих пролётов с временем, названием спутника, максимальной элевацией и карта с орбитами.*

<img width="500" alt="изображение" src="https://github.com/user-attachments/assets/13554af8-887e-4082-b5ae-14d3b9b437c3" />

Скриншот: положение и траектория спутников в реальном времени на карте мира.

## Установка и запуск

Запуск системы производится из файла `main.py`:

```bash
python main.py
```

### Настройка

Перед первым запуском необходимо задать все рабочие параметры в файле `config.json`, расположенном в корне проекта. Сюда входят координаты вашей станции наблюдения, часовой пояс, параметры расчёта, токен Telegram-бота и название виртуального окружения Python.

Пример `config.json`:

```json
{
  "observer longitude": 37.6176,
  "observer latitude": 55.7558,
  "observer altitude": 150.0,
  "time zone utc": 3,
  "step": 120,
  "calculations for next (hours)": 48,
  "telegram bot token": "ВАШ_ТОКЕН_TELEGRAM_БОТА",
  "venv name": ".venv"
}
```

Описание полей:

| Поле | Описание |
|---|---|
| `observer longitude` / `observer latitude` | Координаты вашей приёмной станции (в градусах) |
| `observer altitude` | Высота станции над уровнем моря (в метрах) |
| `time zone utc` | Смещение UTC для отображения времени пролётов |
| `step` | Шаг по времени (в секундах) при расчёте пролётов |
| `calculations for next (hours)` | Горизонт прогнозирования предстоящих пролётов |
| `telegram bot token` | Токен вашего Telegram-бота, полученный у [@BotFather](https://t.me/BotFather) |
| `venv name` | Название/путь виртуального окружения Python, используемого для запуска проекта |

## Дальнейшие шаги разработки

- Рефакторинг архитектуры системы: Telegram-бот и декодирование изображений будут работать на виртуальной машине, а Raspberry Pi будет заниматься только приёмом сигнала. Это повысит стабильность и упростит обновления.
- Обеспечение надёжной непрерывной записи сигнала во время пролётов, включая автоматический перезапуск при программных или аппаратных сбоях.
- Проектирование и изготовление подходящей антенны для диапазона 137 МГц для максимального качества и стабильности приёма.
- Оптимизация всего тракта приёма сигнала (антенна, RTL-SDR, настройки усиления, заземление) для стабильного и качественного захвата сигнала со спутников.
