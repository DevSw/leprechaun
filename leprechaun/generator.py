#!/usr/bin/env python3

import itertools
import string

def digit_generator(limit):
  """Generates a string of digits to be appened to another string.

  Parameters:
    - limit: The upper limit of the range of the length of digits to be
      generated.

  Yields:
    - A string of digits joined together.

  """
  digits = tuple(string.digits)
  for length in range(1, limit+1):
    for digit in itertools.product(digits, repeat=length):
      yield "".join(digit)

def _word_generator(limit):
  """Generates a list of words up to length specified by 'limit'.

  Parameters:
    - limit: The upper limit of the range of the word length.

  Yields:
    - A range of words with a maximum length given 'limit'.

  """
  characters = tuple(string.ascii_letters + " ")
  for length in range(1, limit+1):
    for char in itertools.product(characters, repeat=length):
      yield "".join(char)

def create_wordlist(file_name, word_limit=8, digit_limit=0):
  """Generates a wordlist plaintext file.

  Parameters:
    - file_name: The name to give the wordlist file.
    - word_limit: The upper limit of the range of the word length. Passed to
      "_word_generator"; default=8.
    - digit_limit: The upper limit of the range of digits to append to the word.
      Passed to "digit_generator"; default=0.

  """

  log = logging.getLogger("leprechaun.generator")
  try:
    with open(file_name, "w") as output:
      for word in _word_generator(word_limit):
        print(word, file=output)

        for digit in digit_generator(digit_limit):
          word = word + digit
          print(word, file=output)
  except IOError as err:
    log.error("File yar error: %s",str(err))
    #print("File error: " + str(err))
