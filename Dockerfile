FROM python:buster

COPY . /
RUN pip install -r requirements.txt
CMD [ "python", "app.py" ]