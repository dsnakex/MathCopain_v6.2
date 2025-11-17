#!/usr/bin/env python3
"""Fix pg_hba.conf for mathcopain database"""

import shutil

backup_file = '/etc/postgresql/16/main/pg_hba.conf.backup'
target_file = '/etc/postgresql/16/main/pg_hba.conf'

# Read backup
with open(backup_file, 'r') as f:
    lines = f.readlines()

# Modify lines
new_lines = []
for i, line in enumerate(lines):
    # Change postgres peer to trust
    if line.strip() == 'local   all             postgres                                peer':
        new_lines.append('local   all             postgres                                trust\n')
    # Add mathcopain_user rule before the general "local all all peer" line
    elif line.strip() == 'local   all             all                                     peer':
        new_lines.append('local   all             mathcopain_user                         md5\n')
        new_lines.append(line)
    else:
        new_lines.append(line)

# Write new file
with open(target_file, 'w') as f:
    f.writelines(new_lines)

print("✓ pg_hba.conf fixed")
