#!/usr/bin/env python3

import sqlite3
import logging

log = logging.getLogger("leprechaun.db")

def create_database(output):

  db_file = output + ".db"
  db_connection = sqlite3.connect(db_file)
  create_table(db_connection)
  log.debug("Database created %s",db_file)
  return db_connection

def create_table(connection):
  """Creates a new table in the database.

  Parameters:
    - connection: The connection to the SQLite database.

  """
  cursor = connection.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS rainbow
    (id INTEGER PRIMARY KEY, digest TEXT, word TEXT)""")
  connection.commit()

def save_pair(connection, digest, word):
  """Save both the original word and its digest into the database.

  Parameters:
    - connection: The connection to the SQLite database.
    - digest: The digest of the plaintext word; acts as the primary key.
    - word: The plaintext word.

  """
  cursor = connection.cursor()
  _t = (digest, word)

  cursor.execute("""INSERT INTO rainbow
    VALUES (NULL, ?, ?)""", _t)
  
  connection.commit()

def get_password(connection, digest):
  """Query the database for the digest and return the plaintext password.

  Parameters:
    - connection: The connection to the SQLite database.
    - digest: The digest of the plaintext word.

  Returns:
    - The plaintext password associated with the given digest.
  
  """
  cursor = connection.cursor()
  _t = (digest,)
  cursor.execute("SELECT word FROM rainbow WHERE digest=?", _t)
  return cursor.fetchone()
