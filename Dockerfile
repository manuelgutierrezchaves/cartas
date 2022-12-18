FROM python:3.12.0a3-bullseye

COPY /src/ /src/

CMD [ "python", "/src/main.py" ]