# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import random
import smbus
#from Lego import *
import socket
import select
import Adafruit_TCS34725

#myEV3 = ev3.EV3(protocol = ev3.BLUETOOTH, host = '00:16:53:5c:d7:5c')

#for communicating with other agents
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(('192.168.1.224', 12345)) #use its own IP address

#for communicating with Processing
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind(('192.168.1.224', 5204)) #use its own IP address
s2.listen(1)
conn, addr = s2.accept()
print('Connected by', addr)

# for color sensor
while True:
        tcs = Adafruit_TCS34725.TCS34725()
        tcs.set_interrupt(False)
        r, g, b, c = tcs.get_raw_data()
        # Print out the values.
        print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))
        if ((r < 150) and (g > 200) and (b > 270)):
        # Enable interrupts and put the chip back to low power sleep/disabled.
                tcs.set_interrupt(True)
                tcs.disable()
                print('blue')
                path = [3,3,2,4,2,3,2,1]
                break
        elif ((r > 255) and (g < 150) and (b < 150)):
                tcs.set_interrupt(True)
                tcs.disable()
                path = [3,3,1,4,1,3,1,2]
                print('red')
                break

        else:
                path = [0,0,0,0,0,0,0,0]
                time.sleep(1)

#for line tracker
CS = 5
Clock = 25
Address = 24
DataOut = 23

#for ultrasonic range sensor
TRIG = 27
ECHO = 22

#grid system
x = 1
y = 2
dir = "N"


class TRSensor(object):
        def __init__(self,numSensors = 5):
                self.numSensors = numSensors
                self.calibratedMin = [0] * self.numSensors
                self.calibratedMax = [1023] * self.numSensors
                self.last_value = 0

        """
        Reads the sensor values into an array. There *MUST* be space
        for as many values as there were sensors specified in the constructor.
        Example usage:
        unsigned int sensor_values[8];
        sensors.read(sensor_values);
        The values returned are a measure of the reflectance in abstract units,
        with higher values corresponding to lower reflectance (e.g. a black
        surface or a void).
        """
        def AnalogRead(self):
                value = [0,0,0,0,0,0]
                #Read Channel0~channel4 AD value
                for j in range(0,6):
                        GPIO.output(CS, GPIO.LOW)
                        for i in range(0,4):
                                #sent 4-bit Address
                                if(((j) >> (3 - i)) & 0x01):
                                        GPIO.output(Address,GPIO.HIGH)
                                else:
                                        GPIO.output(Address,GPIO.LOW)
                                #read MSB 4-bit data
                                value[j] <<= 1
                                if(GPIO.input(DataOut)):
                                        value[j] |= 0x01
                                GPIO.output(Clock,GPIO.HIGH)
                                GPIO.output(Clock,GPIO.LOW)
                        for i in range(0,6):
                                #read LSB 8-bit data
                                value[j] <<= 1
                                if(GPIO.input(DataOut)):
                                        value[j] |= 0x01
                                GPIO.output(Clock,GPIO.HIGH)
                                GPIO.output(Clock,GPIO.LOW)
                        #no mean ,just delay
                        for i in range(0,6):
                                GPIO.output(Clock,GPIO.HIGH)
                                GPIO.output(Clock,GPIO.LOW)
#                       time.sleep(0.0001)
                        GPIO.output(CS,GPIO.HIGH)
                return value[1:]

        """
        Reads the sensors 10 times and uses the results for
        calibration.  The sensor values are not returned; instead, the
        maximum and minimum values found over time are stored internally
        and used for the readCalibrated() method.
        """
        def calibrate(self):
                max_sensor_values = [0]*self.numSensors
                min_sensor_values = [0]*self.numSensors
                for j in range(0,10):

                        sensor_values = self.AnalogRead();

                        for i in range(0,self.numSensors):

                                # set the max we found THIS time
                                if((j == 0) or max_sensor_values[i] < sensor_values[i]):
                                        max_sensor_values[i] = sensor_values[i]

                                # set the min we found THIS time
                                if((j == 0) or min_sensor_values[i] > sensor_values[i]):
                                        min_sensor_values[i] = sensor_values[i]

                # record the min and max calibration values
                for i in range(0,self.numSensors):
                        if(min_sensor_values[i] > self.calibratedMin[i]):
                                self.calibratedMin[i] = min_sensor_values[i]
                        if(max_sensor_values[i] < self.calibratedMax[i]):
                                self.calibratedMax[i] = max_sensor_values[i]

        """
        Returns values calibrated to a value between 0 and 1000, where
        0 corresponds to the minimum value read by calibrate() and 1000
        corresponds to the maximum value.  Calibration values are
        stored separately for each sensor, so that differences in the
        sensors are accounted for automatically.
        """
        def     readCalibrated(self):
                value = 0
                #read the needed values
                sensor_values = self.AnalogRead();

                for i in range (0,self.numSensors):

                        denominator = self.calibratedMax[i] - self.calibratedMin[i]

                        if(denominator != 0):
                                value = (sensor_values[i] - self.calibratedMin[i])* 1000 / denominator

                        if(value < 0):
                                value = 0
                        elif(value > 1000):
                                value = 1000

                        sensor_values[i] = value

                #print("readCalibrated",sensor_values)
                return sensor_values

        """
        Operates the same as read calibrated, but also returns an
        estimated position of the robot with respect to a line. The
        estimate is made using a weighted average of the sensor indices
        multiplied by 1000, so that a return value of 0 indicates that
        the line is directly below sensor 0, a return value of 1000
        indicates that the line is directly below sensor 1, 2000
        indicates that it's below sensor 2000, etc.  Intermediate
        values indicate that the line is between two sensors.  The
        formula is:

           0*value0 + 1000*value1 + 2000*value2 + ...
           --------------------------------------------
                         value0  +  value1  +  value2 + ...

        By default, this function assumes a dark line (high values)
        surrounded by white (low values).  If your line is light on
        black, set the optional second argument white_line to true.  In
        this case, each sensor value will be replaced by (1000-value)
        before the averaging.
        """
        def readLine(self, alphabot, at_intersection, white_line = 0):

                black_threshold = 200 #to determine if sensor is over black line
                                #adjust based on tests -- sensors values range from 0 - 1000
                maximum = 25
                sleep_time = 0.5
                turn_time = 0.025

                sensor_values = self.readCalibrated()
                avg = 0
                sum = 0
                on_line = 0
                for i in range(0,self.numSensors):
                        value = sensor_values[i]
                        if(white_line):
                                value = 1000-value
                        # keep track of whether we see the line at all
                        if(value > 200):
                                on_line = 1

                        # only average in values that are above a noise threshold
                        if(value > 50):
                                avg += value * (i * 1000);  # this is for the weighted total,
                                sum += value;                  #this is for the denominator

                if(on_line != 1):
##                      # If it last read to the left of center, return 0.
##                      if(self.last_value < (self.numSensors - 1)*1000/2):
##                              #print("left")
##                              return 0;
##
##                      # If it last read to the right of center, return the max.
##                      else:
##                              #print("right")
##                              return (self.numSensors - 1)*1000

                        print("off line")
                        alphabot.stop()
                        time.sleep(sleep_time)

                        if at_intersection:
                                print("Was at T-intersection and chose straight ...")
                                #went straight at a T-intersection and now off line
                                #need to pick new direction
                                rand_num = random.randint(1,2)

                                if rand_num == 1: #right turn
                                        print("right turn!")
                                        alphabot.setPWMB(maximum)
                                        alphabot.right()
                                        while True:
                                                #check sensors to determine when turn complete
                                                #if right most sensor sees black, then back on line
                                                sensor_values = TR.readCalibrated()

                                                if sensor_values[4] > black_threshold:
                                                        break

                                                time.sleep(turn_time)
                                        print("turn done!")
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return (self.numSensors - 1)*1000
                                elif rand_num == 2: #left turn
                                        print("left turn!")
                                        alphabot.setPWMA(maximum)
                                        alphabot.left()
                                        while True:
                                                #check sensors to determine when turn complete
                                                #if left most sensor sees black, then back on line
                                                sensor_values = TR.readCalibrated()

                                                if sensor_values[0] > black_threshold:
                                                        break

                                                time.sleep(turn_time)
                                        print("turn done!")
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return 0
                                else:
                                        print("random number error!")
                                        alphabot.backward()
                                        time.sleep(sleep_time)
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return (self.numSensors - 1)*1000/2
                        else:
                                print("Dead end! U-turn!")
                                alphabot.setPWMA(27)
                                alphabot.setPWMB(27)
                                alphabot.forward()
                                time.sleep(0.4)
                                alphabot.uTurn()
                                while True:
                                        #check sensors to determine when u-turn complete
                                        #u-turn is in clockwise direction
                                        #if right most sensor sees black, then back on line
                                        sensor_values = TR.readCalibrated()

                                        if sensor_values[4] > black_threshold:
                                                break

                                        time.sleep(turn_time)
                                print("turn done!")
                                alphabot.stop()
                                time.sleep(sleep_time)
                                return (self.numSensors - 1)*1000

                self.last_value = avg/sum

                return self.last_value

#use ultrasonic sensor to check for obstacles in front of agent
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



index = 0
#check to see if agent is at an intersection and decide on behavior
def checkIntersect(TR, alphabot, obstacle = False):

        black_threshold = 500 #to determine if sensor is over black line
                                #adjust based on tests -- sensors values range from 0 - 1000
        white_threshold = 200 #to determine if sensor is over white area
                                #adjust based on tests -- sensors values range from 0 - 1000
        right_flag = False #for checking when right turn complete
        left_flag = False #for checking when left turn complete
        backward_flag = False # for checking when backward complete
        maximum = 25
        sleep_time = 0.5
        turn_time = 0.025


        sensor_values = TR.readCalibrated()


        #if all sensors over black line, then agent at 4-way intersection ot T-intersection
        if ((sensor_values[0] >= black_threshold) and (sensor_values[1] >= black_threshold) and
            (sensor_values[2] >= black_threshold) and (sensor_values[3] >= black_threshold) and
            (sensor_values[4] >= black_threshold)):
                print("At 4-way or T-intersection!")
                global index
                print(index)
                alphabot.stop()
                time.sleep(sleep_time)

                if (index <= 7):
                        dir_num = path [index]
                        index = index + 1

                        # update location
                        global dir
                        global x
                        global y

                        print('at', x, ',', y, dir)

                        if dir == "N":
                                if dir_num == 1:
                                        x = x + 1
                                        dir = "E"
                                elif dir_num == 2:
                                        x = x - 1
                                        dir = "W"
                                elif dir_num == 3:
                                        y = y - 1
                        elif dir == "E":
                                elif dir_num == 1:
                                        y = y + 1
                                        dir = "S"
                                elif dir_num == 2:
                                        y = y - 1
                                        dir = "N"
                                elif dir_num == 3:
                                        x = x + 1
                        elif dir == "W":
                                elif dir_num == 1:
                                        y = y - 1
                                        dir = "N"
                                elif dir_num == 2:
                                        y = y + 1
                                        dir = "S"
                                elif dir_num == 3:
                                        x = x - 1
                        elif dir == "S":
                                elif dir_num == 1:
                                        x = x - 1
                                        dir = "W"
                                elif dir_num == 2:
                                        x = x + 1
                                        dir = "E"
                                elif dir_num == 3:
                                        y = y + 1



                        if dir_num == 1: #right turn
                                        print("right turn!")
                                        alphabot.setPWMB(maximum)
                                        alphabot.right()
                                        while True:
                                                #check sensors to determine when turn complete
                                                #agent sometimes overshoots intersection when stopping
                                                #first check if right most sensor sees black
                                                #then if right most sensor sees white after, the turn is complete
                                                sensor_values = TR.readCalibrated()

                                                if sensor_values[4] >= black_threshold:
                                                        right_flag = True

                                                if sensor_values[4] < white_threshold and right_flag:
                                                        break

                                                time.sleep(turn_time)
                                        print("turn done!")
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return True
                        elif dir_num == 2: #left turn
                                        print("left turn!")
                                        alphabot.setPWMA(maximum)
                                        alphabot.left()
                                        while True:
                                                #check sensors to determine when turn complete
                                                #agent sometimes overshoots intersection when stopping
                                                #first check if left most sensor sees black
                                                #then if left most sensor sees white after, the turn is complete
                                                sensor_values = TR.readCalibrated()

                                                if sensor_values[0] >= black_threshold:
                                                        left_flag = True

                                                if sensor_values[0] < white_threshold and left_flag:
                                                        break

                                                time.sleep(turn_time)
                                        print("turn done!")
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return True
                        elif dir_num == 3: #straight
                                        print("straight!")
                                        alphabot.setPWMA(maximum)
                                        alphabot.setPWMB(maximum)
                                        alphabot.forward()
                                        while True:
                                                #check sensors to determine when intersection passed
                                                #if left and right most sensors see white, then intersection passed
                                                sensor_values = TR.readCalibrated()

                                                if ((sensor_values[0] < white_threshold) and
                                                    (sensor_values[4] < white_threshold)):
                                                        break

                                                time.sleep(turn_time)
                                        print("done!")
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return True
                        elif dir_num == 0: #stop
                                        alphabot.stop()
                                        return True
                        elif dir_num == 4: #straight and backward
                                        print("Arrived!")
                                        alphabot.setPWMA(maximum)
                                        alphabot.setPWMB(maximum)
                                        alphabot.forward()
                                        time.sleep(0.5)
                                        alphabot.stop()
                                        time.sleep(5)
                                        alphabot.backward()
                                        while True:
                                                sensor_values = TR.readCalibrated()

                                                if ((sensor_values[0] >= black_threshold) and (sensor_values[1] >= black_threshold) and
                                                    (sensor_values[2] >= black_threshold) and (sensor_values[3] >= black_threshold) and
                                                    (sensor_values[4] >= black_threshold)):
                                                        backward_flag = True
                                                if ((sensor_values[0] < white_threshold) and
                                                    (sensor_values[4] < white_threshold)) and backward_flag:
                                                        break
                                                time.sleep(turn_time)
                                        print("done!")
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return True
                        else:
                                        print("random number error!")
                                        alphabot.backward()
                                        time.sleep(sleep_time)
                                        alphabot.stop()
                                        time.sleep(sleep_time)
                                        return True
                        print('goint to', x, ',', y, dir)
                else:
                        alphabot.stop()
        else:
                return False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Clock,GPIO.OUT)
GPIO.setup(Address,GPIO.OUT)
GPIO.setup(CS,GPIO.OUT)
GPIO.setup(DataOut,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)

# Simple example prints accel/mag data once per second:
try:

        from AlphaBotv2 import AlphaBot

        maximum = 25
        integral = 0;
        last_proportional = 0

        #for obstacle avoidance
        obstacle_dist = 20 #in cm

        #for T-intersection straight choice edge case
        at_intersection = False

        TR = TRSensor()
        Ab = AlphaBot()
        Ab.stop()
        print("Line follow Example")
        time.sleep(0.5)
        for i in range(0,400):
                TR.calibrate()
                print(i)
        print(TR.calibratedMin)
        print(TR.calibratedMax)
        time.sleep(0.5)
        Ab.forward()
        while True:
                while dist() > obstacle_dist:
                        #check if Processing sees another agent
                        processing_ready = select.select([conn], [], [], 0)
                        while processing_ready[0]:
                                data = conn.recv(1024)
                                print(data.decode('utf-8'))
                                if data.decode('utf-8').endswith( 'hello Agent 3'):
                                        print('stop')
                                        #print('going to', x, ',', y, dir)
                                        Ab.stop()
                                        time.sleep(1)
                                        print('restart')
                                        s1.sendto(b'hello Agent 3', ('192.168.1.253', 12345))

                                else:
                                        break
                                processing_ready = select.select([conn], [], [], 0)

                        #check if receiving messages from other agents
                        message_ready = select.select([s1], [], [], 0)
                        while message_ready[0]:
                                message = s1.recv(1024)
                                print(message.decode('utf-8'))
                                if message.decode('utf-8').endswith( 'hello Agent 1'):
                                        print('stop')
                                        Ab.stop()
                                        time.sleep(1)
                                        print('restart')
                                else:
                                        break
                                message_ready = select.select([s1], [], [], 0)

                        #check if at intersection and make decision
                        at_intersection = checkIntersect(TR, Ab)

                        #follow line
                        Ab.forward()
                        position = TR.readLine(Ab, at_intersection)
                        #print(position)

                        # The "proportional" term should be 0 when we are on the line.
                        proportional = position - 2000

                        # Compute the derivative (change) and integral (sum) of the position.
                        derivative = proportional - last_proportional
                        integral += proportional

                        # Remember the last position.
                        last_proportional = proportional

                        '''
                        // Compute the difference between the two motor power settings,
                        // m1 - m2.  If this is a positive number the robot will turn
                        // to the right.  If it is a negative number, the robot will
                        // turn to the left, and the magnitude of the number determines
                        // the sharpness of the turn.  You can adjust the constants by which
                        // the proportional, integral, and derivative terms are multiplied to
                        // improve performance.
                        '''
                        power_difference = proportional/25 + derivative/100 #+ integral/1000;

                        if (power_difference > maximum):
                                power_difference = maximum
                        if (power_difference < - maximum):
                                power_difference = - maximum
                        #print(position,power_difference)
                        if (power_difference < 0):
                                Ab.setPWMB(maximum + power_difference)
                                Ab.setPWMA(maximum);
                        else:
                                Ab.setPWMB(maximum);
                                Ab.setPWMA(maximum - power_difference)
                        # check if arrive destination
                        # if ((curr == 1) and (next == 2)) or ((curr == 2) and (next == 1)):
                        #     time.sleep(3)
                        #     Ab.stop()
                        #     print("arrive yellow destination")
                        #     time.sleep(10)
                Ab.stop()
                print("Obstacle!")
                time.sleep(1)
                at_intersection = checkIntersect(TR, Ab, True)
##                if not at_intersection:
##                        remove_obstacle(myEV3)
##                        time.sleep(1)



except KeyboardInterrupt:
        #conn.close()
        GPIO.cleanup()
