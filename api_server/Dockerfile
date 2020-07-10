FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN echo "[mongo]" > /usr/src/app/openapi_server/properties.ini
RUN echo "endpotin = mongodb://$MONGO_HOST:27017/" >> /usr/src/app/openapi_server/properties.ini

EXPOSE 8082

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]