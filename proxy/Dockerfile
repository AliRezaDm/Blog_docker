# Getting a image of nginx that allows unprivilged user to run commands
FROM nginxinc/nginx-unprivileged:1-alpine

#Copying the configuration filea
COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

# switch to root to make directory for static files and give owner full priviliges
USER root 
RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

USER nginx