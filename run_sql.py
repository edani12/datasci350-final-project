import sqlite3

# The SQL files (02_clean_data.sql and 03_descriptive_stats.sql) cannot be run
# directly in VS Code without an active database connection. This script serves
# as a workaround by connecting to the SQLite database via Python and executing
# both SQL files in order, replicating what would otherwise require a dedicated
# SQL client or CLI setup.


conn = sqlite3.connect('data/healthcare_demographics.db')

with open('scripts/02_clean_data.sql', 'r') as f:
    conn.executescript(f.read())

with open('scripts/03_descriptive_stats.sql', 'r') as f:
    conn.executescript(f.read())

conn.commit()
conn.close()
print("Done!")