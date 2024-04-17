FROM nginx:1.25.4-alpine3.18-slim

ENV HOME=/web
RUN mkdir $HOME
RUN mkdir $HOME/static
RUN mkdir $HOME/media

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d