#!/bin/bash
#
## Install script
## Run this with sudo !
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
    echo "Default Install..."

    sudo apt update && sudo apt install -y wkhtmltopdf libopenjp2-7 python3 alsa-utils sed curl weather-util
    echo "APT packages are installed successfully ✔️\n"

    pip install -r requirements.txt
    echo "Pip packages are installed successfully ✔️\n"

    config_file_ini="$current_path/app/config/config.ini"
    config_file_php="$current_path/app/config/config.php"
    config_file_sh="$current_path/app/config/config.sh"

    # Demander les informations à l'utilisateur
    read -p "Telegram Bot TOKEN: " telegram_bot_token
    read -p "OpenAI API KEY: " openai_api_key
    read -p "Nextcloud SERVER URL: " nextcloud_url
    read -p "Nextcloud BOT NAME: " nextcloud_bot_name
    read -p "Nextcloud PASSWORD: " nextcloud_password
    read -p "Nextcloud Talk ID Channel: " nextcloud_talk_channel_id
    read -p "OpenWeather API KEY: " openweather_api_key
    read -p "Indeed job title: " indeed_job_name
    read -p "Indeed city name: " indeed_city_name

    # Contenu du fichier de configuration INI
    home_path="[Paths]\nHOME_PATH = $current_path"
    telegram_bot_token="[Telegram_api]\nTELEGRAM_BOT_TOKEN = $telegram_bot_token"
    openai_api_key="[OpenAI_api]\nOPENAI_API_KEY = $openai_api_key"
    nextcloud_talk_channel_id="[Nextcloud_Talk_api]\nNEXTCLOUD_TALK_CHANNEL_ID = $nextcloud_talk_channel_id"
    openweather_api_key="[Openweather_api]\nOPENWEATHER_API_KEY = $openweather_api_key"
    indeed_job_name="[Indeed_job_name]\nINDEED_JOB_NAME = $indeed_job_name"
    indeed_city_name="[Indeed_city_name]\nINDEED_CITY_NAME = $indeed_city_name"

    echo -e "# Config file\n\n$home_path" \
    "\n\n$telegram_bot_token\n\n$openai_api_key" \
    "\n\n$nextcloud_talk_channel_id\n\n$openweather_api_key" \
    "\n\n$indeed_job_name\n$indeed_city_name" > "$config_file_ini"

        # Contenu du fichier de configuration PHP
        php_config="<?php

\$SERVER = \"$nextcloud_url\";
\$USER = \"$nextcloud_bot_name\";
\$PASS = \"$nextcloud_password\";

?>"
    echo -e "$php_config" > "$config_file_php"

    echo -e "HOME_PATH=\"$current_path\"\nexport HOME_PATH" > "$config_file_sh"
    echo "Paths are defined successfully ✔️\n"

    # Utilisez la commande find pour rechercher tous les fichiers .sh
    # et appliquer chmod +x à chacun d'eux
    find "$current_path" -type f -name "*.sh" -exec chmod +x {} \;
    echo "Permissions for .sh files have been applied successfully ✔️\n"

    # Obtenir l'utilisateur courrant
    current_user=$(echo $current_path | cut -d/ -f3)

    # Obtient le contenu du crontab de l'utilisateur courant s'il existe, sinon crée un fichier vide
    sudo -u $current_user crontab -l > crontab_temp 2>/dev/null || touch crontab_temp

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
      echo "Cron is installed successfully ✔️\n"
    else
      echo "Error during cron installation ❌"
      rm crontab_temp
      exit 1
    fi

    while true
    do
        echo "Default install is done ✔️\nNow, make your choice: [R]eboot🔄, [S]tart▶️, [W]eb🌐 or [Q]uit🚪 : "
        read -r REPLY
        case $REPLY in
            [Rr]* ) sudo reboot; break;;
            [Ss]* ) start_install; break;;
            [Ww]* ) web_install; break;;
            [Qq]* ) echo "Bye 👋"; exit;;
            * ) echo "⛔️Enter one of these letters: R, S, W or Q";;
        esac
    done
}

start_install() {
    echo "Start Install..."

    sudo crontab -l > crontab_temp 2>/dev/null || touch crontab_temp

    echo "@reboot cd $current_path && ./start_catprinterbot.sh" | sudo tee -a crontab_temp

    if sudo crontab crontab_temp; then
        rm crontab_temp
        echo "Cron with sudo is installed successfully ✔️\n"
    else
        echo "Error during cron installation ❌"
        rm crontab_temp
        exit 1
    fi

    while true
    do
        echo "Start install is done ✔️\nNow, make your choice: [R]eboot🔄, [D]efault⚙️, [W]eb🌐 or [Q]uit🚪 : "
        read -r REPLY
        case $REPLY in
            [Rr]* ) sudo reboot; break;;
            [Dd]* ) default_install; break;;
            [Ww]* ) web_install; break;;
            [Qq]* ) echo "Bye 👋"; exit;;
            * ) echo "⛔️Enter one of these letters: R, D, W or Q";;
        esac
    done
}

web_install() {
    echo "Web Install..."

    sudo apt update && sudo apt install php apache2
    echo "Apache2 and PHP installed successfully ✔️\n"

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

    mkdir /var/www/html/catlog/
    echo "$php_web_log" > "/var/www/html/catlog/index.php"
    echo "PHP file generated successfully ✔️\n"
    ip_priv=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}')
    printf "\nYour logs can be readable at : $ip_priv/catlog/ \n\n"

    while true
    do
        echo "Web install is done ✔️\nNow, make your choice: [R]eboot🔄, [D]efault⚙️, [S]tart▶️ or [Q]uit🚪 : "
        read -r REPLY
        case $REPLY in
            [Rr]* ) sudo reboot; break;;
            [Dd]* ) default_install; break;;
            [Ss]* ) start_install; break;;
            [Qq]* ) echo "Bye 👋"; exit;;
            * ) echo "⛔️Enter one of these letters: R, D, S or Q";;
        esac
    done
}

while true
do
    echo "Choose your install : [D]efault⚙️, [S]tart▶️, [W]eb🌐 or [Q]uit🚪 : "
    read -r REPLY
    case $REPLY in
        [Dd]* ) default_install; break;;
        [Ss]* ) start_install; break;;
        [Ww]* ) web_install; break;;
        [Qq]* ) echo "Bye 👋"; exit;;
        * ) echo "⛔️Enter one of these letters: D, S, W or Q";;
    esac
done
