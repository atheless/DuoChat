FROM nginxproxy/nginx-proxy

COPY vhost.d/* /etc/nginx/vhost.d/
COPY custom.conf /etc/nginx/conf.d/custom.conf

COPY vhost.d/* /app/vhostrewrite/
COPY www_redirect.conf /app/www_redirect.conf
