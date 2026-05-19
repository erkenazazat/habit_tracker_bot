# Habit Tracker Telegram Bot

Telegram bot for tracking daily habits, managing routines, and improving productivity through reminders and structured habit tracking.

---

## Team Members & Contributions

### 1.Erkenaz
- Initial project setup
- Created base files:
  - `config.py` (Telegram bot token setup)
  - `habits.json` (data storage file initialized with `{}`)
  - `models.py` (basic habit manager structure)

---

### 2.Zangar 
- Improved project architecture
- Implemented OOP structure
- Enhanced `models.py`
- Designed interface logic and class structure

---

### 3.Nurasyl
- Implemented event handlers (Telegram bot logic)
- Added background tasks (scheduler / reminders)
- Managed bot interaction flow and user events

---

## Features

- Add daily habits
- Track habit progress
- View active habits
- Delete habits
- Daily reminders
- Interactive Telegram buttons (Inline / Reply keyboards)
- Persistent data storage using JSON
- Background scheduled tasks for notifications

---

## Technologies Used

- Python 3
- pyTelegramBotAPI 
- JSON file storage
- Object-Oriented Programming (OOP)
- APScheduler 

---

## How It Works

1. User sends a command in Telegram
2. Handler processes the request
3. Model updates habit data
4. Data is saved in JSON file
5. Scheduler sends reminders in background

---

## Data Persistence

All user habits are stored in:

`
habits.json
`
Data is saved in JSON format for simplicity and portability.

---
## Background Tasks

The bot uses a scheduler to send periodic reminders about habits and check user activity.

---

## Project Goal

The goal of this project is to help users build better habits through automation, reminders, and structured tracking inside Telegram.
