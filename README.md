# Style-Transfer Website -- online Image Stylizing
Open source for ***www.styletransfer.cn*** &nbsp;(**unavailable now**)

If you are interested in the details of this project, don't hesitate to contact author by email: styletransfer@163.com.

We appreciate your stars and forks.

## How to run
1. install Python 3.\*: https://www.python.org/downloads/
2. install Django : https://www.djangoproject.com/download/
3. insatll Apache HTTP Server(optinal): https://httpd.apache.org/download.cgi
4. configure running environment for deep learning: 
```
pip install TensorFlow-gpu 1.12.0
pip install Keras 2.2.4
pip install bottle 0.12.16
pip install gevent 1.4.0
pip install h5py 2.9.0
pip install Paste 3.0.8
pip install opencv-python 4.0.0.21
pip install Scikit-image 0.14.2
```
5. download vgg from [here](https://drive.google.com/open?id=1Q5MnOVDGfEcNGVy5AKs2y9jHd92URssG), and put it in ../Style-transfer/fast-style-transfer-master/data/.
5. run website offline:
```
python manage.py runserver
```
6. open a browser, visit http://127.0.0.1:8000/ <br>
**ENJOY IT**
