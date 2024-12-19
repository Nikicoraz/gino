FROM python:3.10-slim

WORKDIR /home/nicola/gino

RUN apt update && apt install ffmpeg -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./main.py"]
