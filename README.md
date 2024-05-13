# Portail-Captif
 
 Ceci est une application conçu pour un portail captif
 
 Les fonctionnalités disponibles sur cette application sont:
- Requête de numéro de téléphone et envoi un voucher code par sms
- Vérification d'un utilisateur s'il fait partie de l'organisation
- Ajout de numéro de téléphone pour un utilisateur
- Modification de mot de passe

# Installation dans Ubuntu/Debian
## Installer Gammu depuis la code source
1. Télécharger gammu depuis le site officiel https://wammu.eu/download/gammu/
```
wget https://dl.cihar.com/gammu/releases/gammu-1.42.0.tar.gz
```
 
2. Décompresser l'archive
```
tar xvf gammu-1.42.0.tar.gz
```

3. Configurer et installer 
```
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential cmake
cd gammu-1.42.0
./configure; make
sudo make install
sudo ldconfig
```

4. Vérifier si le package est bien installé
```
gammu version
```

## Configurer Gammu
1. Brancher le modem

2. Vérifier s'il est bien installé
```
lsusb
```
![lsusb capture](images/lsusb.png)

3. Créer un fichier *.gammurc* dans le repértoire _Home_
```
cat << EOF > ~/.gammurc
[gammu]

port = /dev/ttyUSB1
model = 
connection = at
synchronizetime = yes
logfile = 
logformat = nothing
use_locking = 
gammuloc =
EOF
```


4. Pour executer le commande <gammu> sans avoir le privilège root à chaque fois, ajouter l'utilisateur dans le group <dialout>
```
sudo usermod -aG dialout $user
```

5. Redémarrer le serveur.

6. Tester la commande du N*4 sans sudo
```
gammu identify
```

7. Ajouter <GAMMU_PATH> dans l'environnement, _~/.bashrc_ ou bien _~/.zshrc_
```
nano ~/.bashrc
```
```
export GAMMU_PATH="/usr/local"
```
Enregistrer et quitter `ctrl+x` `y`

8. Rafraîchir le dernier changement dans le fichier de l'environnement
```
source ~/.bashrc
```

9. Installer <pkg-config>
```
sudo apt install pkg-config
```

## Installation de l'application
1. Installer <pip>
```
sudo apt install python-pip git
```
2. Installer les packages requises
```
cd ~
git clone https://github.com/tersteven83/portail-captif.git
cd portail-captif
pip install -r requirements.txt
```
