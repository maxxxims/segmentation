### Segmentation
### Run application for image annotation (2 variants):
#
Variant 1 using docker
```
    git clone https://github.com/maxxxims/segmentation.git
    cd segmentation
    docker-compose up --build
```
Variant 2 using python (py/python3). The required version of Python>=3.10
```
    git clone https://github.com/maxxxims/segmentation.git
    cd segmentation
    pip freeze -r "requirements.txt"
    python -m GUI.server
```

### Close docker & use venv
```
    docker-compose down  # close app if you use docker

    python -m venv venv       # if you run the app with python 
    source venv/bin/activate  # and there are some problems with the versions
```
#

### Open application for image annotation

The application will be available at the default url 
`http://127.0.0.1:8050/ `<br> Detailed information about the functionality is available in the  <a href="http://127.0.0.1:8050/tutorial">tutorial </a> (http://127.0.0.1:8050/tutorial)