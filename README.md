[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

# Projet 11 : Améliorez une application Web Python par des tests et du débogage

***voir https://openclassrooms.com/fr/paths/518/projects/839/assignment***


 ## Logiciels
 
 ```
Windows 11
Python 3.10.1
Edge Wedriver 103.0.1264.77 x64
Flask 2.1.3
Selenium 4.3.0
pytest - voir requirements.txt
```

## Initialisation du projet sous windows

### Windows 
```
git clone https://github.com/jsoques1/Python_Testing.git

cd Python_Testing
python -m venv env 
env\Scripts\activate

pip install -r requirements.txt
```

### Selenium edge
```
Télécharger le webdriver [https://developer.microsoft.com/fr-fr/microsoft-edge/tools/webdriver/]
Le recopier dans un répertoire du PATH ou mettre à jour celui-ci avec le répertoire où le webdriver se trouve
```

### Utilisation

- Lancer le serveur Flask avec Powershell :

```
$env:FLASK_APP = "server.py"
flask run
```

***N'oubliez pas de relancer le serveur flask pour réinitialiser les données.***


- Lancer le client Web avec l'URL : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)



## Tests



### Tests fonctionnels/ intégration / unitaires  


- Pour effectuer l'ensemble des tests unitaires et d'intégration, entrer la commande :

```
pytest
```

- Pour otbenir la couverture des tests dans le répertoire htmlcov, entrer la commande :

```
pytest --cov=. --cov-report html
```

### Test de performances

- Lancer le serveur locust

```
locust -f tests\performance_tests\locustfile.py
```

- Puis lancer le client locust via un brower à l'url [http://localhost:8089](http://localhost:8089) et entrer les pamramètres conseillés:

```
Number of users: 6
Spawn ratio: 1
Host: http://127.0.0.1:5000/
```


### Rapports

Les captures d'écran des derniers rapports de tests sont disponibles dans le dossier 'reports'.

- [pytest] pytest_report.png

- [Couverture] coverage_report.png 

- [Performance] locust_report.png & locust_report_2.png 

Optionnel

- [flake8] flake8.png
