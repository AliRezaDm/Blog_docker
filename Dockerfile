FROM python:3.10-alpine
# specifying the scritps directory for excutable scripts 
ENV PATH = "/scripts:${PATH}"
# Copying requirements into the container
COPY Requirements/ Requirements/
# Add necessary packages for uWSGI
# no-cache -> store no cache in order to keep it as lighweight as possible 
# --virtual .tmp -> for deleting the dependecies after we're done with them 
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
# installing production requirements
RUN pip install -r Requirements/production.txt
# rmoving depenedecies because their not needed
RUN apk del .tmp
# setting up work directory and copying everything to the container
RUN mkdir /app
COPY ./ /app
WORKDIR /app
# Adding scritps and giving executable permission 
COPY ./scripts /scripts
RUN chmod +x /scripts/*
# creating directory for media and static files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static 
# Creatitng another user with less priviliges
RUN adduser -D emtedad
RUN chown -R emtedad:emtedad /vol
RUN chmod -R 755 /vol/web
#Switch from root to the user 
USER emtedad

CMD ["entrypoint.sh"]

