"""
Python Script Scheduler for Windows 11
A simple scheduler to run Python scripts at specific days and times.
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
import json
import os


class ScriptScheduler:
    """Manages scheduling and execution of Python scripts."""
    
    def __init__(self, config_file='schedule_config.json'):
        """Initialize the scheduler with a configuration file."""
        self.config_file = config_file
        self.jobs = []
        self.load_config()
    
    def load_config(self):
        """Load schedule configuration from JSON file."""
        if not os.path.exists(self.config_file):
            print(f"Configuration file '{self.config_file}' not found.")
            print("Creating example configuration file...")
            self.create_example_config()
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.jobs = config.get('jobs', [])
                print(f"Loaded {len(self.jobs)} job(s) from configuration.")
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def create_example_config(self):
        """Create an example configuration file."""
        example_config = {
            "jobs": [
                {
                    "name": "Daily Morning Task",
                    "script": "example_task.py",
                    "schedule": {
                        "type": "daily",
                        "time": "09:00"
                    },
                    "enabled": True
                },
                {
                    "name": "Weekly Monday Report",
                    "script": "example_task.py",
                    "schedule": {
                        "type": "weekly",
                        "day": "monday",
                        "time": "10:00"
                    },
                    "enabled": True
                },
                {
                    "name": "Hourly Check",
                    "script": "example_task.py",
                    "schedule": {
                        "type": "hourly"
                    },
                    "enabled": False
                }
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, indent=4)
        print(f"Created example configuration file: {self.config_file}")
    
    def run_script(self, script_path, job_name):
        """Execute a Python script."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running job: {job_name}")
        print(f"Executing script: {script_path}")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"✓ Job '{job_name}' completed successfully")
                if result.stdout:
                    print(f"Output: {result.stdout}")
            else:
                print(f"✗ Job '{job_name}' failed with return code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            print(f"✗ Job '{job_name}' timed out after 5 minutes")
        except Exception as e:
            print(f"✗ Error running job '{job_name}': {e}")
    
    def schedule_job(self, job):
        """Schedule a single job based on its configuration."""
        if not job.get('enabled', True):
            print(f"Skipping disabled job: {job.get('name', 'Unnamed')}")
            return
        
        name = job.get('name', 'Unnamed Job')
        script = job.get('script', '')
        schedule_config = job.get('schedule', {})
        
        if not script:
            print(f"Warning: Job '{name}' has no script defined. Skipping.")
            return
        
        if not os.path.exists(script):
            print(f"Warning: Script '{script}' for job '{name}' not found. Skipping.")
            return
        
        schedule_type = schedule_config.get('type', 'daily')
        time_str = schedule_config.get('time', '09:00')
        
        # Schedule based on type
        if schedule_type == 'hourly':
            schedule.every().hour.do(self.run_script, script, name)
            print(f"Scheduled '{name}' to run every hour")
        
        elif schedule_type == 'daily':
            schedule.every().day.at(time_str).do(self.run_script, script, name)
            print(f"Scheduled '{name}' to run daily at {time_str}")
        
        elif schedule_type == 'weekly':
            day = schedule_config.get('day', 'monday').lower()
            day_func = getattr(schedule.every(), day, None)
            
            if day_func:
                day_func.at(time_str).do(self.run_script, script, name)
                print(f"Scheduled '{name}' to run every {day.capitalize()} at {time_str}")
            else:
                print(f"Warning: Invalid day '{day}' for job '{name}'. Skipping.")
        
        elif schedule_type == 'interval':
            minutes = schedule_config.get('minutes', 30)
            schedule.every(minutes).minutes.do(self.run_script, script, name)
            print(f"Scheduled '{name}' to run every {minutes} minutes")
        
        else:
            print(f"Warning: Unknown schedule type '{schedule_type}' for job '{name}'. Skipping.")
    
    def start(self):
        """Start the scheduler and run indefinitely."""
        print("\n" + "="*60)
        print("Python Script Scheduler for Windows 11")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Schedule all jobs
        for job in self.jobs:
            self.schedule_job(job)
        
        if not schedule.get_jobs():
            print("\nNo jobs scheduled. Please check your configuration.")
            print("Press Ctrl+C to exit.")
        else:
            print(f"\nTotal jobs scheduled: {len(schedule.get_jobs())}")
            print("Press Ctrl+C to stop the scheduler.")
        
        print()
        
        # Run the scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nScheduler stopped by user.")
            print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Python Script Scheduler for Windows 11',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scheduler.py                    # Use default config file
  python scheduler.py -c my_config.json  # Use custom config file
  python scheduler.py --create-example   # Create example config and exit
        """
    )
    
    parser.add_argument(
        '-c', '--config',
        default='schedule_config.json',
        help='Path to configuration file (default: schedule_config.json)'
    )
    
    parser.add_argument(
        '--create-example',
        action='store_true',
        help='Create an example configuration file and exit'
    )
    
    args = parser.parse_args()
    
    if args.create_example:
        scheduler = ScriptScheduler(args.config)
        scheduler.create_example_config()
        print(f"\nExample configuration created: {args.config}")
        print("Edit this file and run the scheduler again.")
        return
    
    scheduler = ScriptScheduler(args.config)
    scheduler.start()


if __name__ == '__main__':
    main()
