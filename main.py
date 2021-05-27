from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
import requests
from fake_useragent import UserAgent
import json

get_slots_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
uagent = UserAgent()
browser_header = {'User-Agent': uagent.random}


def scheduled_method():
    print("Starting HTTP call...")
    response = requests.get(get_slots_url,
                            headers=browser_header,
                            params={'pincode': '751024',
                                    'date': f"{datetime.now().strftime('%d-%m-%Y')}"})
    appointment_slots = json.loads(response.content)
    for center in appointment_slots['centers']:
        for session in center.get('sessions'):
            if session.get('min_age_limit') == 18:
                if session.get('available_capacity_dose1') != 0:
                    print(f"Available : {session.get('slots')}")


scheduler = BackgroundScheduler()
kwargs = {'minutes': 30}
scheduler.add_job(scheduled_method, 'interval', id='schedule_method', **kwargs)
scheduler.start()
for i in range(60):
    time.sleep(1)
scheduler.shutdown()
