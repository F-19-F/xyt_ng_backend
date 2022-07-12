### 学年设计-校园通NG后端 19信管1 唐霆峰组
基于restframework的校园通后端,学年设计时间紧迫,可能有不完善的地方。
出于开发演示的目的，我使用了sqlite3数据库作为后端的数据库。在Django的ORM下，数据库后端只是一个数据存储介质了，切换后端数据库只需要简单修改设置即可。

### 1.项目依赖
* python 3.8.9
* django 4.0.5
* djangorestframework 3.13
* simple-ui
* django-cors-headers
* django-filter

### 2.运行方式
#### 2.1 使用docker
运行下面两行命令后访问[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)可进入管理界面
```
docker build -t "xytbackend" .
docker run -dp 8000:8000  xytbackend
```
#### 2.2 使用venv
```
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```



