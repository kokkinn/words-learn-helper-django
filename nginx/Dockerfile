FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
# delete default conf file

COPY nginx.conf /etc/nginx/conf.d
# copy new conf file to container