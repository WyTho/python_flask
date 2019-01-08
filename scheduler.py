import schedule
import time
from datetime import datetime
from models.Schedule import ScheduleModel
from app import app as app
from db import db


def job():
    schedules = ScheduleModel.find_all()
    current_time = datetime.now().strftime('%X')
    print("I'm working... " + current_time)
    current_weekday = datetime.now().weekday()
    for schedule in schedules:
        if schedule.time == current_time:
            print("MATCHING TIMES")
            for schedule_day in schedule.schedule_days:
                print(schedule_day.day + " vs " + current_weekday)
                if current_weekday == schedule_day.day:
                    print("MATCHING DAYS")


def scheduler():
    db.init_app(app)
    app.app_context().push()
    while True:
        # schedule.every(10).seconds.do(job)
        # while True:
        #     schedule.run_pending()
        #
        print(datetime.now().time())
        if datetime.now().time().second == 0:
            print('in scheduler')
            schedule.every(1).minutes.do(job)

            while 1:
                schedule.run_pending()
        elif datetime.now().time().second < 54:
            time.sleep(5)
