#!/usr/bin/python3

import time
import datetime
import threading
import schedule
import tinytuya

### TUYA platform connection & outlets start
# Connect to Tuya Cloud
c = tinytuya.Cloud(apiRegion="eu",apiKey="##############",apiSecret="################")
# Outlet(s)
TY_Outlet_1 = "##############"
### TUYA platform connection & outlets end

# Time display tool
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Tuya Device Check
def TuyaDisplayStatusOfDevice(device):
    print(f"{get_current_time()} Tuya Display Status of Device starts..")
    time.sleep(0.5)
    result = c.getstatus(device)
    print(f"Status of device:\n {result}")
    time.sleep(0.5)
    print("Tuya Display Status of Device End")

# TUYA command e.g. TY_Outlet_1,"switch_1",True 
def sendcommand(outlet,switch,value):
    print(f"{get_current_time()} Sending switch command starts...")
    print(f"Arguemnts: outlet: {outlet}, switch: {switch}, value: {value}")
    result = c.sendcommand(outlet,{"commands": [{"code": switch, "value": value},]})
    print(f"Results\n: {result}")
    print("Sending switch command End")



# SCHEDULE
def initialize_schedule():
    print(f"{get_current_time()} initializing schedule...")
    # Turn ON port 2 from outlet 1 on every friday at 18:00 o'clock
    schedule.every().friday.at("18:00").do(lambda: sendcommand(TY_Outlet_1,"switch_2",True))
    # Turn OFF port 2 from outlet 1 on every sunday at 18:00 o'clock
    schedule.every().sunday.at("18:00").do(lambda: sendcommand(TY_Outlet_1,"switch_2",False))

def schedule_thread():
    print(f"{get_current_time()} running schedule_thread...")
    while True:
        schedule.run_pending()
        time.sleep(10)

#MAIN PROGRAM
if __name__ == '__main__':
    TuyaDisplayStatusOfDevice(TY_Outlet_1)
    initialize_schedule()
    print(f"{get_current_time()} starting schedule_thread...")
    threading.Thread(target=schedule_thread, daemon=True).start()
