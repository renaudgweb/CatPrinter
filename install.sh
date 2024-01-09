#!/bin/bash
#
## Install script
## Run this with sudo 
#
# Quitte le programme si une commande échoue
set -o errexit
# Quitte le programme si variable non definie
set -o nounset
# Quitte le programme si une commande échoue dans un pipe
set -o pipefail

clear
cat << "EOF"

Installation script for the catprinter



                         /\_/\ 
                        ( o.o )
                         > ^ <




/!\⚠️Be sure to REBOOT after the execution of this script⚠️/!\

EOF

# Obtenir le chemin du répertoire actuel
current_path=$(pwd)

default_install() {
    printf "Default Install...\n"
    # Installe Pip requirements
    pip install -r requirements.txt
    printf "Pip packages are installed successfully ✔️\n"

    # Installe pkg
    sudo apt update && sudo apt install -y wkhtmltopdf libopenjp2-7 python3 sed curl weather-util
    printf "APT packages are installed successfully ✔️\n"


    config_file_ini="$current_path/app/config/config.ini"
    config_file_sh="$current_path/app/config/config.sh"

    home_path="[Paths]\nHOME_PATH = $current_path"
    telegram_bot_token="[Telegram_api]\nTELEGRAM_BOT_TOKEN = TOKEN-HERE"
    openai_api_key="[OpenAI_api]\nOPENAI_API_KEY = APIKEY-HERE"
    nextcloud_talk_channel_id="[Nextcloud_Talk_api]\nNEXTCLOUD_TALK_CHANNEL_ID = CHANNEL-ID-HERE"
    openweather_api_key="[Openweather_api]\nOPENWEATHER_API_KEY = APIKEY-HERE"

    echo -e "# Config file\n\n" > "$config_file_ini"
    echo -e "$home_path\n\n$telegram_bot_token\n\n$openai_api_key\n\n$nextcloud_talk_channel_id\n\n$openweather_api_key" > "$config_file_ini"
    echo -e "HOME_PATH=\"$current_path\"\nexport HOME_PATH" > "$config_file_sh"
    printf "Paths are defined successfully ✔️\n"

    # Utilisez la commande find pour rechercher tous les fichiers .sh
    # et appliquer chmod +x à chacun d'eux
    find "$current_path" -type f -name "*.sh" -exec chmod +x {} \;
    printf "Permissions for .sh files have been applied successfully ✔️\n"


    # Obtenir l'utilisateur courrant
    current_user=$(echo $current_path | cut -d/ -f3)

    # Obtient le contenu du crontab de l'utilisateur courant s'il existe, sinon crée un fichier vide
    sudo -u $current_user crontab -l > crontab_temp 2>/dev/null || touch crontab_temp

    # Ajoute les nouvelles lignes
    {
      echo "@reboot cd $current_path && python3 -tt print_server.py"
      echo "@reboot sh $current_path/app/monitor/cat_monitor.sh > $current_path/app/monitor/cat_monitor.txt 2>&1"
      echo "@reboot cd $current_path/app/telegram_bot && sleep 15 && python3 bot.py > $current_path/app/monitor/start.txt 2>&1"
      echo "* * * * * truncate -s 2M  $current_path/app/monitor/start.txt"
      echo "* * * * * truncate -s 2M  $current_path/app/monitor/cat_monitor.txt"
    } >> crontab_temp

    # Installe la nouvelle crontab pour l'utilisateur actuel
    if sudo -u $current_user crontab crontab_temp; then
      rm crontab_temp
      printf "Cron is installed successfully ✔️\n"
    else
      echo "Error during cron installation ❌\n"
      rm crontab_temp
      exit 1
    fi
}

start_install() {
    printf "Start Install...\n"

    sudo crontab -l > crontab_temp 2>/dev/null || touch crontab_temp

    echo "@reboot cd $current_path && ./start_catprinterbot.sh" | sudo tee -a crontab_temp

    # Install the new crontab for root user
    if sudo crontab crontab_temp; then
        rm crontab_temp
        printf "Cron with sudo is installed successfully ✔️\n"
    else
        echo "Error during cron installation ❌\n"
        rm crontab_temp
        exit 1
    fi
}

web_install() {
    printf "Web Install...\n"

    sudo apt update && sudo apt install php apache2
    printf "Apache2 and PHP installed successfully ✔️\n"

    php_web_log="<?php

\$log = file_get_contents('$current_path/app/monitor/start.txt');
\$lines = explode(\"\\n\", \$log);

echo '<!DOCTYPE html>
    <html>
    <head>
        <meta charset=\"utf-8\">
        <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">
        <meta name=\"viewport\" content=\"height=device-height, width=device-width, initial-scale=1.0, shrink-to-fit=no, user-scalable=no\">
        <link rel=\"icon\" type=\"image/png\" href=\"#\">
        <script src=\"https://cdn.tailwindcss.com\"></script>
        <title>Cat Printer Logs</title>
    </head>
    <body style=\"background-color:lightgrey;\">
        <h1 class=\"text-center text-3xl font-bold underline font-mono\">Cat Printer Logs</h1>
        <div style=\"margin:2%;\">
            <pre style=\"white-space:pre-wrap;\">
                <code class=\"font-mono\" style=\"font-size:12px;background:greenyellow;word-wrap:break-word;\">';

foreach (\$lines as \$line) {
    echo \$line.'<br>';
}

echo '          </code>
            </pre>
        </div>
    </body>
</html>';

?>"

    # Écriture du contenu dans un fichier PHP
    mkdir /var/www/html/cat/
    echo "$php_web_log" > "/var/www/html/cat/index.php"
    printf "PHP file generated successfully ✔️\n"
    ip_priv=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}')
    printf "\nYour logs can be readable at : $ip_priv/cat/ \n\n"

}

while true
do
    printf "Choose your install : [D]efault, [S]tart, [W]eb or [Q]uit : "
    read -r REPLY
    case $REPLY in
        [Dd]* ) default_install; break;;
        [Ss]* ) start_install; break;;
        [Ww]* ) web_install; break;;
        [Qq]* ) printf "Bye 💨\n"; exit;;
        * ) printf "⛔️Enter one of these letters: D, S, W or Q\n";;
    esac
done
