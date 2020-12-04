import schedule
import time






while True:
    schedule.every().minute.do(job)
    time.sleep(1)
    print("hehe")

