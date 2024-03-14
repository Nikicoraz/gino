FROM python:3.9

WORKDIR /home/nicola/gino

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install ffmpeg -y

COPY . .
CMD ["python", "./main.py"]
