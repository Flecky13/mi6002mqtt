# mi6002mqtt
Bosswerk Mi600 or Deye Sun600 to MQTT

Englisch:
Update the file config_sample.ini and copy it to config.ini
Before creating your own DockerImange, configure the config ini file if it should be copied with or not.
I use a Kubernettes cluster and have integrated the config.ini via a Config.map.

In the Docker file there is a crontab entry that reads the MI600 every 5 minutes and sends it to an MQTT Broker


German:
Aktualisiert die config_sample.ini fie und copiert Sie zu config.ini
Konfiguriert vor dem Erstellen des eigenen DockerImange, ob die config.ini datei mit kopiert werden soll oder nicht
Ich nutze ein Kubernettes Cluster und habe die config.ini über ein Config.map eingebunden.

Im Docker file wird ein crontab eintrag erzeugt das den MI600 alle 5 Minuten ausliest und an einen MQTT Broker sendet

I have reused some script parts from https://github.com/fr00sch/bosswerk_mi600_solar and extrat the config to config.ini

Docker image without config.ini, "docker push p72t19/mi6002mqtt:v0.5"
https://hub.docker.com/repository/docker/p72t19/mi6002mqtt


