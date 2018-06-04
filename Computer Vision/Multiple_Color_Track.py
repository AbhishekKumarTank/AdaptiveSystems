'''
Created on May 15, 2018

@author: Shashank.bhoite
'''
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label, Entry, LEFT, StringVar
import math

# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Adaptive System")
window.config(background="#FFFFFF")

# Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=2, column=0, padx=10, pady=2)
imageFrame2 = tk.Frame(window, width=600, height=500)
imageFrame2.grid(row=1, column=0, padx=10, pady=2)
imageFrame3 = tk.Frame(window, width=600, height=500)
imageFrame3.grid(row=0, column=0, padx=10, pady=2)
# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
opacity = 0.2
xoff, yoff, zoff, grid = 0, 0, 0, 0


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(cv2image, (600, 480))
    cv2image3 = cv2.resize(cv2image, (640, 480))
    img2 = frame
    img3 = frame.copy()
    img6 = cv2.imread("white.png")
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    xoff, yoff, grid = helloCallBack()
    xoff = int(xoff)
    yoff = int(yoff)
    grid = int(grid)
    hfactor = round((640 / grid))
    vfactor = round((480 / grid))
    cordx = []
    cordy = []
    for i in range(1, 640):
        if (i % hfactor == 0):
            cv2.line(img3, (i, 0), (i, 480), (0, 255, 0), 2, 1)
            # print(i)
    for i in range(1, 480):
        if (i % vfactor == 0):
            cv2.line(img3, (0, i), (640, i), (0, 255, 0), 2, 1)
            # print(i)
    cv2.addWeighted(img3, opacity, img2, 1 - opacity, 0, img3)
    # definig the range of red color
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # defining the Range of Blue color
    blue_lower = np.array([99, 115, 150], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)

    # defining the Range of yellow color
    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    # defining the Range of Blue color
    green_lower = np.array([40, 100, 50], np.uint8)
    green_upper = np.array([80, 255, 255], np.uint8)

    # finding the range of red,blue and yellow color in the image
    red = cv2.inRange(hsv, red_lower, red_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)
    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernal)
    res = cv2.bitwise_and(img2, img2, mask=red)
    blue = cv2.dilate(blue, kernal)
    res1 = cv2.bitwise_and(img2, img2, mask=blue)

    yellow = cv2.dilate(yellow, kernal)
    res2 = cv2.bitwise_and(img2, img2, mask=yellow)
    green = cv2.dilate(green, kernal)
    res3 = cv2.bitwise_and(img2, img2, mask=green)
    cv2.putText(img6, "AGENTS     X" + "   Y    Z   ROW  COLUMN", (50, 85), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 5)
    cv2.putText(img6, "_________________________________", (50, 100), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 5)

    # Tracking the Red Color
    (_, contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 250):
            current_cellx, current_celly = 0, 0
            x, y, w, h = cv2.boundingRect(contour)
            current_cellx = math.ceil(x / hfactor)
            current_celly = math.ceil(y / vfactor)
            img = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            var1 = "red car" + "    " + str(x)
            cv2.putText(img2, "RED CAR X=" + str(x) + ", Y=" + str(y), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255))
            cv2.circle(img3, (x, y), 10, (0, 0, 255), -1)
            cv2.putText(img3, " RED CAR (" + str(round(x / 10)) + "," + str(round(y / 10)) + ")", (x, y),
                        cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255))
            cordx.append(x + xoff)
            cordy.append(yoff)
            cv2.putText(img6, "RED CAR   " + str(x + xoff) + " " + str(y + yoff) + "       " + str(
                current_celly) + "      " + str(current_cellx), (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 5)

    # Tracking the Blue Color
    (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 2000):
            current_cellx, current_celly = 0, 0
            x, y, w, h = cv2.boundingRect(contour)
            current_cellx = math.ceil(x / hfactor)
            current_celly = math.ceil(y / vfactor)
            img = cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img2, "BLUE CAR", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0))
            cv2.circle(img3, (x, y), 10, (255, 0, 0), -1)
            cv2.putText(img3, " BLUE CAR (" + str(round(x / 10)) + "," + str(round(y / 10)) + ")", (x, y),
                        cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0))
            cv2.putText(img6, "BLUE CAR  " + str(x + xoff) + " " + str(y + yoff) + "       " + str(
                current_celly) + "      " + str(current_cellx), (50, 300), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 5)
    # Tracking the green Color
    (_, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 2000):
            current_cellx, current_celly = 0, 0
            x, y, w, h = cv2.boundingRect(contour)
            current_cellx = math.ceil(x / hfactor)
            current_celly = math.ceil(y / vfactor)
            img = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img2, "GREEN  CAR", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0))
            cv2.circle(img3, (x, y), 10, (0, 255, 0), -1)
            # print(x,xoff)
            cv2.putText(img3, " GREEN CAR (" + str(round(x / 10)) + "," + str(round(y / 10)) + ")", (x, y),
                        cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0))
            cv2.putText(img6, "GREEN CAR " + str(x + xoff) + " " + str(y + yoff) + "       " + str(
                current_celly) + "      " + str(current_cellx), (50, 400), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 5)
    # Tracking the yellow Color
    (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            current_cellx, current_celly = 0, 0
            x, y, w, h = cv2.boundingRect(contour)
            current_cellx = math.ceil(x / hfactor)
            current_celly = math.ceil(y / vfactor)
            img = cv2.rectangle(img2, (x, y), (x + w, y + h), (60, 255, 255), 2)
            cv2.putText(img2, "YELLOW CAR", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.2, (60, 255, 255))
            cv2.circle(img3, (x, y), 10, (0, 255, 0), -1)
            cv2.putText(img3, " YELLOW CAR (" + str(round(x / 10)) + "," + str(round(y / 10)) + ")", (x, y),
                        cv2.FONT_HERSHEY_PLAIN, 1.2, (60, 255, 255))
            cv2.putText(img6, "YELLOW CAR " + str(x + xoff) + " " + str(y + yoff) + "       " + str(
                current_celly) + "      " + str(current_cellx), (50, 500), cv2.FONT_HERSHEY_PLAIN, 4, (60, 255, 255), 5)
    img5 = cv2.resize(img2, (320, 240))
    img4 = cv2.resize(img6, (320, 240))
    npv = np.vstack((img5, img4))
    npvc = np.concatenate((img4, img5), axis=0)
    # cv2.imshow("demo",npvc)
    nph = np.hstack((npvc, img3))
    nphc = np.concatenate((npvc, img3), axis=1)
    # cv2.namedWindow('Color Tracking', flags=cv2.WINDOW_GUI_NORMAL)
    # cv2.imshow("Color Tracking",nphc)
    img = Image.fromarray(cv2.cvtColor(nphc, cv2.COLOR_BGR2RGBA))
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


L1 = Label(imageFrame2, text=" OFFSET  ", fg="red", font=("Helvetica", 10))
L1.grid(row=0, column=0, sticky="w")
L3 = Label(imageFrame3, text=" Connect 2018 - Adaptive System Showcase ", fg="blue", font=("Helvetica", 20))
L3.grid(row=0, column=0, sticky="w")
v = StringVar(imageFrame2, value='0')
v2 = StringVar(imageFrame2, value='0')
v3 = StringVar(imageFrame2, value='0')
v4 = StringVar(imageFrame2, value='0')
v5 = StringVar(imageFrame2, value='1')
E1 = Entry(imageFrame2, bd=5, width=8, textvariable=v)
E1.grid(row=0, column=1)
E2 = Entry(imageFrame2, bd=5, width=8, textvariable=v2)
E2.grid(row=0, column=2)
E3 = Entry(imageFrame2, bd=5, width=8, textvariable=v3)
E3.grid(row=0, column=3)
E4 = Entry(imageFrame2, bd=5, width=8, textvariable=v4)
E4.grid(row=0, column=4)


def helloCallBack():
    xoff = E1.get()
    yoff = E2.get()
    grid = E6.get()
    if xoff == "":
        xoff = "0"
    if yoff == "":
        yoff = "0"
    if grid == "" or grid == "0":
        grid = "1"
    # print("OFFSET X="+E1.get()," Y=",E2.get()+" Z="+E3.get()+" Height="+E4.get())
    return xoff, yoff, grid


L2 = Label(imageFrame2, text="   INSTRUCTIONS ", fg="red", font=("Helvetica", 10))
L2.grid(row=0, column=5, sticky="w")
E5 = Entry(imageFrame2, bd=5, width=50, fg="white", bg="white")
E5.grid(row=0, column=6)
B1 = tk.Button(imageFrame2, text=" SUBMIT ", fg="blue", font=("Helvetica", 10), command=helloCallBack)
B1.grid(row=0, column=7)
L5 = Label(imageFrame2, text=" GRID-SIZE ", fg="red", font=("Helvetica", 10))
L5.grid(row=0, column=8, sticky="w")
E6 = Entry(imageFrame2, bd=5, width=8, textvariable=v5)
E6.grid(row=0, column=9)
# Slider window (slider controls stage position)
'''sliderFrame = tk.Frame(window, width=600, height=100)
sliderFrame.grid(row = 600, column=0, padx=10, pady=2)'''
#show_frame()  # Display 2
window.mainloop()  # Starts GUI
