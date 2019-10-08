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

Paper for this project is [here](https://github.com/QingShuiXiFan/Style-Transfer/blob/master/paper/20190530-%E8%89%BA%E6%9C%AF%E9%A3%8E%E6%A0%BC%E8%BF%81%E7%A7%BB%E7%BD%91%E7%AB%99%E7%9A%84%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0%E2%80%94%E2%80%94%E6%AF%95%E4%B8%9A%E8%AE%BA%E6%96%87.pdf)
