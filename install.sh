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


# Installe Pip requirements
pip install -r requirements.txt
printf "Les paquets Pip sont installés ✅️\n"

# Installe pkg
sudo apt update && sudo apt install -y wkhtmltopdf libopenjp2-7 python3.9 sed curl
printf "Les paquets APT sont installés ✅️\n"


# Obtenir le chemin du répertoire actuel
current_path=$(pwd)


config_file_py="$current_path/app/config/config.py"
config_file_sh="$current_path/app/config/config.sh"

echo -e "HOME_PATH=\"$current_path\"\n\nTELEGRAM_BOT_TOKEN=\"TELEGRAM-TOKEN-HERE\"\n\nOPENAI_API_KEY=\"API-KEY-HERE\"" > "$config_file_py"
echo -e "HOME_PATH=\"$current_path\"\nexport HOME_PATH" > "$config_file_sh"
printf "Les chemins sont définis ✅️\n"

# Utilisez la commande find pour rechercher tous les fichiers .sh
# et appliquer chmod +x à chacun d'eux
find "$current_path" -type f -name "*.sh" -exec chmod +x {} \;
printf "Les droits des fichiers .sh sont appliqués ✅️\n"


# Obtient le contenu du crontab
crontab -l > crontab_temp

# Ajoute les nouvelles lignes
echo "@reboot cd $current_path && python3 -tt print_server.py" >> crontab_temp
echo "@reboot sh $current_path/app/monitor/cat_monitor.sh > $current_path/app/monitor/cat_monitor.txt 2>&1" >> crontab_temp
echo "@reboot cd $current_path/app/telegram_bot && sleep 15 && python3 bot.py > $current_path/app/monitor/start.txt 2>&1" >> crontab_temp
echo "* * * * * truncate -s 2M  $current_path/app/monitor/start.txt" >> crontab_temp
echo "* * * * * truncate -s 2M  $current_path/app/monitor/cat_monitor.txt" >> crontab_temp

# Installe la nouvelle crontab
crontab crontab_temp

rm crontab_temp
printf "Les Cron sont installés ✅️\n"

# Obtient le contenu actuel du crontab de root
#sudo crontab -l > crontab_temp

# Ajoute une nouvelle ligne (ajustez selon vos besoins)
#echo "@reboot cd $current_path && ./start_catprinterbot.sh" | sudo tee -a crontab_temp

# Installe la nouvelle crontab pour root
#sudo crontab crontab_temp

#rm crontab_temp
#printf "Les Cron sudo sont installés ✅️\n"
