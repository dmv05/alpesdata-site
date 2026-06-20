FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html
RUN chmod -R 644 /usr/share/nginx/html/*.xml /usr/share/nginx/html/*.txt && \
    chmod -R 755 /usr/share/nginx/html
EXPOSE 80
