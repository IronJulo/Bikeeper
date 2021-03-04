FROM python:3.6
RUN mkdir /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8080
RUN pip install -r requirements.txt
CMD flask loaddb && flask run --host=0.0.0.0 