# Quick Start Guide - Python Script Scheduler

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install schedule
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Schedule

Edit `schedule_config.json` to define when your scripts should run:

```json
{
    "jobs": [
        {
            "name": "My Daily Task",
            "script": "my_script.py",
            "schedule": {
                "type": "daily",
                "time": "09:00"
            },
            "enabled": true
        }
    ]
}
```

### Step 3: Run the Scheduler

**Windows Command Prompt:**
```cmd
python scheduler.py
```

**Or double-click:**
- `run_scheduler.bat` (Batch file)
- `run_scheduler.ps1` (PowerShell script)

---

## 📋 Common Scheduling Examples

### Run Every Day at 9 AM
```json
{
    "type": "daily",
    "time": "09:00"
}
```

### Run Every Monday at 10 AM
```json
{
    "type": "weekly",
    "day": "monday",
    "time": "10:00"
}
```

### Run Every Hour
```json
{
    "type": "hourly"
}
```

### Run Every 30 Minutes
```json
{
    "type": "interval",
    "minutes": 30
}
```

---

## 🪟 Run on Windows Startup

### Using Task Scheduler (Best Method)

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click **"Create Basic Task"**
3. Name it: "Python Script Scheduler"
4. Trigger: **"When the computer starts"** or **"When I log on"**
5. Action: **"Start a program"**
   - Program: `python.exe`
   - Arguments: `"C:\path\to\scheduler.py"`
   - Start in: `C:\path\to\`
6. Finish!

### Using Startup Folder (Alternative)

1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a shortcut to `run_scheduler.bat` in this folder
3. The scheduler will start when you log in

---

## ✅ Testing Your Setup

### Test 1: Run Example Task
```bash
python example_task.py
```

You should see output and a `task_log.txt` file created.

### Test 2: Check Scheduler Help
```bash
python scheduler.py --help
```

### Test 3: Run Scheduler for 10 Seconds
```bash
python scheduler.py
```

Press `Ctrl+C` after 10 seconds. You should see the scheduled jobs listed.

---

## 🛠️ Creating Your Own Scripts

Create any Python script you want to schedule:

**my_backup.py:**
```python
from datetime import datetime
import shutil

def main():
    print(f"Backup started at {datetime.now()}")
    # Your backup code here
    shutil.copy('important.txt', f'backup_{datetime.now():%Y%m%d}.txt')
    print("Backup completed!")

if __name__ == '__main__':
    main()
```

Then add it to `schedule_config.json`:
```json
{
    "name": "Daily Backup",
    "script": "my_backup.py",
    "schedule": {
        "type": "daily",
        "time": "02:00"
    },
    "enabled": true
}
```

---

## ❓ Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'schedule'`
- **Solution:** Run `pip install schedule`

**Problem:** Script doesn't run
- **Solution:** Check that the script path is correct in `schedule_config.json`
- **Solution:** Make sure `"enabled": true` is set

**Problem:** Need help with configuration
- **Solution:** Run `python scheduler.py --create-example` to create a sample config

**Problem:** Want to run in background without console window
- **Solution:** Use `pythonw scheduler.py` or set up Windows Task Scheduler

---

## 📚 More Information

See [SCHEDULER_README.md](SCHEDULER_README.md) for detailed documentation including:
- All scheduling options
- Windows Task Scheduler setup
- Advanced configuration
- Tips and best practices

---

## 💡 Tips

1. **Test manually first**: Run your script with `python myscript.py` before scheduling
2. **Use absolute paths**: In your scripts, use full file paths like `C:\data\file.txt`
3. **Add logging**: Make your scripts write to log files for debugging
4. **Start simple**: Schedule one task first, then add more
5. **Check the output**: When you run `scheduler.py`, it shows what's scheduled

---

**That's it! You're ready to schedule Python scripts on Windows 11!** 🎉
