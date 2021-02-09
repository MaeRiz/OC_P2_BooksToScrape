# Programme de scraping en Python

Pour utiliser cette application suivez la procédure ci-dessous.

Cette procédure a été conçue pour l'OS Windows 10. Certaines commandes peuvent varier selon votre OS.

## Utilisation

1. Installer [Python 3](https://www.python.org/downloads/).

2. Télécharger le programme via GitHub avec la commande ci-dessous ou en téléchargeant [l'archive](https://github.com/MaeRiz/P1_OC/archive/master.zip).
```bash
git clone https://github.com/MaeRiz/OC_P2_BooksToScrape.git
```

3. Se rendre dans le répertoire du projet dans un terminal:
```cmd
cd "répertoire/du/projet"
```

4. Créer l'environnement virtuel:
```cmd
python3 -m venv env
```

5. Activer l'environnement virtuel:
```cmd
env\Scripts\activate
```

6. installer les modules via la commande:
```cmd
pip install -r requirements.txt
```

7. Lancer le programme:
```cmd
python app.py
```

## Informations

- Chaque catégorie correspond à un fichier .CSV et se trouve dans le répertoire ../app/books/

- Chaque ligne dans le fichier .CSV correspond à un livre (sauf l'entête).

- Toutes les images sont enregistrées dans le répertoire: ../app/imgs/

- Le séparateur utilisé dans le fichier .CSV est le point-virgule (;).

- Les répertoires (../books/ et ../imgs/) et les fichiers .CSV sont créés automatiquement au lancement du programme.

- Les images sont nommées par le numéro de produit unique de chaque livre.