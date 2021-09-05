FROM noraneco/ubuntu-apache:latest
COPY ./public_html/ /var/www/html/
WORKDIR /var/www/html/
CMD python3 serve.py && apachectl -D FOREGROUND