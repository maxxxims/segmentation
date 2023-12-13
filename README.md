### Segmentation
### Run application for image annotation (2 variants):
#
   1) Variant 1 using docker
```
    git clone https://github.com/maxxxims/segmentation.git
    cd segmentation
    docker-compose up --build
```
2) Variant 2 using python (py/python3). The required version of Python>=3.10
```
    git clone https://github.com/maxxxims/segmentation.git
    cd segmentation
    pip freeze -r "requirements.txt"
    python -m GUI.server
```
#
### Open the app

The application will be available at the default url 
`http://127.0.0.1:8050/ `<br> Detailed information about the functionality can be found in the  <a href="http://127.0.0.1:8050/tutorial">tutorial </a> (http://127.0.0.1:8050/tutorial)

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
