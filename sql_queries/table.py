"""
Contains SQL statements that handle the table creations in a database.
"""

USERS_TABLE = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                age INTEGER CHECK(age >= 18 AND age <= 130),
                gender TEXT CHECK(gender IN ('Male', 'Female')),
                country TEXT
            );
            """
SUBSCRIPTIONS_TABLE = """
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                subscription_type TEXT CHECK(subscription_type IN ('Basic', 'Premium', 'Standard')),
                monthly_revenue REAL,
                join_date TEXT,
                last_payment_date TEXT,
                plan_duration TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            """
DEVICES_TABLE = """
            CREATE TABLE IF NOT EXISTS devices (
                device_id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT UNIQUE CHECK(device_name IN ('Smart TV', 'Smartphone', 'Tablet', 'Laptop'))
            );
            """
USER_DEVISES_TABLE = """
            CREATE TABLE IF NOT EXISTS user_devices (
                user_id INTEGER,
                device_id INTEGER,
                PRIMARY KEY (user_id, device_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (device_id) REFERENCES devices(device_id)
            );
            """
VIEWING_ACTIVITY_TABLE = """
            CREATE TABLE IF NOT EXISTS viewing_activity  (
                user_id INTEGER PRIMARY KEY,
                movies_watched INTEGER,
                series_watched INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            """
PROFILES_TABLE = """
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                active_profiles INTEGER,
                household_profile_ind INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            """
