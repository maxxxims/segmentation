# Segmentation
This repository contains an image annotation tools for segmentation and a segmentation framework based on classical machine learning methods.

An example of annotation web-application can be found at the link: http://193.233.20.41:8050/v2/



<u> Login details</u>:<br>
<b>login</b> - tester, <b>password</b> - 321
### Run application for image annotation locally (2 variants):
#
   1) Variant 1 using docker
```
    git clone https://github.com/maxxxims/segmentation.git
    cd segmentation
    docker-compose up --build
```
2) Variant 2 using python3 (py/python). The required version of Python>=3.10
```
    git clone https://github.com/maxxxims/segmentation.git
    cd segmentation
    pip3 install -r "requirements.txt"
    python3 -m GUI.server
```
#
### Open the app

The application will be available at the default url 
`http://127.0.0.1:8050/v2/ `<br> Detailed information about the functionality can be found on the  <a href="http://162.248.227.166:8060/tutorial2">tutorial </a> page (http://162.248.227.166:8060/tutorial2)

##

#### Additional help: close docker & use venv
```
    docker-compose down  # close app if you use docker

    python -m venv venv       # if you run the app with python 
    source venv/bin/activate  # and there are some problems with the versions
```
#
#

![example](https://github.com/maxxxims/segmentation/blob/main/GUI/static/step2.png)
