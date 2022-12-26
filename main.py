import sqlite3

# Set up the database connection
conn = sqlite3.connect('vaccinations.db')
cursor = conn.cursor()

# Create the tables for the database
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        phone_number TEXT,
        national_id TEXT
    )
''')
cursor.execute('''
    CREATE TABLE centers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        address TEXT,
        vaccines TEXT
    )
''')
cursor.execute('''
    CREATE TABLE reservations (
        user_id INTEGER,
        center_id INTEGER,
        vaccine_name TEXT,
        date TEXT
    )
''')

# Commit the changes to the database
conn.commit()

# Define functions for the system
def register_user(name, email, password, phone_number, national_id):
    cursor.execute('''
        INSERT INTO users (name, email, password, phone_number, national_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, password, phone_number, national_id))
    conn.commit()

def login(email, password):
    cursor.execute('''
        SELECT * FROM users WHERE email=? AND password=?
    ''', (email, password))
    user = cursor.fetchone()
    if user:
        return user
    return None

def add_center(name, address, vaccines):
    cursor.execute('''
        INSERT INTO centers (name, address, vaccines)
        VALUES (?, ?, ?)
    ''', (name, address, vaccines))
    conn.commit()

def remove_center(center_id):
    cursor.execute('''
        DELETE FROM centers WHERE id=?
    ''', (center_id,))
    conn.commit()

def search_centers(name):
    cursor.execute('''
        SELECT * FROM centers WHERE name=?
    ''', (name,))
    centers = cursor.fetchall()
    if centers:
        return centers
    return None

def list_users():
    cursor.execute('''
        SELECT * FROM users
    ''', ())
    users = cursor.fetchall()
    if users:
        return users
    return None

def reserve_vaccination(user_id, center_id, vaccine_name):
    cursor.execute('''
        INSERT INTO reservations (user_id, center_id, vaccine_name)
        VALUES (?, ?, ?)
    ''', (user_id, center_id, vaccine_name))
    conn.commit()

def accept_reservation(user_id, date):
    cursor.execute('''
        UPDATE reservations SET date=? WHERE user_id=?
    ''', (date, user_id))
    conn.commit()

def get_vaccination_date(user_id):
    cursor.execute('''
        SELECT date FROM reservations WHERE user_id=?
    ''', (user_id,))
    date = cursor.fetchone()
    if date:
        return date[0]
# Register a user
register_user('John Smith', 'john@example.com', 'password123', '123-456-7890', '123-45-6789')

# Log in as the user
user = login('john@example.com', 'password123')
if user:
    print(f"Logged in as {user[1]}")
else:
    print("Invalid email or password")

# Add a vaccination center
add_center('Center 1', '123 Main St', 'Flu, Measles, Polio')

# Remove a vaccination center
remove_center(1)

# Search for vaccination centers
centers = search_centers('Center 1')
if centers:
    print(f"Found {len(centers)} centers")
else:
    print("No centers found")

# List registered users
users = list_users()
if users:
    print(f"Found {len(users)} users")
else:
    print("No users found")

# Reserve a vaccination
reserve_vaccination(1, 1, 'Flu')

# Accept a reservation and set a vaccination date
accept_reservation(1, '2022-01-01')

# Get the vaccination date for a user
date = get_vaccination_date(1)
if date:
    print(f"Your vaccination date is {date}")
else:
    print("You do not have vaccination date")

# have a vaccination date set yet")

# Close the database connection
conn.close()
