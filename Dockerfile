FROM python:alpine

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && apk add i2c-tools --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
    && pip install flask Flask-Bootstrap flask-socketio eventlet smbus2 pyyaml \
    && apk del .build-deps gcc libc-dev make

COPY ./app /app
RUN chmod +x /app/*.sh

WORKDIR /app/

EXPOSE 1080

# DEBUG - if true (default) a debugger is started and changes to src are automatically reloaded
#ENV DEBUG=False
# PORT - port for webserver
#ENV PORT=1080
#ENV I2C_PERSISTENCE=true
# I2C_PERSISTENCE - if true (default) the relays are set to the value in the config file on boot
#ENV I2C_PERSISTENCE=true
# SECRET_KEY - secret for socketIO. If not set a random one is generated on each boot
#ENV SECRET_KEY=mysecret
# I2C_CONFIG_FILE - path to the folder with the list of I2C relays. Created on first usage.
ENV I2C_CONFIG_FILE=/config/i2c_config.yaml

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/app/start-server.sh"]
