# 基于镜像基础
FROM python:3.7

# 添加环境变量
# ENV PATH /usr/local/bin

# 设置工作目录 /proxy_poll
WORKDIR /proxy_poll

# 复制当前代码文件到容器中 /proxy_poll
ADD . /proxy_poll

# 拷贝requirments.txt到工作目录
COPY requirments.txt requirments.txt

# 安装pip
# RUN pip install --upgrade pip

# 安装所需的包
# RUN pip install -r requirements.txt

# Run app.py when the container launches
# CMD ["python", "run.py"]
