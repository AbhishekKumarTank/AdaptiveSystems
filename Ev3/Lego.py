#!/usr/bin/env python3
from subprocess import call
import ev3
import time 

def move(speed: int, turn: int) -> None:
    global myEV3, stdscr
    
    if turn > 0:
        speed_right = speed
        speed_left  = round(speed * (1 - turn / 100))
    else:
        speed_right = round(speed * (1 + turn / 100))
        speed_left  = speed
        ops = b''.join([
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_B),              # NOS
        ev3.LCX(speed_right),             # SPEED
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_C),              # NOS
        ev3.LCX(speed_left),              # SPEED
        ev3.opOutput_Start,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_B + ev3.PORT_C)  # NOS
    ])
    myEV3.send_direct_cmd(ops)
def move_turn(speed: int, turn: int) -> None:
    global myEV3, stdscr
    
    if turn > 0:
        speed_right = speed
        speed_left  = -speed
        
    else:
        
        speed_right = -speed
        speed_left  = speed
        ops = b''.join([
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_B),              # NOS
        ev3.LCX(speed_right),             # SPEED
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_C),              # NOS
        ev3.LCX(speed_left),              # SPEED
        ev3.opOutput_Start,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_B + ev3.PORT_C)  # NOS
    ])
    myEV3.send_direct_cmd(ops) 

def pick(speed: int, turn: int) -> None:
    global myEV3, stdscr
    
    if turn > 0:
        speed_right = speed
        speed_left  = round(speed * (1 - turn / 100))
    else:
        speed_right = speed
        speed_left  = speed
    ops = b''.join([
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A),              # NOS
        ev3.LCX(speed_right),             # SPEED
        
        ev3.opOutput_Start,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A)  # NOS
    ])
    myEV3.send_direct_cmd(ops)

def stop() -> None:
    global myEV3, stdscr
    
    ops = b''.join([
        ev3.opOutput_Stop,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_B + ev3.PORT_C), # NOS
        ev3.LCX(0)                        # BRAKE
    ])
    myEV3.send_direct_cmd(ops)



def remove_obstacle(eV3):
	try:
		global myEV3 
		myEV3 = eV3
		speed = 0
		turn  = 0
		#myEV3 = ev3.EV3(protocol=ev3.USB, host='00:16:53:56:0B:18')
		flag = ""
		move(30, 0)
		time.sleep(3)
		stop()
		time.sleep(1)
		pick(30, 0)
		time.sleep(2)
		stop()
		time.sleep(1)
		move(-30, 0)
		time.sleep(3)
		stop()
		time.sleep(1)
		pick(-30, 0)
		time.sleep(2)

	except:
		print("Lego is called")
		pass


