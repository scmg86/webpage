# webpage.github.io

This repository contains a simple webpage and a Python Script Scheduler for Windows 11.

## Python Script Scheduler

A lightweight tool to schedule Python scripts to run at specific days and times on Windows 11.

### Quick Start

1. Install: `pip install -r requirements.txt`
2. Run: `python scheduler.py`

See [QUICKSTART.md](QUICKSTART.md) for a quick guide or [SCHEDULER_README.md](SCHEDULER_README.md) for full documentation.

### Features

- ⏰ Schedule scripts daily, weekly, hourly, or at custom intervals
- 📝 Simple JSON configuration
- 🪟 Windows 11 compatible
- 🔄 Runs continuously in background
- 📋 Built-in logging and error handling

### Example

```json
{
    "name": "Daily Report",
    "script": "generate_report.py",
    "schedule": {
        "type": "daily",
        "time": "09:00"
    },
    "enabled": true
}
```
