"""
Example Python script to be scheduled.
This demonstrates what a scheduled task might look like.
"""

from datetime import datetime
import random


def main():
    """Main function that runs when this script is executed."""
    print("="*50)
    print("Example Scheduled Task Running")
    print("="*50)
    print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Simulate some work
    print("Performing scheduled task...")
    
    # Example: Generate a random number
    random_num = random.randint(1, 100)
    print(f"Generated random number: {random_num}")
    
    # Example: Log something
    with open('task_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Task executed successfully. Random: {random_num}\n")
    
    print("Task completed!")
    print("="*50)


if __name__ == '__main__':
    main()
