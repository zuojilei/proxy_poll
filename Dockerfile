# 基于镜像基础
FROM python:3.7

# 设置代码文件夹工作目录 /proxy_poll
WORKDIR /proxy_poll

# 复制当前代码文件到容器中 /proxy_poll
ADD . /proxy_poll

# 安装所需的包
RUN pip install --upgrade pip \
    && pip install -r ./requirements.txt

# Run app.py when the container launches
CMD ["python", "run.py"]