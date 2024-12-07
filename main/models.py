from django.db import models

# Create your models here.
import psycopg2

DB_CONFIG = {
    "dbname": "eventsync",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def get_db_connection():
    """Establish and return a connection to the database."""
    return psycopg2.connect(**DB_CONFIG)
