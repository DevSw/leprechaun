#############
Leprechaun.py
#############
A simple rainbow table generator written in **Python 3**.

********
Synopsis
********
Leprechaun.py is a simple Python program used for generating cryptographic
rainbow tables. This script can compute hashes using the MD5, SHA1, SHA256 and
SHA512 algorithms. Leprechaun can hash any arbitrary number of plaintext files,
as long as they're within the same directory. Or, if you're a normal person
without a huge directory filled with wordlists, you can hash one single file.
The choice is yours! 

************
Installation
************
Leprechaun is available for download from PyPI using ``pip``, just like
everything else! ::

    $ mkdir DIRECTORY
    $ cd DIRECTORY
    $ virtualenv -p python3 .
    $ pip install leprechaun

*****
Usage
*****
``leprechaun [-h] [-g] [-l LENGTH] [-d] [-o OUTPUT] [--debug] [-m] [-s] [-s2] [-s3] [-s5] WORDLIST``
    
**arguments:** ::

    (Positional Arguments)
    WORDLIST                          The file name of the wordlist to hash,
                                      without the file extension

    (Optional Arguments)
    -h, --help                        Show this help message and exit

    (Wordlist Arguments)
    -f, --wordlist-folder             Hash all of the plaintext files in a
                                      folder, rather than a single file. The
                                      name of the folder will be set by the
                                      WORDLIST argument
    -g, --generate-wordlist           Generate a wordlist dynamically instead
                                      of using a pre-built one; the name of the
                                      dynamically generated wordlist will be set
                                      by the WORDLIST argument
    -l LENGTH, --word-length LENGTH   The maximum length of the words to be
                                      generated (default=8)

    (Output Arguments)
    -o OUTPUT, --output OUTPUT        Name of the rainbow table file, without
                                      the file extension (default=rainbow)
    -d, --use-database                Save the output to an SQLite DB instead
                                      of a plaintext file
    (Logging Arguments)
    --debug                           Print debug log messages

    (Hashing Arguments)
    -m, --md5                         Generate MD5 hashes of given passwords (default)
    -s, --sha1                        Generate SHA1 hashes of given passwords    
    -s2, --sha256                     Generate SHA256 hashes of given passwords    
    -s3, --sha384                     Generate SHA384 hashes of given passwords    
    -s5, --sha512                     Generate SHA512 hashes of given passwords

********
Examples
********
Below are a few simple examples on using Leprechaun.py. While not an exaustive
compilation of use cases, the program itself is quite simple to figure out on
one's own. ::

  # Create a rainbow table using the MD5 hashing algorithm.
  leprechaun /path/to/your/wordlist.txt

  # Create a rainbow table using the SHA-1 hashing algorithm.
  leprechaun -s /path/to/your/wordlist.txt

  # Create a rainbow table using the SHA-1 hashing algorithm, saving the
  # output in an SQLite database.
  leprechaun -s -d /path/to/your/wordlist.txt

  # Create a rainbow table using the SHA-256 hashing algorithm, hashing all of
  # the plaintext files in a given directory, saving the output in an SQLite
  # database.
  leprechaun -s2 -d -f /path/to/your/wordlists

  # Create a rainbow table using the SHA-256 hashing algorithm, hashing all of
  # the plaintext files in a given directory, saving the output in an SQLite
  # database named "patty"
  leprechaun -s2 -d -o patty -f /path/to/your/wordlists

*********
Wordlists
*********
Because any good wordlist contains several million lines of words, and several
million lines of anything takes up a heck of a lot of space, the previously
distributed wordlist is no longer being distributed. But don't fret! I've
uploaded that same wordlist onto the Internet for everyone to enjoy. You may
find it here_.

.. _here: https://mega.co.nz/#!mMdSWDgS!Bst3ZBdshvHo0uI5R_AZ8C2RZASSBnAmlnsEh4ffkoU

*******
License
*******

    The MIT License (MIT)

    Copyright (c) 2013 Zach Dziura

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
