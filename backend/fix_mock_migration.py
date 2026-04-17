import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check if migration already recorded
cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app='mock_interview' AND name='0001_initial'")
count = cursor.fetchone()[0]

if count == 0:
    # Add migration record
    cursor.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
        ('mock_interview', '0001_initial', datetime.now().isoformat())
    )
    conn.commit()
    print("✓ Migration record added successfully")
else:
    print("✓ Migration record already exists")

# Verify tables exist
tables = [
    'mock_interview_interviewquestion',
    'mock_interview_mockinterviewsession',
    'mock_interview_useranswer'
]

for table in tables:
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (table,))
    exists = cursor.fetchone()[0]
    if exists:
        print(f"✓ Table {table} exists")
    else:
        print(f"✗ Table {table} MISSING")

conn.close()
print("\nDatabase is ready!")
