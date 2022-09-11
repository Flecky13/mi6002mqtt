FROM python:alpine

LABEL authors="Pedro Tepe <support@hometepe.de>"
LABEL version="0.3"
LABEL description="Bosswerk Mi600 to MQTT \
Bosswerk to Mqtt Mi300/Mi600 solar micro inverter \
Quelle https://github.com/Skarabaen/BosswerkMI600 \
\
Aktuell noch als Test Version\
kein Support, verwendung unter eigene verantwortung."
LABEL org.opencontainers.image.source https://github.com/Flecky13/mi6002mqtt

RUN mkdir /opt/mi600/
WORKDIR /opt/mi600/

RUN pip3 install requests
RUN pip install paho-mqtt

COPY mi600.py /opt/mi600/
#COPY config.ini /opt/mi600/

RUN touch crontab.tmp \
    && echo '*/5 * * * * /usr/local/bin/python /opt/mi600/mi600.py > /opt/mi600/crontab.log 2>&1' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

CMD ["/usr/sbin/crond", "-f", "-d", "0"]