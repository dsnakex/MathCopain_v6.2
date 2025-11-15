# 🤖 CLAUDE CODE BRIEFING - MathCopain v6.3
## Instructions pour Claude Code - Implémentation & Refactoring

**Objectif :** Vous êtes Claude Code. Ce document = vos instructions de travail pour implémenter v6.3.

---

## 🎯 Mission Globale

Transformer MathCopain v6.2 (4894 lignes fragiles) en v6.3 (production-ready) en 3 semaines.

**Votre rôle :** Implémenter les tâches code du TASK_TRACKER.md avec précision et tests.

---

## 📋 PHASES & VÔTRE RÔLE

### Phase 1 : Tests Unitaires (S1 J1-J5)
**Votre focus :** Créer infrastructure tests + tests prioritaires

#### Responsabilités
- [ ] Créer `tests/` directory structure
- [ ] Configurer pytest (conftest.py, fixtures)
- [ ] Écrire tests complets pour:
  - `exercices_utils.py` (additions, soustractions)
  - `division_utils.py` (divisions + restes)
  - `monnaie_utils.py` (euros, centimes)
  - `mesures_utils.py` (longueurs, masses, volumes)
  - `decimaux_utils.py`
  - `adaptive_system.py`
  - `skill_tracker.py`
  - `utilisateur.py`

#### Qualité Standards
```python
# Chaque test doit:
✅ Avoir docstring claire
✅ Tester cas normal + limites + erreurs
✅ Éviter dépendances externes (mock si nécessaire)
✅ Isolé (1 test = 1 fonction)
✅ Nommage: test_[fonction]_[cas]

# Exemple:
def test_generate_addition_normal_range():
    """Test addition generates numbers in 1-100 range."""
    result = generate_addition(level=1)
    assert 1 <= result[0] <= 100
    assert 1 <= result[1] <= 100
    assert isinstance(result[2], int)

def test_generate_addition_edge_case_zero():
    """Test addition with zero edge case."""
    result = generate_addition(level=1, min_val=0)
    assert result[0] >= 0
```

#### Git Commits
```
Jour 1: git commit -m "feat: setup pytest infrastructure"
Jour 2: git commit -m "test: add addition/subtraction unit tests"
Jour 3: git commit -m "test: add division unit tests"
Jour 4: git commit -m "test: add money and measurements tests"
Jour 5: git commit -m "test: add adaptive system & tracking tests"
```

---

### Phase 2 : Refactoring Critique (S1 J2 parallel, S1 J5 focus)
**Votre focus :** Restructurer app.py sans breaking changes

#### Tasks
1. **Créer core/ directory structure**
   ```
   core/
   ├── __init__.py           # Exports public API
   ├── exercise_generator.py # Extract from app.py
   ├── adaptive_system.py    # Existing, move here
   ├── skill_tracker.py      # Existing, move here
   ├── data_manager.py       # NEW - validation + atomic writes
   ├── authenticator.py      # Extract from utilisateur.py
   ├── session_manager.py    # NEW - session state
   └── logger.py             # NEW - structured logging
   ```

2. **Refactor app.py → 200 lignes**
   ```python
   # app.py structure AFTER refactor:
   
   import streamlit as st
   from core import (
       SessionManager, 
       ExerciseGenerator,
       SkillTracker,
       SkillTracker
   )
   from ui import render_sidebar, render_main_area
   
   def main():
       # Initialize session
       sm = SessionManager()
       
       # Render UI
       with st.sidebar:
           render_sidebar(sm)
       
       render_main_area(sm)
   
   if __name__ == "__main__":
       main()
   ```

3. **Create ui/ directory structure**
   ```
   ui/
   ├── __init__.py
   ├── sidebar.py        # Sidebar rendering
   ├── exercise_view.py  # Exercise display
   ├── dashboard_view.py # Stats/progress
   └── utils.py          # UI helpers
   ```

#### Import Rules (CRITICAL)
```python
# ALLOWED:
core/ → core/ (imports within core)
ui/ → core/ (ui uses core logic)
app.py → core/ + ui/ (orchestration)
tests/ → everything

# FORBIDDEN (WILL CREATE BUGS):
core/ → ui/ (circular import!)
ui/ → ui/ (cross-module imports)
```

#### Git Commit
```
git commit -m "refactor: separate concerns (core vs ui)"
```

#### Quality Checklist
- [ ] All imports follow rules above
- [ ] No circular dependencies (check: grep -r "import app")
- [ ] app.py < 300 lignes
- [ ] core/ modules have type hints
- [ ] Tests still pass after refactor

---

### Phase 2 : CI/CD Setup (S2 J6-J7)
**Votre focus :** Automate testing pipeline

#### Tasks
1. **Create `.github/workflows/tests.yml`**
   ```yaml
   name: Tests & Quality
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ['3.9', '3.10', '3.11']
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: ${{ matrix.python-version }}
         - name: Install dependencies
           run: |
             pip install --upgrade pip
             pip install -r requirements.txt
         - name: Run tests
           run: pytest tests/ -v --tb=short
         - name: Coverage report
           run: pytest --cov=core --cov=ui --cov-report=term --cov-report=xml
         - name: Upload coverage
           uses: codecov/codecov-action@v3
         - name: Lint with flake8
           run: flake8 . --statistics --show-source
         - name: Lint with pylint
           run: pylint core/ ui/ --disable=C0111,C0103
   ```

2. **Create `.flake8` config**
   ```
   [flake8]
   max-line-length = 120
   exclude = .git,__pycache__,tests/
   ignore = E501, W503
   ```

3. **Create `pyproject.toml` for pytest**
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = "test_*.py"
   python_classes = "Test*"
   python_functions = "test_*"
   addopts = "-v --strict-markers"
   ```

#### Git Commits
```
git commit -m "ci: add GitHub Actions workflow"
git commit -m "ci: add linting config (flake8, pylint)"
```

---

### Phase 2 : Coverage Improvement (S2 J8-J9)
**Votre focus :** Reach 80%+ coverage

#### Tasks
1. **Run coverage analysis**
   ```bash
   pytest --cov=core --cov=ui --cov-report=html
   # Open htmlcov/index.html to see gaps
   ```

2. **For each module < 70%:**
   - Add missing tests for branches (if/else)
   - Test error paths (exceptions)
   - Test integration between modules
   - Target each module ≥ 80%

3. **Optimize test speed**
   ```bash
   pytest tests/ --durations=10  # Identify slow tests
   pip install pytest-xdist
   pytest -n auto  # Parallel execution
   ```

#### Git Commit
```
git commit -m "test: improve coverage to 80%+ with integration tests"
```

---

### Phase 3 : Security (S3 J11-J12)
**Votre focus :** Implement encryption & validation

#### Task 1 : PIN Hashing with bcrypt

Create `core/security.py`:
```python
from bcrypt import hashpw, checkpw, gensalt
import logging

logger = logging.getLogger(__name__)

class PinManager:
    @staticmethod
    def hash_pin(pin: str) -> str:
        """Hash PIN with bcrypt (rounds=12 = ~100ms per hash)."""
        pin_bytes = pin.encode('utf-8')
        salt = gensalt(rounds=12)
        return hashpw(pin_bytes, salt).decode('utf-8')
    
    @staticmethod
    def verify_pin(pin_input: str, pin_hash: str) -> bool:
        """Verify PIN against hash (timing-safe)."""
        try:
            return checkpw(pin_input.encode('utf-8'), pin_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"PIN verification error: {e}")
            return False
```

Update `core/authenticator.py`:
```python
# BEFORE:
if user_data['pin'] == input_pin:
    return True

# AFTER:
if PinManager.verify_pin(input_pin, user_data['pin_hash']):
    return True
```

Create migration script:
```python
# scripts/migrate_pins_to_bcrypt.py
import json
import os
from core.security import PinManager

def migrate():
    """Migrate plaintext PINs to bcrypt hashes."""
    old_file = "utilisateurs_securises.json"
    new_file = "utilisateurs_securises.json.new"
    
    with open(old_file, 'r') as f:
        users = json.load(f)
    
    for user_id, user_data in users.items():
        if 'pin' in user_data:
            user_data['pin_hash'] = PinManager.hash_pin(user_data['pin'])
            del user_data['pin']
    
    with open(new_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"✅ Migration complete. Review {new_file}, then:")
    print(f"   mv {new_file} {old_file}")

if __name__ == "__main__":
    migrate()
```

#### Task 2 : Input Validation

Create `core/validators.py`:
```python
from pydantic import BaseModel, validator
import re

class UserProfile(BaseModel):
    name: str
    email: str
    grade: str  # CE1, CE2, CM1, CM2
    
    @validator('name')
    def validate_name(cls, v):
        if not (1 <= len(v) <= 50):
            raise ValueError('Name must be 1-50 characters')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\']+$', v):
            raise ValueError('Invalid characters in name')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('grade')
    def validate_grade(cls, v):
        if v not in ['CE1', 'CE2', 'CM1', 'CM2']:
            raise ValueError('Invalid grade')
        return v
```

#### Task 3 : Rate Limiting

Create rate limiter in `core/security.py`:
```python
class PinGuardian:
    def __init__(self, max_attempts=3, lockout_minutes=15):
        self.max_attempts = max_attempts
        self.lockout_minutes = lockout_minutes
        self.attempts = {}  # {user_id: (attempts, timestamp)}
    
    def can_attempt(self, user_id: str) -> bool:
        """Check if user can attempt PIN."""
        if user_id not in self.attempts:
            return True
        
        attempts, timestamp = self.attempts[user_id]
        elapsed = (time.time() - timestamp) / 60
        
        if elapsed > self.lockout_minutes:
            del self.attempts[user_id]
            return True
        
        return attempts < self.max_attempts
    
    def record_attempt(self, user_id: str, success: bool):
        """Record PIN attempt."""
        if success:
            if user_id in self.attempts:
                del self.attempts[user_id]
        else:
            if user_id not in self.attempts:
                self.attempts[user_id] = (1, time.time())
            else:
                attempts, _ = self.attempts[user_id]
                self.attempts[user_id] = (attempts + 1, time.time())
```

#### Git Commits
```
git commit -m "security: implement bcrypt PIN hashing"
git commit -m "security: add input validation with pydantic"
git commit -m "security: add rate limiting for PIN attempts"
```

---

### Phase 3 : Backup & Release (S3 J14-J15)
**Votre focus :** Production hardening

#### Task : Backup Scripts

Create `scripts/backup.py`:
```python
#!/usr/bin/env python3
import os
import shutil
import tarfile
from datetime import datetime

def backup_users():
    """Create backup of user data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_name = f"{backup_dir}/backup_{timestamp}"
    
    # Create tar.gz
    with tarfile.open(f"{backup_name}.tar.gz", "w:gz") as tar:
        tar.add("data/users/", arcname="users")
        tar.add("utilisateurs_securises.json", arcname="utilisateurs_securises.json")
    
    print(f"✅ Backed up to {backup_name}.tar.gz")
    return backup_name

if __name__ == "__main__":
    backup_users()
```

Create `scripts/restore.py`:
```python
#!/usr/bin/env python3
import tarfile
import json
import sys

def restore_backup(backup_file):
    """Restore from backup."""
    # Extract
    with tarfile.open(backup_file, "r:gz") as tar:
        tar.extractall()
    
    # Validate
    with open("utilisateurs_securises.json", "r") as f:
        data = json.load(f)
    
    print(f"✅ Restored from {backup_file}")
    print(f"   Users: {len(data)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python restore.py <backup_file>")
        sys.exit(1)
    restore_backup(sys.argv[1])
```

#### Task : Version Bump & Release

1. Update version in app.py:
   ```python
   __version__ = "6.3.0"
   ```

2. Create CHANGELOG entry (see CHANGELOG.md template)

3. Create GitHub Release:
   ```bash
   git tag -a v6.3.0 -m "Production ready v6.3.0"
   git push origin v6.3.0
   # Then go to GitHub → Create Release
   ```

#### Git Commits
```
git commit -m "ops: add backup/restore scripts"
git commit -m "release: v6.3.0 - Production ready"
```

---

## 📚 IMPORTANT REMINDERS

### For Every Code Change
1. ✅ Write tests FIRST (TDD)
2. ✅ Run pytest locally before pushing
3. ✅ Check coverage: `pytest --cov`
4. ✅ Lint code: `flake8 .` and `pylint core/`
5. ✅ Atomic commits (one feature = one commit)
6. ✅ Meaningful commit messages

### Quality Standards
```python
# ❌ DON'T
def fn(x):
    pass

# ✅ DO
def validate_user_input(user_name: str) -> bool:
    """Validate user input meets requirements.
    
    Args:
        user_name: Username to validate
    
    Returns:
        True if valid, False otherwise
    
    Raises:
        ValueError: If name too long
    """
    if len(user_name) > 50:
        raise ValueError("Name too long")
    return True
```

### Type Hints Required
```python
# ✅ Use type hints everywhere
def generate_exercice(level: int, type: str) -> Tuple[int, int, int]:
    """Generate exercise tuple."""
    ...

def verify_answer(user_answer: int, correct_answer: int) -> bool:
    """Check if answer is correct."""
    ...
```

### No Print() - Use Logger
```python
# ❌ BAD
print("User logged in")

# ✅ GOOD
import logging
logger = logging.getLogger(__name__)
logger.info(f"User {user_id} logged in")
```

---

## 🎯 SUCCESS CRITERIA

### End of Each Phase

**S1 End (Jour 5):**
- [ ] 8 test files created
- [ ] 45-50% coverage achieved
- [ ] All tests passing
- [ ] Refactor app.py complete
- [ ] 5 clean commits

**S2 End (Jour 10):**
- [ ] CI/CD pipeline working (green builds)
- [ ] 80%+ coverage
- [ ] All tests passing
- [ ] 5-6 commits
- [ ] Architecture docs created

**S3 End (Jour 15):**
- [ ] Security features implemented
- [ ] Backup/restore scripts working
- [ ] v6.3.0 tagged & released
- [ ] Full documentation complete
- [ ] Ready for production deployment

---

## 🚨 BLOCKERS & ESCALATION

If you encounter:
- **Architectural blocker** → Ask for clarification in DECISIONS_LOG.md
- **Dependency issue** → Update requirements.txt + document why
- **Test failing unexpectedly** → Debug + add edge case
- **Performance problem** → Profile first, then optimize

---

## 📞 HANDOFF BETWEEN PHASES

After each phase completion:
1. Run full test suite: `pytest tests/ -v`
2. Check coverage: `pytest --cov --cov-report=term`
3. Review all commits: `git log --oneline`
4. Create summary in TASK_TRACKER.md
5. Tag version: `git tag -a v6.3.X`

---

**Good luck! You got this! 🚀**

Questions? Check DECISIONS_LOG.md for context, or ask for clarification.
