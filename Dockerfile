FROM python:3.8-slim-bullseye

COPY . /app/
# 安装依赖
RUN pip3 install -r /app/requirements.txt
# 暴露8000端口
EXPOSE 8000
# 入口
CMD ["python3","/app/manage.py","runserver","0.0.0.0:8000"]