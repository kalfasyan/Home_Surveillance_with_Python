# Motion Detection Alerts with Streaming  
Motion detection using OpenCV (Raspberry Pi compatible), alerting through pushbullet, served with flask.

## Installation
```pip install -r requirements.txt```

## Usage
```CAMERA=opencv python3 app.py -c conf.json```  
  
Then open this [address (http://0.0.0.0:5000/)](http://0.0.0.0:5000/) on your browser.  
  
If you run it on raspberry pi (+ enabled camera module, installed picamera package), uncomment line 13 from app.py:  
```#from camera_pi import Camera```

### Thanks to:
[miguelgrinberg](https://github.com/miguelgrinberg/flask-video-streaming) - for the flask streaming part  
[Adrian Rosebrock](https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/) - for the motion detection part  
[pushbullet](https://docs.pushbullet.com) - for the alerts part  
