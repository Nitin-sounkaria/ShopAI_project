import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store.db")

print("Using database:")
print(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Show current tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

print("\nTables before migration:")
for table in cursor.fetchall():
    print(" -", table[0])


# -------------------------
# USERS TABLE
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT
)
""")


# -------------------------
# USER PREFERENCES TABLE
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT PRIMARY KEY,
    prefers_organic INTEGER,
    max_price REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# -------------------------
# ADD USER ID TO ORDERS
# -------------------------

cursor.execute("PRAGMA table_info(orders)")
columns = [row[1] for row in cursor.fetchall()]

print("\nOrders columns before migration:")
print(columns)

if "user_id" not in columns:
    print("Adding user_id to orders...")

    cursor.execute("""
    ALTER TABLE orders
    ADD COLUMN user_id TEXT
    """)

    print("user_id added.")
else:
    print("user_id already exists.")


# -------------------------
# CREATE USER
# -------------------------

cursor.execute("""
INSERT OR IGNORE INTO users (id, name)
VALUES (?, ?)
""", ("user_001", "Nitin"))


# -------------------------
# ASSIGN EXISTING ORDERS
# -------------------------

cursor.execute("""
UPDATE orders
SET user_id = ?
WHERE user_id IS NULL
""", ("user_001",))

print("Existing orders assigned to user_001.")


# -------------------------
# CREATE DEFAULT PREFERENCES
# -------------------------

cursor.execute("""
INSERT OR IGNORE INTO user_preferences
(user_id, prefers_organic, max_price)
VALUES (?, ?, ?)
""", ("user_001", None, None))


conn.commit()


# -------------------------
# VERIFY
# -------------------------

print("\nUsers:")
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

print("\nUser preferences:")
cursor.execute("SELECT * FROM user_preferences")
print(cursor.fetchall())

print("\nOrders:")
cursor.execute("""
SELECT id, product_id, product_name, price, user_id
FROM orders
""")

for row in cursor.fetchall():
    print(row)


conn.close()

print("\n✅ MIGRATION COMPLETED")
