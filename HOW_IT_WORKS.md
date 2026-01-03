# How the Scheduler Works

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Python Script Scheduler                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ reads
                              ▼
                  ┌───────────────────────┐
                  │  schedule_config.json │
                  │                       │
                  │  Defines:             │
                  │  - Job names          │
                  │  - Script paths       │
                  │  - When to run        │
                  │  - Enabled/disabled   │
                  └───────────────────────┘
                              │
                              │ schedules
                              ▼
              ┌───────────────────────────────┐
              │    Schedule Library           │
              │    (runs in background)       │
              └───────────────────────────────┘
                              │
                              │ at specified times
                              ▼
              ┌───────────────────────────────┐
              │   Executes Python Scripts     │
              │   - example_task.py           │
              │   - your_script.py            │
              │   - any_script.py             │
              └───────────────────────────────┘
                              │
                              │ logs results
                              ▼
                  ┌───────────────────────┐
                  │   Console Output      │
                  │   + Log Files         │
                  └───────────────────────┘
```

## Execution Flow

### 1. Startup Phase

```
Start scheduler.py
    │
    ├─→ Load schedule_config.json
    │       │
    │       ├─→ Parse JSON
    │       ├─→ Validate jobs
    │       └─→ Store in memory
    │
    ├─→ Schedule each enabled job
    │       │
    │       ├─→ Daily jobs → schedule.every().day.at("09:00")
    │       ├─→ Weekly jobs → schedule.every().monday.at("10:00")
    │       ├─→ Hourly jobs → schedule.every().hour
    │       └─→ Interval jobs → schedule.every(30).minutes
    │
    └─→ Enter main loop
            │
            └─→ while True:
                    check if any job should run
                    execute if due
                    sleep 1 second
                    repeat
```

### 2. Job Execution Phase

```
Time matches schedule
    │
    ├─→ Call run_script(script_path, job_name)
    │       │
    │       ├─→ Print start message with timestamp
    │       │
    │       ├─→ Execute: python script_path
    │       │       │
    │       │       ├─→ Capture stdout (normal output)
    │       │       ├─→ Capture stderr (errors)
    │       │       └─→ Set timeout (5 minutes)
    │       │
    │       ├─→ Check return code
    │       │       │
    │       │       ├─→ Success (0) → Print success + output
    │       │       └─→ Failure (≠0) → Print error + stderr
    │       │
    │       └─→ Print completion message
    │
    └─→ Return to main loop
```

## Job Types Explained

### Daily Schedule
```
Type: "daily"
Time: "09:00"

Timeline:
Mon Tue Wed Thu Fri Sat Sun
 ↓   ↓   ↓   ↓   ↓   ↓   ↓
9AM 9AM 9AM 9AM 9AM 9AM 9AM
```

### Weekly Schedule
```
Type: "weekly"
Day: "monday"
Time: "10:00"

Timeline:
Mon     Tue Wed Thu Fri Sat Sun
 ↓
10AM   (skip until next Monday)
```

### Hourly Schedule
```
Type: "hourly"

Timeline:
12AM 1AM 2AM 3AM ... 11PM 12AM
 ↓    ↓   ↓   ↓  ...  ↓    ↓
run  run run run ... run  run
```

### Interval Schedule
```
Type: "interval"
Minutes: 30

Timeline:
12:00 → 12:30 → 1:00 → 1:30 → 2:00 → ...
  ↓       ↓       ↓       ↓       ↓
 run     run     run     run     run
```

## Configuration Structure

```
schedule_config.json
│
└─── jobs (array)
        │
        ├─── job 1
        │     ├─── name: "Daily Morning Task"
        │     ├─── script: "example_task.py"
        │     ├─── schedule
        │     │     ├─── type: "daily"
        │     │     └─── time: "09:00"
        │     └─── enabled: true
        │
        ├─── job 2
        │     ├─── name: "Weekly Report"
        │     ├─── script: "report.py"
        │     ├─── schedule
        │     │     ├─── type: "weekly"
        │     │     ├─── day: "monday"
        │     │     └─── time: "10:00"
        │     └─── enabled: true
        │
        └─── job 3
              └─── ... (more jobs)
```

## Windows Integration Options

### Option 1: Manual Execution
```
User double-clicks
    │
    ├─→ run_scheduler.bat (Command Prompt)
    │   └─→ python scheduler.py
    │
    └─→ run_scheduler.ps1 (PowerShell)
        └─→ python scheduler.py
```

### Option 2: Startup Folder
```
Windows boots → User logs in
    │
    └─→ shell:startup folder
            │
            └─→ run_scheduler.bat shortcut
                    │
                    └─→ Scheduler starts automatically
```

### Option 3: Task Scheduler (Recommended)
```
Windows Task Scheduler
    │
    ├─→ Trigger: Computer starts / User logs in
    │
    ├─→ Action: Run python.exe scheduler.py
    │
    └─→ Settings:
            ├─→ Run whether user logged on or not
            ├─→ Run with highest privileges
            └─→ Restart on failure
```

## Error Handling

```
Script Execution
    │
    ├─→ Script exists?
    │       No → Print warning, skip
    │       Yes → Continue
    │
    ├─→ Execute script
    │       │
    │       ├─→ Success (return code 0)
    │       │       └─→ Print output, continue
    │       │
    │       ├─→ Failure (return code ≠ 0)
    │       │       └─→ Print error, continue to next job
    │       │
    │       └─→ Timeout (> 5 minutes)
    │               └─→ Kill process, print timeout, continue
    │
    └─→ Return to scheduler loop
```

## File Relationships

```
Project Directory
│
├─ scheduler.py ..................... Main scheduler program
│   │
│   └─→ imports: schedule, subprocess, json, datetime
│
├─ schedule_config.json ............. Job definitions
│   │
│   └─→ read by: scheduler.py
│
├─ example_task.py .................. Example job script
│   │
│   └─→ executed by: scheduler.py
│
├─ requirements.txt ................. Python dependencies
│   │
│   └─→ contains: schedule>=1.2.0
│
├─ run_scheduler.bat ................ Windows batch launcher
│   │
│   └─→ executes: python scheduler.py
│
├─ run_scheduler.ps1 ................ PowerShell launcher
│   │
│   └─→ executes: python scheduler.py
│
└─ Documentation
    ├─ README.md .................... Overview
    ├─ SCHEDULER_README.md .......... Detailed docs
    ├─ QUICKSTART.md ................ Quick start guide
    └─ HOW_IT_WORKS.md .............. This file
```

## Example: Full Cycle

```
1. User starts: python scheduler.py
        ↓
2. Scheduler loads: schedule_config.json
        ↓
3. Finds job: "Daily Morning Task" at 09:00
        ↓
4. Current time: 08:59:45
        ↓
5. Waits...
        ↓
6. Time reaches: 09:00:00
        ↓
7. Executes: python example_task.py
        ↓
8. Script runs:
   - Prints messages
   - Generates random number
   - Writes to task_log.txt
        ↓
9. Script completes successfully
        ↓
10. Scheduler prints: "✓ Job 'Daily Morning Task' completed successfully"
        ↓
11. Returns to waiting for next scheduled time
        ↓
12. Repeat from step 5
```

## Time Checking Logic

```
Every second, scheduler checks:

current_time = now()
for each scheduled_job:
    if current_time matches job.schedule:
        execute(job.script)
        mark as completed
    
sleep(1 second)
repeat
```

## Benefits of This Design

✓ **Simple**: Easy to understand and configure
✓ **Flexible**: Multiple schedule types supported
✓ **Reliable**: Error handling prevents crashes
✓ **Portable**: Works on any Windows system with Python
✓ **Extensible**: Easy to add new job types
✓ **Lightweight**: Minimal resource usage
✓ **Transparent**: Clear logging of all operations

---

**Understanding this flow will help you customize and troubleshoot the scheduler!**
