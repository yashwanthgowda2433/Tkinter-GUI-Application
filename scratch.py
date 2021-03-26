from tkinter import *
from tkinter.messagebox import *
import _tkinter
import tkinter.messagebox
import tkinter as tk
import sys, os
from tkinter import ttk
import cv2
import time
from PIL import ImageTk, Image
import PIL
import numpy as np
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageDraw
window= tk.Tk()
window.title("MVS")
window.geometry('1400x700')

window['bg'] = 'gray'
# lmain = Label(window)
# lmain.grid()
imageFrame = tk.Frame(window, width=17, height=7)
imageFrame.grid(row=0, column=0, padx=400, pady=75)

#Capture video frames
lmain = tk.Label(imageFrame)
# newval =lmain
lmain.grid(row=0, column=0)

cap = cv2.VideoCapture(0)
# newval = cap
def circle_detect(image):
    frame = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1.2, 100)
    # ensure at least some circles were found
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (255, 255, 255), 4)
    return frame
bottom_right = (300, 300)
upper_left = (50, 50)
# GLOBAL VARIABLES
v = DoubleVar()
v1 = DoubleVar()
b = DoubleVar()
h = DoubleVar()
t = DoubleVar()
e = DoubleVar()
ul0 =DoubleVar()
ul1 =DoubleVar()
br0 =DoubleVar()
br1 =DoubleVar()
# contour = DoubleVar()
detection_type = tk.StringVar()
detection_type.set('NO Detection')

rect = (0,0,0,0)
startPoint = False
endPoint = False

def on_mouse(event,x,y,flags,params):

    global rect,startPoint,endPoint

    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:

        if startPoint == True and endPoint == True:
            startPoint = False
            endPoint = False
            rect = (0, 0, 0, 0)

        if startPoint == False:
            rect = (x, y, 0, 0)
            startPoint = True
        elif endPoint == False:
            rect = (rect[0], rect[1], x, y)
            endPoint = True

def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # cv2.namedWindow('frame')

    # img = Image.fromarray('frame',cv2image)
    # cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    if str(detection_type.get()) == 'Edge Detection':
        cv2image = cv2.Canny(cv2image, 100, 200)
    if str(detection_type.get()) == 'Circle Detection':

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(cv2image, cv2.HOUGH_GRADIENT, 1.2, 100)

        if circles is None:
            btn_fail.config(bg='red')
            btn_pass.config(bg='white')
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            btn_pass.config(bg='green')
            btn_fail.config(bg='white')
            if len(circles) > 0:
                print(f"Number of circles Detected= {len(circles)}")
            for (x, y, r) in circles:
                cv2.circle(cv2image, (x, y), r, (255, 255, 255), 4)
    if str(detection_type.get()) == 'Line Detection':
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(cv2image, 75, 150)
        # HoughLines(image, rho, theta, threshold[, lines[, srn[, stn[, min_theta[, max_theta]]]]])
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 30, maxLineGap=250)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(cv2image, (x1, y1), (x2, y2), (0, 0, 128), 1)
    if str(detection_type.get()) == 'Sharpening Detection':
        sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        cv2image = cv2.filter2D(frame, -1, sharpen_filter)
    if str(detection_type.get()) == 'Smoothing Detection':
        kernel = np.ones((15, 15), np.float32) / 225
        cv2image = cv2.filter2D(frame, -1, kernel)
    # if str(detection_type.get()) == 'blur':
    # cv2image = cv2.GaussianBlur(frame, (21, 21), value='blur')
    # canny edge slider
    sel = int(v.get())
    sel2 = int(v1.get())
    if(sel2 > 179):
        sel1 = sel2
    else:
        sel1 = 179
    #print(sel)
    if(sel > 1):
        cv2image = cv2.Canny(cv2image, sel, sel1)
    #end canny edge slider
    # blur
    blurs = int(b.get())
    ksize = (blurs,179)
    if(blurs > 0):
        cv2image = cv2.blur(cv2image, ksize)
    # blur end
    # Hue start
    hue = int(h.get())
    if(hue>0) :
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2HSV)
        cv2image[:, :, 0] += hue
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_HSV2BGR)
        # Hue End
    thresholdValue = int(t.get())
    #maxval = (thresholdValue,255)
    if (thresholdValue > 1):
        cv2image = cv2.threshold(cv2image, thresholdValue,255, cv2.THRESH_BINARY)[1]
    Enhance = int(e.get())
    if(Enhance > 1):
        enh_val = Enhance / 40
        clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
        lab = cv2.cvtColor(cv2image, cv2.COLOR_BGR2LAB)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        cv2image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    if str(detection_type.get()) == 'ROI Detection':
        # Rectangle marker
        r = cv2.rectangle(frame, upper_left, bottom_right, (100, 50, 200), 5)
        # r1 =cv2.rectangle(image_frame, upper_left1, bottom_right1, (50, 30, 100), 4)
        rect_img = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
        # rect_img1 = image_frame[upper_left1[1]: bottom_right1[1], upper_left1[0]: bottom_right1[0]]
        # sketcher_rect = rect_img
        # sketcher_rect = sketch_transform(sketcher_rect)

        circle_rect = rect_img
        # circle_rect = rect_img1
        circle_rect = circle_detect(circle_rect)

        # Conversion for 3 channels to put back on original image (streaming)
        # sketcher_rect_rgb = cv2.cvtColor(sketcher_rect, cv2.COLOR_GRAY2RGB)
        circle_rect_rgb = cv2.cvtColor(circle_rect, cv2.COLOR_GRAY2RGB)
        # circle_rect_rgb1 = cv2.cvtColor(circle_rect, cv2.COLOR_GRAY2RGB)

        # Replacing the sketched image on Region of Interest
        # image_frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]] = sketcher_rect_rgb
        frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]] = circle_rect_rgb
        # image_frame[upper_left1[1]: bottom_right1[1], upper_left1[0]: bottom_right1[0]] = circle_rect_rgb1
        # cv2.imshow(" ROI", frame)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # cv2.imshow(" ROI", circle_rect_rgb1)

    if(int(ul0.get())):
        ul00 = int(ul0.get())
        if (int(ul1.get())):
            ul01 = int(ul1.get())
            if (int(br0.get())):
                br00 = int(br0.get())
                if (int(br1.get())):
                    br01 = int(br1.get())
                    upper_lefts = (ul00, ul01)
                    bottom_rights = (br00, br01)
                    r = cv2.rectangle(frame, upper_lefts, bottom_rights, (100, 50, 200), 5)

                    rect_img = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]

                    circle_rect = rect_img

                    circle_rect = circle_detect(circle_rect)

                    circle_rect_rgb = cv2.cvtColor(circle_rect, cv2.COLOR_GRAY2RGB)

                    frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]] = circle_rect_rgb

                    cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # print(frame)
    cv2.setMouseCallback('frame', on_mouse)

    # drawing rectangle
    if startPoint == True and endPoint == True:
        cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 2)
        print(rect[0])
        print(rect[1])
        print(rect[2])
        print(rect[3])

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1.2, 100)
        # ensure at least some circles were found
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (255, 255, 255), 4)

    # cv2.imshow('frame', frame)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream)

video_stream()

_, frame = cap.read()
# img = cv2.imread('face_person1.jpg')
edge = Image.fromarray(frame)
tk_edge = ImageTk.PhotoImage(edge)
def savefile_jpg():
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    edge.save(filename)
def savefile_bmp():
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".bmp")
    if not filename:
        return
    edge.save(filename)
def snapshot():
    # Get a frame from the video source
    ret, frame = cap.read()

    if ret:
        cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
def roi():
    ret, frame = cap.read()
    r = cv2.rectangle(frame, upper_left, bottom_right, (100, 50, 200), 5)
    rect_img = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
    # sketcher_rect = rect_img
    # sketcher_rect = sketch_transform(sketcher_rect)

    circle_rect = rect_img
    circle_rect = circle_detect(circle_rect)

    # Conversion for 3 channels to put back on original image (streaming)
    # sketcher_rect_rgb = cv2.cvtColor(sketcher_rect, cv2.COLOR_GRAY2RGB)
    circle_rect_rgb = cv2.cvtColor(circle_rect, cv2.COLOR_GRAY2RGB)

    # Replacing the sketched image on Region of Interest
    # image_frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]] = sketcher_rect_rgb
    frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]] = circle_rect_rgb


def OpenFile():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("Text File", ".txt"),("All Files",".*")),
                           title = "Choose a file."
                           )
    print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as UseFile:
            print(UseFile.read())
    except:
        print("No file exists")
#Title = window.title( "File Opener")

#Menu Bar
def donothing():
    x = 0
menu = Menu(window)
window.config(menu=menu)

file = Menu(menu)
help = Menu(menu)
edit= Menu(menu)
file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = lambda:exit())

help.add_command(label="Help Index")
help.add_command(label="About...", command=donothing)


edit.add_command(label="Cut", command=donothing)
edit.add_command(label="Copy", command=donothing)
edit.add_command(label="Past", command=donothing)
edit.add_command(label="Duplicate Line", command=donothing)
edit.add_command(label="Toggle Case", command=donothing)

menu.add_cascade(label = 'File', menu = file)
menu.add_cascade(label="Help", menu=help)
menu.add_cascade(label="Edit",menu=edit)

model_val = tk.StringVar()
canny = tk.Scale(window, label='canny', variable=v, from_=0, to=112, length=152, showvalue=2, orient=tk.HORIZONTAL)
canny.place(x=20, y=75)
canny = tk.Scale(window, label='canny', variable=v1, from_=179, to=200, length=200, orient=tk.HORIZONTAL)
canny.place(x=160, y=75)
# btn = Button(window, text ="Apply Canny Detection", command = video_stream)
# btn.place(x=40, y=140)
# canny.set(179)
blur = tk.Scale(window, variable=b, label='blur', from_=0, to=179, length=350, showvalue=2, orient=tk.HORIZONTAL)
blur.place(x=20, y=140)
thresh = tk.Scale(window, variable=t, label='thresh', from_=0, to=179, length=350, showvalue=2, orient=tk.HORIZONTAL)
thresh.place(x=20, y=200)
Hue = tk.Scale(window, variable=h, label='Hue', from_=0, to=179, length=350, showvalue=2, orient=tk.HORIZONTAL)
Hue.place(x=20, y=260)
Enhance = tk.Scale(window, variable=e,label='Enhance', from_=0, to=179, length=350, showvalue=2, orient=tk.HORIZONTAL)
Enhance.place(x=20, y=320)


Sharpening_Detection = tk.Radiobutton(window, text='Sharpening_Detection', variable=detection_type, value='Sharpening Detection', width=18, height=1)
Sharpening_Detection.place(x=20, y=400)
Smoothing_Detection = tk.Radiobutton(window, text='Smoothing_Detection', variable=detection_type, value='Smoothing Detection', width=18, height=1)
Smoothing_Detection.place(x=20, y=450)
Edge_Detection = tk.Radiobutton(window, text='Edge_Detection', variable=detection_type, value='Edge Detection', width=18, height=1)
Edge_Detection.place(x=20, y=500)
Circle_Detection = tk.Radiobutton(window, text='Circle_Detection', variable=detection_type, value='Circle Detection', width=18, height=1)
Circle_Detection.place(x=20, y=550)
Line_Detection = tk.Radiobutton(window, text='Line_Detection', variable=detection_type, value='Line Detection', width=18, height=1)
Line_Detection.place(x=20, y=600)
ROI_Detection = tk.Radiobutton(window, text='ROI_Detection', variable=detection_type, value='ROI Detection', width=18, height=1,command = roi)
ROI_Detection.place(x=1050, y=400)
#
# contour = ttk.Combobox(window, width=30)
# contour.place(x=1050, y=450)


# btn_roi = tk.Button(window, text='ROI',width=15, height=1,command = roi)
# btn_roi.place(x=1050, y=50)
# btn_close_device = tk.Button(window, text='Close Device', width=15, height=1)
# btn_close_device.place(x=1200, y=50)

btn_start_grabbing = tk.Button(window, text='Start Grabbing', width=15, height=1)
btn_start_grabbing.place(x=1050, y=75)
btn_stop_grabbing = tk.Button(window, text='Stop Grabbing', width=15, height=1)
btn_stop_grabbing.place(x=1200, y=75)


btn_save_bmp = tk.Button(window, text='Save as BMP', width=15, height=1,command=savefile_bmp)
btn_save_bmp.place(x=1050, y=125)
btn_save_jpg = tk.Button(window, text='Save as JPG', width=15, height=1,command=savefile_jpg)
btn_save_jpg.place(x=1200, y=125)
# label_exposure_time = tk.Label(window, text='Exposure Time', width=15, height=1)
# label_exposure_time.place(x=1050, y=175)
# text_exposure_time = tk.Text(window, width=15, height=1)
# text_exposure_time.place(x=1200, y=175)

# label_gain = tk.Label(window, text='Gain', width=15, height=1)
# label_gain.place(x=1050, y=225)
# text_gain = tk.Text(window, width=15, height=1)
# text_gain.place(x=1200, y=225)
#
# label_frame_rate = tk.Label(window, text='Frame Rate', width=15, height=1)
# label_frame_rate.place(x=1050, y=275)
# text_frame_rate = tk.Text(window, width=15, height=1,command = fps)
# text_frame_rate.place(x=1200, y=275)

btn_enum_devices = tk.Button(window, text='Enum Devices', width=35, height=1)
label_exposure_time = tk.Label(window, text='upper_left[0]', width=15, height=1)
label_exposure_time.place(x=1050, y=175)
text_exposure_time = tk.Entry(window, textvariable=ul0, width=15)
text_exposure_time.place(x=1200, y=175)
label_exposure_time = tk.Label(window, text='upper_left[1]', width=15, height=1)
label_exposure_time.place(x=1050, y=225)
text_exposure_time = tk.Entry(window, textvariable=ul1, width=15)
text_exposure_time.place(x=1200, y=225)
label_exposure_time = tk.Label(window, text='bottom_right[0]', width=15, height=1)
label_exposure_time.place(x=1050, y=275)
text_exposure_time = tk.Entry(window, textvariable=br0, width=15)
text_exposure_time.place(x=1200, y=275)
label_exposure_time = tk.Label(window, text='bottom_right[1]', width=15, height=1)
label_exposure_time.place(x=1050, y=325)
text_exposure_time = tk.Entry(window, textvariable=br1, width=15)
text_exposure_time.place(x=1200, y=325)
# detection_type.set(1)



btn_live_feed=tkinter.Button(window, text="Live Feed",width=50,command =video_stream)
btn_live_feed.place(x=400, y=600)
btn_snapshot=tkinter.Button(window, text="Snapshot", width=50,command=snapshot)
btn_snapshot.place(x=400, y=650)


btn_pass= tk.Button(window, text='Pass', width=15, height=1)
btn_pass.place(x=1050, y=600)
btn_fail = tk.Button(window, text='Fail', width=15, height=1)
btn_fail.place(x=1200, y=600)


xVariable = tkinter.StringVar()
window.mainloop()