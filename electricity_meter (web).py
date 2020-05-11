import RPi.GPIO as GPIO
import time
import datetime
import requests

''' script ktery bezi na raspberry a odesila na web-server namerena data '''


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(16,GPIO.IN,GPIO.PUD_UP)

impulse = int(0)
recorded = 0
last=0
increase=0
last_time=0
actual_time=datetime.datetime.now()

while (True): 

    #mereni impulzu
    if(GPIO.input(16) == False):
        if(recorded == 0):
            impulse = impulse + 1
            print("dalsi ",impulse)
            recorded = 1
    else:
        recorded=0

    #mereni prirustku
    if(time.time()>(last_time+60) or last_time==0):
        print("mereni")
        increase=impulse-last #prirustek (celkovy pocet impulzu minus celkovy pri minulem mereni)
        last=impulse
        actual_time=int(time.time())
        #print(impulse)
        print(increase)
        last_time=time.time()
        data_from_pi = {'time': actual_time, 'increase': increase}
        
        try:
            response = requests.post('http://127.0.0.1:5000/api', json=data_from_pi)
            if response.ok:
                print(response.json())
        except:
            print("chyba na serveru")

    
              


