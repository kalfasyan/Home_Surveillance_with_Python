# USAGE
# python pi_surveillance.py --conf conf.json

import io
import time
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import numpy as np
import os
import scipy.misc
import picamera
from base_camera import BaseCamera
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():

        with picamera.PiCamera() as camera:
            camera.vflip = True
            # construct the argument parser and parse the arguments
            ap = argparse.ArgumentParser()
            ap.add_argument("-c", "--conf", required=True,
                help="path to the JSON configuration file")
            args = vars(ap.parse_args())

            # filter warnings, load the configuration and initialize the Dropbox
            # client
            warnings.filterwarnings("ignore")
            conf = json.load(open(args["conf"]))
            # let camera warm up
            print("[INFO] warming up...")
            time.sleep(conf["camera_warmup_time"])

            # initialize the camera and grab a reference to the raw camera capture
            camera.resolution = tuple(conf["resolution"])
            camera.framerate = conf["fps"]
            rawCapture = io.BytesIO()

            # allow the camera to warmup, then initialize the average frame, last
            # uploaded timestamp, and frame motion counter
            avg = None
            lastUploaded = datetime.datetime.now()
            motionCounter = 0
            imgCounter = 0
            
            # capture frames from the camera
            for _ in camera.capture_continuous(rawCapture, format="jpeg", use_video_port=True):
                # grab the raw NumPy array representing the image and initialize
                # the timestamp and occupied/unoccupied text
                rawCapture.seek(0)
                yield rawCapture.read()

                data = np.fromstring(rawCapture.getvalue(), dtype=np.uint8)
                # "Decode" the image from the array, preserving colour
                frame = cv2.imdecode(data, 1)

                rawCapture.seek(0)
                rawCapture.truncate(0)

                timestamp = datetime.datetime.now()
                text = "No motion detected.."

                # resize the frame, convert it to RGB,
                # and make a grayscale copy and blur it
                frame = cv2.cvtColor(imutils.resize(frame, width=500), cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # if the average frame is None, initialize it
                if avg is None:
                    print("[INFO] starting background model...")
                    avg = gray.copy().astype("float")
                    rawCapture.truncate(0)
                    continue

                # accumulate the weighted average between the current frame and
                # previous frames, then compute the difference between the current
                # frame and running average
                cv2.accumulateWeighted(gray, avg, 0.5)
                frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

                # threshold the delta image, dilate the thresholded image to fill
                # in holes, then find contours on thresholded image
                thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                    cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]

                # loop over the contours
                for c in cnts:
                    # if the contour is too small, ignore it
                    if cv2.contourArea(c) < conf["min_area"]:
                        continue

                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    text = "Motion Detected!"

                # draw the text and timestamp on the frame
                ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
                

                # check to see if the room is occupied
                if text == "Motion Detected!":
                    # check to see if enough time has passed between uploads
                    if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
                        # increment the motion counter
                        motionCounter += 1

                        # check to see if the number of frames with consistent motion is
                        # high enough
                        if motionCounter >= conf["min_motion_frames"]:
                            # update the last uploaded timestamp and reset the motion
                            # counter
                            print("[INFO] Motion detected!")
                            os.system('./pushbullet.sh "Alert Motion Detected"')
                            
                            scipy.misc.imsave('./saved_imgs/outfile'+str(imgCounter)+'.jpg', frame)
                            imgCounter += 1
                            
                            lastUploaded = timestamp
                            motionCounter = 0
                # otherwise, the room is not occupied
                else:
                    motionCounter = 0