# portail-captif
 
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
```

4. Vérifier si le package est bien installé
```
gammu version
```

II - Configurer Gammu
