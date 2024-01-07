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

default_install() {
    printf "default install...\n"
    # Installe Pip requirements
    pip install -r requirements.txt
    printf "Pip packages are installed successfully ✔️\n"

    # Installe pkg
    sudo apt update && sudo apt install -y wkhtmltopdf libopenjp2-7 python3 sed curl
    printf "APT packages are installed successfully ✔️\n"


    # Obtenir le chemin du répertoire actuel
    current_path=$(pwd)


    config_file_py="$current_path/app/config/config.py"
    config_file_sh="$current_path/app/config/config.sh"

    echo -e "HOME_PATH=\"$current_path\"\n\nTELEGRAM_BOT_TOKEN=\"TELEGRAM-TOKEN-HERE\"\n\nOPENAI_API_KEY=\"API-KEY-HERE\"" > "$config_file_py"
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

all_install() {
    default_install;

    printf "and start install\n"

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

while true
do
    printf "Choice: [D]efault install, with [S]tart install or [Q]uit : "
    read -r REPLY
    case $REPLY in
        [Dd]* ) default_install; break;;
        [Ss]* ) all_install; break;;
        [Qq]* ) printf "Bye 💨\n"; exit;;
        * ) printf "⛔️Enter one of these letters: D, S or Q\n";;
    esac
done
