# Python Script Scheduler for Windows 11

A simple, lightweight Python-based scheduler to run Python scripts at specific days and times on Windows 11.

## Features

- 📅 Schedule scripts to run daily, weekly, hourly, or at custom intervals
- ⚙️ Easy JSON configuration
- 🔄 Runs continuously in the background
- 📝 Built-in logging and error handling
- 🪟 Windows 11 compatible

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the schedule library directly:

```bash
pip install schedule
```

### 2. Create Configuration

The scheduler uses a JSON configuration file to define scheduled tasks. An example configuration file (`schedule_config.json`) is included.

To create a new example configuration:

```bash
python scheduler.py --create-example
```

### 3. Run the Scheduler

```bash
python scheduler.py
```

Or with a custom configuration file:

```bash
python scheduler.py -c my_schedule.json
```

## Configuration Format

The configuration file (`schedule_config.json`) defines all scheduled jobs:

```json
{
    "jobs": [
        {
            "name": "Daily Morning Task",
            "script": "example_task.py",
            "schedule": {
                "type": "daily",
                "time": "09:00"
            },
            "enabled": true
        },
        {
            "name": "Weekly Monday Report",
            "script": "example_task.py",
            "schedule": {
                "type": "weekly",
                "day": "monday",
                "time": "10:00"
            },
            "enabled": true
        },
        {
            "name": "Every 30 Minutes",
            "script": "my_script.py",
            "schedule": {
                "type": "interval",
                "minutes": 30
            },
            "enabled": true
        },
        {
            "name": "Hourly Task",
            "script": "another_script.py",
            "schedule": {
                "type": "hourly"
            },
            "enabled": true
        }
    ]
}
```

### Schedule Types

#### Daily
Runs every day at a specific time:
```json
{
    "type": "daily",
    "time": "09:00"
}
```

#### Weekly
Runs on a specific day of the week at a specific time:
```json
{
    "type": "weekly",
    "day": "monday",
    "time": "10:00"
}
```

Valid days: `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`

#### Hourly
Runs every hour:
```json
{
    "type": "hourly"
}
```

#### Interval
Runs at a custom minute interval:
```json
{
    "type": "interval",
    "minutes": 30
}
```

### Job Properties

- **name**: Descriptive name for the job (for logging)
- **script**: Path to the Python script to execute (relative or absolute)
- **schedule**: Schedule configuration (see types above)
- **enabled**: `true` or `false` - whether the job should run

## Running as a Background Service on Windows

### Option 1: Use Windows Task Scheduler (Recommended)

1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Basic Task**
3. Name: "Python Script Scheduler"
4. Trigger: **When the computer starts** or **When I log on**
5. Action: **Start a program**
   - Program: `python.exe` (or full path like `C:\Python311\python.exe`)
   - Arguments: `C:\path\to\scheduler.py`
   - Start in: `C:\path\to\` (folder containing scheduler.py)
6. Check **"Run whether user is logged on or not"** for background execution
7. Click Finish

### Option 2: Create a Batch File

Create a file called `run_scheduler.bat`:

```batch
@echo off
cd /d "%~dp0"
python scheduler.py
pause
```

Then create a shortcut to this batch file in your Startup folder:
- Press `Win + R`
- Type: `shell:startup`
- Create a shortcut to `run_scheduler.bat` in this folder

### Option 3: Use pythonw (No Console Window)

```batch
pythonw scheduler.py
```

This runs the scheduler without showing a console window.

## Example Scripts

### example_task.py

A simple example script that logs execution:

```python
from datetime import datetime

def main():
    print(f"Task executed at {datetime.now()}")
    
    with open('task_log.txt', 'a') as f:
        f.write(f"{datetime.now()} - Task completed\n")

if __name__ == '__main__':
    main()
```

### Create Your Own Scripts

Your scheduled scripts can do anything:
- Send emails or notifications
- Backup files
- Process data
- Web scraping
- Database maintenance
- System monitoring
- And more!

## Command Line Options

```
python scheduler.py [OPTIONS]

Options:
  -c, --config FILE      Use custom configuration file (default: schedule_config.json)
  --create-example       Create an example configuration file and exit
  -h, --help            Show help message
```

## Examples

### Example 1: Daily Backup Script

```json
{
    "name": "Daily Backup",
    "script": "backup.py",
    "schedule": {
        "type": "daily",
        "time": "02:00"
    },
    "enabled": true
}
```

### Example 2: Business Days Report

```json
{
    "name": "Monday Report",
    "script": "generate_report.py",
    "schedule": {
        "type": "weekly",
        "day": "monday",
        "time": "08:00"
    },
    "enabled": true
}
```

### Example 3: Frequent Monitoring

```json
{
    "name": "System Monitor",
    "script": "monitor.py",
    "schedule": {
        "type": "interval",
        "minutes": 15
    },
    "enabled": true
}
```

## Troubleshooting

### Script Not Running

1. Check that the script path in the configuration is correct
2. Verify the script exists and is executable
3. Check the console output for error messages
4. Ensure the `schedule` library is installed: `pip install schedule`

### Time Format

- Use 24-hour format: "09:00", "14:30", "23:45"
- Use HH:MM format (hour:minute)

### Scripts Timeout

- Default timeout is 5 minutes per script
- Long-running scripts should implement their own background processing

### Permissions

- Ensure the scheduler has permission to execute the Python scripts
- If using Task Scheduler, run with appropriate user privileges

## System Requirements

- Windows 11 (also works on Windows 10)
- Python 3.7 or higher
- `schedule` library

## License

This is a simple utility script provided as-is for educational and practical purposes.

## Tips

1. **Test your scripts**: Run them manually before scheduling to ensure they work
2. **Use logging**: Have your scripts write to log files for debugging
3. **Start simple**: Begin with one scheduled task and add more gradually
4. **Monitor execution**: Check logs periodically to ensure tasks are running
5. **Handle errors**: Make your scripts robust with try-except blocks
6. **Absolute paths**: Use full paths for files in your scripts to avoid issues

## Support

For issues or questions, please refer to the documentation of the `schedule` library:
https://schedule.readthedocs.io/
