# IT Parc

Module Odoo 18 Enterprise pour la gestion centralisee du parc informatique de TECHPARK CI.

Le depot contient uniquement le module custom `it_parc`. Il ne contient pas le code source Odoo complet.

## Environnement requis

- Odoo 18 Enterprise
- Python 3.11
- PostgreSQL
- Modules Odoo requis :
  - `base`
  - `hr`
  - `stock`
  - `purchase`
  - `account`
  - `maintenance`
  - `mail`
  - `contacts`
  - `web`
- Bibliotheque Python requise pour les exports Excel :
  - `xlsxwriter`

## Installation du module

Cloner le depot, puis placer le dossier `it_parc` dans un chemin d'addons Odoo.

Exemple :

```text
D:\Odoo_final\odoo-18.0+e.20241230\odoo\addons\it_parc
```

Verifier que le chemin parent est bien declare dans `odoo.conf` :

```ini
addons_path = D:\Odoo_final\odoo-18.0+e.20241230\odoo\addons
```

Installer le module :

```powershell
cd D:\Odoo_final\odoo-18.0+e.20241230
venv\Scripts\python.exe -m odoo -c odoo.conf -d test_shop -i it_parc --stop-after-init
```

Mettre a jour le module apres modification :

```powershell
cd D:\Odoo_final\odoo-18.0+e.20241230
venv\Scripts\python.exe -m odoo -c odoo.conf -d test_shop -u it_parc --stop-after-init
```

Lancer Odoo :

```powershell
cd D:\Odoo_final\odoo-18.0+e.20241230
venv\Scripts\python.exe -m odoo -c odoo.conf
```

URL locale :

```text
http://127.0.0.1:8072
```

## Generation des PDF

Les rapports PDF du module utilisent le moteur QWeb natif d'Odoo. Pour que la generation PDF fonctionne, Odoo doit aussi trouver `wkhtmltopdf`.

Sur Windows, installer :

```text
wkhtmltopdf 0.12.6-1 avec Qt patche
```

Chemin attendu apres installation :

```text
C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
```

Ajouter ensuite le chemin dans `odoo.conf` :

```ini
bin_path = C:\Program Files\wkhtmltopdf\bin
```

Puis redemarrer completement Odoo.

Pour verifier depuis PowerShell :

```powershell
& "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
```

La sortie attendue doit ressembler a :

```text
wkhtmltopdf 0.12.6 (with patched qt)
```

Si Odoo affiche encore :

```text
Unable to find Wkhtmltopdf on this system
```

verifier que `bin_path` est bien dans le fichier `odoo.conf` utilise au demarrage, puis redemarrer le serveur Odoo.

## Fonctionnalites principales

- Inventaire des equipements informatiques
- Affectation des equipements aux employes et departements
- Historique des affectations
- Suivi des interventions de maintenance
- Gestion des contrats fournisseurs
- Alertes de garantie et d'echeance de contrat
- Assistants metier :
  - reaffectation
  - renouvellement de contrat
  - scan des alertes
  - import CSV
  - export Excel
- Rapports PDF QWeb
- Dashboard OWL

## Rapports disponibles

- Fiche PDF d'un equipement
- Inventaire du parc informatique
- Historique PDF des maintenances

Les boutons visibles dans les fiches :

- `Fiche PDF` dans une fiche equipement
- `Historique PDF` dans une fiche intervention

## Exports Excel

Les exports `.xlsx` utilisent `xlsxwriter`.

Exports disponibles :

- inventaire complet
- synthese des couts de maintenance
- contrats arrivant a echeance

## Securite

Deux groupes sont fournis :

- `IT Technicien`
- `IT Manager`

Les droits sont definis dans :

```text
it_parc/security/ir.model.access.csv
it_parc/security/parc_securite.xml
```

## Structure

```text
it_parc/
  __init__.py
  __manifest__.py
  controllers/
  data/
  models/
  report/
  security/
  static/
  views/
  wizards/
```

## Notes de depot

Les fichiers de travail locaux ne doivent pas etre pousses :

- cahier des charges
- scripts temporaires
- documents de travail
- environnements virtuels
- caches Python
- logs

Le `.gitignore` du depot protege ces elements.
