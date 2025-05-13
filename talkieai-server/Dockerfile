# 使用官方 Python 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 到容器中
#COPY ./requirements.txt .

# 复制整个项目代码到容器中
COPY . .

# 安装系统依赖
#RUN apt-get update && apt-get install -y ffmpeg libasound2
RUN apt-get update && apt-get install -y libasound2

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt


# 暴露应用监听的端口
EXPOSE 8097

# 启动命令，对应你的 uvicorn 命令
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8097"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8097"]
#CMD ["sh", "-c", "cd /app && uvicorn app.main:app --host 0.0.0.0 --port 8097"]
