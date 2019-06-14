# Motion Detection, Alerts, Streaming  
With this repo you can:  
1. Watch your webcam/camera/picamera feed on localhost [(0.0.0.0:5000)](https://0.0.0.0:5000) which is served with flask.  
2. Perform motion detection on the camera feed, using opencv.  
3. Send alerts / push notifications (via pushbullet) to your phone, desktop or anywhere you have installed pushbullet, with its API.  
4. Save the images that triggered the alerts on your disk (marking the exact image region of movement).  
  

## Requirements  
I strongly advise you to install a separate virtual environment to avoid dependency hells of python packages.  
Check out "Step 8" from [this nice blog post](https://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/).  

Get an Access token from [Pushbullet](https://www.pushbullet.com/#settings/account)  

Make sure you have 'curl' installed:  
```sudo apt install curl```  
  
Python 3  

## Installation  
run the install.sh script:  
```./install.sh```  

## Usage  
```CAMERA=opencv python3 app.py -c conf.json```  
  
Then open this [address (http://0.0.0.0:5000/)](http://0.0.0.0:5000/) on your browser.  
  
If you run it on raspberry pi (+ enabled camera module, installed picamera package), uncomment line 13 from app.py:  
```#from camera_pi import Camera```  
and then run:  
```python3 app.py -c conf.json```  

### Thanks to:
[miguelgrinberg](https://github.com/miguelgrinberg/flask-video-streaming) - for the flask streaming part  
[Adrian Rosebrock](https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/) - for the motion detection part  
[pushbullet](https://docs.pushbullet.com) - for the alerts part  

#### Troubleshooting
You might have to install these libraries if you get errors complaining about them:
```
sudo apt install libhdf5-dev
sudo apt install libhdf5-serial-dev 
sudo apt install libqt4-test 
sudo apt install libqtgui4
```
