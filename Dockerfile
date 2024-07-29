FROM python:slim

WORKDIR /home/nicola/gino

RUN apt update && apt install ffmpeg -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./main.py"]
