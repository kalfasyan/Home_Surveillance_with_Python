# Motion Detection Alerts, plus Streaming  
With this repo you can:  
1. Watch your webcam/camera/picamera feed on localhost [(0.0.0.0:5000)](https://0.0.0.0:5000) which is served with flask.  
2. Perform motion detection on the camera feed, using opencv.  
3. Send alerts (via pushbullet) to your phone, desktop or anywhere you have installed pushbullet, with its API.  
4. Save the images that triggered the alerts on your disk (marking the exact image region of movement).  
  

## Installation
```pip install -r requirements.txt```

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
