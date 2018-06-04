import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot
import smbus
from Lego import *
myEV3 = ev3.EV3(protocol=ev3.USB, host='00:16:53:56:0B:18')
Ab = AlphaBot()

DR = 16
DL = 19
TRIG = 22
ECHO = 27
def dist():
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
		pass
	t1 = time.time()
	while GPIO.input(ECHO):
		pass
	t2 = time.time()
	return (t2-t1)*34000/2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)

Ab.stop()
try:
        while True:
                obstacle_distance=dist();
                if(obstacle_distance<=35 and obstacle_distance>30):
                    print(obstacle_distance)
                    #Ab.set_speed(28,28)
                    DR_status = GPIO.input(DR)
                    DL_status = GPIO.input(DL)
                    if((DL_status == 1) and (DR_status == 1)):
                        Ab.forward()
                        print("forward")
                    elif((DL_status == 0) and (DR_status == 1)):
                        Ab.right()
                        print("right")
                    elif((DL_status == 1) and (DR_status == 0)):
                        Ab.left()
                        print("left")
                    elif((DL_status == 0) and (DR_status == 0)):
                        Ab.stop()
                        print("stop")
                        time.sleep(2)
                        Ab.right()
                        time.sleep(.8)
                elif(obstacle_distance<=30 and obstacle_distance>25):
                    print(obstacle_distance)
                    #Ab.set_speed(26,26)
                    DR_status = GPIO.input(DR)
                    DL_status = GPIO.input(DL)
                    if((DL_status == 1) and (DR_status == 1)):
                            Ab.forward()
                            print("forward")
                    elif((DL_status == 0) and (DR_status == 1)):
                            Ab.right()
                            print("right")
                    elif((DL_status == 1) and (DR_status == 0)):
                            Ab.left()
                            print("left")
                    elif((DL_status == 0) and (DR_status == 0)):
                            Ab.stop()
                            print("stop")
                            time.sleep(2)
                            Ab.right()
                            time.sleep(.9)
                elif(obstacle_distance<=25 and obstacle_distance>18):
                    print(obstacle_distance)
                    #Ab.set_speed(25,25)
                    DR_status = GPIO.input(DR)
                    DL_status = GPIO.input(DL)
                    if((DL_status == 1) and (DR_status == 1)):
                            Ab.forward()
                            print("forward")
                    elif((DL_status == 0) and (DR_status == 1)):
                            Ab.right()
                            print("right")
                    elif((DR_status == 0) and (DL_status == 1)):
                            Ab.left()
                            print("left")
                    elif((DL_status == 0) and (DR_status == 0)):
                            Ab.stop()
                            print("stop")
                            time.sleep(2)
                            Ab.right()
                            time.sleep(1)
                elif(obstacle_distance<=18):
                    print(obstacle_distance)
                    Ab.stop()
                    time.sleep(10)
                    new_dist = dist()
                    if(new_dist <= 18):
                            Ab.stop()
                            remove_obstacle(myEV3)
                else:
                        DR_status = GPIO.input(DR)
                        DL_status = GPIO.input(DL)
                        if((DL_status == 1) and (DR_status == 1)):
                                Ab.forward()
                                print("forward")
                                print(DL_status,DR_status)
                        elif((DL_status == 0) and (DR_status == 1)):
                                Ab.right()
                                print("right")
                                print(DL_status,DR_status)
                        elif((DL_status == 1) and (DR_status == 0)):
                                Ab.left()
                                print("left")
                                print(DL_status,DR_status)
                        elif((DL_status == 0) and (DR_status == 0)):
                                Ab.stop()
                                print("stop")
                                time.sleep(2)
                                Ab.forward()
                                time.sleep(.4)
				
          

except KeyboardInterrupt:
	GPIO.cleanup();



