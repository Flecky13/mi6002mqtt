# mi6002mqtt
Bosswerk Mi600 to MQTT

Englisch:
Update the fie config_sample.ini and copy it to config.ini
Before creating your own DockerImange, configure whether the config ini file should be copied with or not.
I use a Kubernettes cluster and have integrated the config.ini via a Config.map.

In the Docker file there is a crontab entry that reads the MI600 every 5 minutes and sends it to an MQTT Borker


German:
Aktualisieren Sie die config_sample.ini fie und copier Sie diese zu config.ini
Konfigurieren Sie vor dem Erstellen des eigenen DockerImange, ob die config ini datei mit kopiert werden soll oder nicht
Ich nutze ein Kubernettes Cluster und habe die config.ini über ein Config.map eingebunden.

Im Docker file ird ein crontab eintrag ezeug das den MI600 alle 5 Minuten ausliest und an einen MQTT Borker sendet

