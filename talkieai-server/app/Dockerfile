FROM python:3.11
WORKDIR /app
COPY . .

RUN rm -f /etc/apt/sources.list /etc/apt/sources.list.d/* \
 && printf '%s\n' \
      'deb https://mirrors.ustc.edu.cn/debian bookworm main contrib non-free' \
      'deb https://mirrors.ustc.edu.cn/debian-security bookworm-security main contrib non-free' \
      'deb https://mirrors.ustc.edu.cn/debian bookworm-updates main contrib non-free' \
    > /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends libasound2 curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8097
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8097"]
