FROM python:3.9-alpine AS builder
RUN mkdir /build
WORKDIR /build

RUN apk add --no-cache build-base binutils musl-dev libc-dev linux-headers

RUN python -m ensurepip --upgrade
COPY ./requirements.txt .
RUN pip install --prefer-binary -r requirements.txt --break-system-packages --verbose

RUN pip install pyinstaller --break-system-packages
COPY . .
RUN pyinstaller --noconfirm --onefile --clean --hiddenimport _cffi_backend main.py

FROM alpine AS release
COPY --from=builder /build/dist/main /main
COPY .env /
RUN apk add --no-cache ffmpeg
ENTRYPOINT ["/main"]
