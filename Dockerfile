FROM python:3.11
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY app .
RUN pip install -r requirements.txt
EXPOSE 8081
CMD [ "python", "-u", "./app.py"]
