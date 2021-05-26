from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime


def scheduled_method():
    print(f"[{datetime.now()}]......scheduled process is running")


scheduler = BackgroundScheduler()
kwargs = {'seconds': 30}
scheduler.add_job(scheduled_method, 'interval', id='schedule_method', **kwargs)
scheduler.start()
for i in range(60):
    time.sleep(1)
scheduler.shutdown()
