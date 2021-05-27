from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import time
from datetime import datetime
import requests
from fake_useragent import UserAgent
import json
import pywhatkit

get_slots_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
uagent = UserAgent()
browser_header = {'User-Agent': uagent.random}


async def scheduled_method():
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
                    message = f"{session.get('vaccine')} is available, " \
                              f"Available dose : {session.get('available_capacity_dose1')}, " \
                              f"Available Place : {center.get('name')}, " \
                              f"Address : {center.get('address')}"
                    print(message)
                    pywhatkit.sendwhatmsg("you contact number with country code", message,
                                          time_hour=int(datetime.now().strftime('%H')),
                                          time_min=int(datetime.now().strftime('%M')) + 1,
                                          wait_time=0)
    print("Ending HTTP call")


scheduler = AsyncIOScheduler()
scheduler.add_job(scheduled_method, 'interval', minutes=10)
scheduler.start()
print("System interrupt to halt execution")
try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
