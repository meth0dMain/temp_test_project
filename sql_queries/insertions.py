"""
Contains SQL statements that handle the insertion of new records into a database.
"""

INSERT_USERS = """
INSERT INTO users (user_id, age, gender, country) VALUES (?, ?, ?, ?)
ON CONFLICT(user_id) DO UPDATE SET age=excluded.age, gender=excluded.gender, country=excluded.country;
"""
INSERT_SUBSCRIPTION = """
INSERT INTO subscriptions (user_id, subscription_type, monthly_revenue, join_date, last_payment_date, plan_duration)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT(user_id) DO UPDATE SET
subscription_type = excluded.subscription_type,
monthly_revenue = excluded.monthly_revenue,
join_date = excluded.join_date,
last_payment_date = excluded.last_payment_date,
plan_duration = excluded.plan_duration;
"""
INSERT_DEVICE = """
INSERT INTO devices (device_name) VALUES (?) ON CONFLICT(device_name) DO NOTHING;
"""
INSERT_USER_DEVICE = """
INSERT INTO user_devices (user_id, device_id) VALUES (?, ?)
ON CONFLICT(user_id, device_id) DO UPDATE SET
device_id = excluded.device_id;
"""
INSERT_VIEWING_ACTIVITY = """
INSERT INTO viewing_activity (user_id, movies_watched, series_watched)
VALUES (?, ?, ?)
ON CONFLICT(user_id) DO UPDATE SET
movies_watched = excluded.movies_watched,
series_watched = excluded.series_watched;
"""
INSERT_PROFILE = """
INSERT INTO profiles (user_id, active_profiles, household_profile_ind)
VALUES (?, ?, ?)
ON CONFLICT(user_id) DO UPDATE SET
active_profiles = excluded.active_profiles,
household_profile_ind = excluded.household_profile_ind;
"""
