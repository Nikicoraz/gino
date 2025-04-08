FROM python:3.9-alpine AS builder
RUN mkdir /build
WORKDIR /build

RUN apk add --no-cache build-base binutils musl-dev libc-dev linux-headers

RUN python -m ensurepip --upgrade
RUN pip install --prefer-binary --verbose --break-system-packages opencv-python-headless
COPY ./requirements.txt .
RUN pip install --prefer-binary -r requirements.txt --verbose --break-system-packages

RUN pip install pyinstaller --break-system-packages
COPY . .
RUN pyinstaller --noconfirm --onefile --clean --hiddenimport _cffi_backend main.py

FROM alpine AS release
RUN apk add --no-cache ffmpeg
COPY --from=builder /build/dist/main /main
COPY .env /
COPY ./Images /Images
ENTRYPOINT ["/main"]
