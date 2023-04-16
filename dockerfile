FROM python:3.9.1

WORKDIR /usr/app/src
COPY ./ ./
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python", "main.py"]