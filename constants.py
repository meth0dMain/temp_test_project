"""
Defines constants and lists for validation and data processing.
"""

from country_list import countries_for_language

VALID_SUBSCRIPTION_TYPES = ["Basic", "Premium", "Standard"]
VALID_DEVICES = ["Smart TV", "Smartphone", "Tablet", "Laptop"]
VALID_GENDERS = ["Male", "Female"]
VALID_COUNTRIES = list(dict(countries_for_language("en")).values())

INT_COLUMNS = [
    "User ID",
    "Monthly Revenue",
    "Active Profiles",
    "Household Profile Ind",
    "Movies Watched",
    "Series Watched",
]
DATE_COLUMNS = ["Join Date", "Last Payment Date"]
