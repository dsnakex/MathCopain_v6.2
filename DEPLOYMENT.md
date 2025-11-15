# Guide de Déploiement - MathCopain v6.3.0

Guide complet pour déployer MathCopain en production.

---

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Migration depuis v6.2](#migration-depuis-v62)
5. [Déploiement Local](#déploiement-local)
6. [Déploiement Cloud](#déploiement-cloud)
7. [Maintenance](#maintenance)
8. [Backup & Restore](#backup--restore)
9. [Troubleshooting](#troubleshooting)
10. [Sécurité](#sécurité)

---

## Prérequis

### Système
- **Python**: 3.11 ou supérieur
- **OS**: Linux, macOS, ou Windows
- **RAM**: 512 MB minimum, 1 GB recommandé
- **Espace disque**: 100 MB minimum

### Compétences
- Connaissance basique de Python
- Connaissance basique du terminal/ligne de commande
- (Optionnel) Git pour cloner le repository

---

## Installation

### 1. Cloner le Repository

```bash
git clone https://github.com/dsnakex/MathCopain_v6.2.git
cd MathCopain_v6.2
```

### 2. Créer Environnement Virtuel

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Installer Dépendances

```bash
pip install -r requirements.txt
```

#### Dépendances Principales
- `streamlit==1.31.0` - Framework web
- `bcrypt==5.0.0` - Hashing sécurisé PINs
- `pydantic==2.12.4` - Validation inputs
- `pytest==7.4.3` - Tests (dev)
- `pytest-cov==4.1.0` - Coverage (dev)

### 4. Vérifier Installation

```bash
python -c "import streamlit; import bcrypt; import pydantic; print('✅ Installation OK')"
```

---

## Configuration

### 1. Configuration Fichiers

```bash
# Créer répertoire backups
mkdir -p backups

# Initialiser fichiers données (si premier démarrage)
python -c "from authentification import init_fichier_securise; init_fichier_securise()"
```

### 2. Variables d'Environnement (Optionnel)

Créer fichier `.env`:

```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### 3. Configuration Streamlit

Créer `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "localhost"
headless = true
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## Migration depuis v6.2

### ⚠️ Important: Backup Obligatoire

```bash
# 1. Créer backup données actuelles
python backup_restore.py backup

# 2. Vérifier backup créé
python backup_restore.py list
```

### Migration PINs vers Bcrypt

**PINs en plaintext (v6.2) → Hash bcrypt (v6.3)**

```bash
# 1. Dry-run (test sans modifications)
python migrate_pins_to_bcrypt.py --dry-run

# 2. Migration réelle
python migrate_pins_to_bcrypt.py

# 3. Vérifier résultat
# Tester connexion utilisateurs existants
```

**Note**: Nouveaux comptes créés dans v6.3 utilisent automatiquement bcrypt.

### Vérification Post-Migration

1. ✅ Backup créé
2. ✅ PINs migrés (affichage confirmation dans console)
3. ✅ Test connexion utilisateurs existants
4. ✅ Application démarre sans erreur

---

## Déploiement Local

### Développement

```bash
# Activer environnement virtuel
source venv/bin/activate  # Linux/macOS
# OU
venv\Scripts\activate  # Windows

# Lancer application
streamlit run app.py
```

Application accessible sur: `http://localhost:8501`

### Production Locale

```bash
# Lancer en mode production
streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
```

### Systemd Service (Linux)

Créer `/etc/systemd/system/mathcopain.service`:

```ini
[Unit]
Description=MathCopain v6.3.0
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/mathcopain
ExecStart=/var/www/mathcopain/venv/bin/streamlit run app.py --server.port 8501 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Activer service
sudo systemctl daemon-reload
sudo systemctl enable mathcopain
sudo systemctl start mathcopain

# Vérifier status
sudo systemctl status mathcopain
```

---

## Déploiement Cloud

### Streamlit Cloud (Recommandé)

**Avantages**: Gratuit, simple, HTTPS automatique

1. **Créer compte** sur [streamlit.io](https://streamlit.io/)

2. **Connecter repository GitHub**

3. **Configurer déploiement**:
   - Main file: `app.py`
   - Python version: 3.11
   - Requirements: `requirements.txt`

4. **Déployer** ✅

5. **URL publique**: `https://votre-app.streamlit.app`

### Heroku

**Fichiers requis**:

`Procfile`:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

`setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

**Déploiement**:
```bash
heroku create mathcopain
git push heroku main
heroku open
```

### AWS EC2

1. **Lancer instance EC2** (Ubuntu 22.04 LTS)
2. **SSH dans instance**
3. **Installer Python 3.11**:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv -y
   ```
4. **Cloner projet et installer dépendances**
5. **Configurer Nginx reverse proxy** (port 80 → 8501)
6. **Configurer SSL** (Let's Encrypt)
7. **Lancer avec systemd**

### Docker (Avancé)

`Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build
docker build -t mathcopain:6.3.0 .

# Run
docker run -p 8501:8501 mathcopain:6.3.0
```

---

## Maintenance

### Backups Automatiques

**Cron Job (Linux)**:

```bash
# Éditer crontab
crontab -e

# Ajouter ligne (backup quotidien à 2h du matin)
0 2 * * * cd /path/to/mathcopain && /path/to/venv/bin/python backup_restore.py backup
```

### Nettoyage Backups

```bash
# Garder seulement 30 derniers backups
python backup_restore.py cleanup --keep 30
```

### Logs

```bash
# Logs Streamlit
tail -f ~/.streamlit/logs/streamlit.log

# Logs systemd (si service)
sudo journalctl -u mathcopain -f
```

### Mises à Jour

```bash
# 1. Backup données
python backup_restore.py backup

# 2. Pull dernières modifications
git pull origin main

# 3. Mettre à jour dépendances
pip install -r requirements.txt --upgrade

# 4. Redémarrer
# Local: Ctrl+C puis relancer
# Systemd: sudo systemctl restart mathcopain
```

---

## Backup & Restore

### Créer Backup

```bash
# Backup dans répertoire par défaut (backups/)
python backup_restore.py backup

# Backup dans répertoire personnalisé
python backup_restore.py backup --output /path/to/backups
```

### Lister Backups

```bash
python backup_restore.py list
```

**Exemple sortie**:
```
📦 Backups disponibles (5):

Date                 Utilisateurs    Taille     Fichier
--------------------------------------------------------------------------------
2025-01-15T14:30:00  15              0.05 MB    mathcopain_backup_20250115_143000.json
2025-01-14T14:30:00  12              0.04 MB    mathcopain_backup_20250114_143000.json
...
```

### Restaurer Backup

```bash
# Dry-run (test sans modifications)
python backup_restore.py restore backups/mathcopain_backup_20250115_143000.json

# Restauration réelle
python backup_restore.py restore backups/mathcopain_backup_20250115_143000.json --confirm
```

**⚠️ Attention**: Restauration écrase données actuelles. Backup automatique créé avant restauration.

---

## Troubleshooting

### Application ne démarre pas

```bash
# Vérifier dépendances installées
pip list | grep streamlit
pip list | grep bcrypt

# Réinstaller dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier erreurs Python
python -c "import app"
```

### Erreur "Module not found"

```bash
# Activer environnement virtuel
source venv/bin/activate

# Installer dépendances manquantes
pip install -r requirements.txt
```

### Port 8501 déjà utilisé

```bash
# Linux/macOS: Trouver processus
lsof -i :8501

# Windows: Trouver processus
netstat -ano | findstr :8501

# Tuer processus ou changer port
streamlit run app.py --server.port 8502
```

### PINs ne fonctionnent plus après migration

1. Vérifier migration complétée: `python migrate_pins_to_bcrypt.py --dry-run`
2. Vérifier format hash bcrypt dans `utilisateurs_securises.json`
3. Restaurer backup si nécessaire: `python backup_restore.py restore BACKUP_FILE --confirm`

### Tests échouent

```bash
# Installer dépendances dev
pip install pytest pytest-cov

# Lancer tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=. --cov-report=html
```

---

## Sécurité

### Bonnes Pratiques

✅ **Obligatoire**:
- Migration PINs vers bcrypt (v6.3.0)
- Backups réguliers (quotidiens)
- HTTPS en production (Let's Encrypt gratuit)
- Mises à jour sécurité régulières

✅ **Recommandé**:
- Firewall configuré (seulement ports 80/443 ouverts)
- Rate limiting au niveau reverse proxy (Nginx)
- Logs centralisés
- Monitoring (uptime, erreurs)

⚠️ **À Éviter**:
- ❌ Exposer port 8501 directement (utiliser reverse proxy)
- ❌ Stocker backups sans encryption
- ❌ Partager fichiers JSON utilisateurs
- ❌ Désactiver rate limiting PIN

### Checklist Sécurité

- [ ] PINs hashés avec bcrypt (v6.3.0+)
- [ ] Rate limiting activé (5 tentatives/15min)
- [ ] HTTPS configuré
- [ ] Backups automatisés
- [ ] Logs activés
- [ ] Fichiers sensibles dans .gitignore
- [ ] Dépendances à jour
- [ ] Tests passent (513/513)

---

## Support

### Documentation
- **README.md**: Vue d'ensemble projet
- **CHANGELOG.md**: Historique versions
- **TASK_TRACKER.md**: Progression développement

### Tests
```bash
# Lancer tous tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=. --cov-report=term
```

### Contact
- **Repository**: https://github.com/dsnakex/MathCopain_v6.2
- **Issues**: https://github.com/dsnakex/MathCopain_v6.2/issues

---

**Version**: 6.3.0
**Dernière mise à jour**: 2025-01-15
**Auteur**: dsnakex
