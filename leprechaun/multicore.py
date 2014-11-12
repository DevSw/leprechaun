#!/usr/bin/env python3

from multiprocessing import Process, cpu_count, JoinableQueue
from itertools import islice
from operator import truediv
import logging
import sys

log = logging.getLogger("leprechaun.multicore")

def cpuCount():
  """Retrieve the number of available cores on this system.

  Returns:
    - Number of available cores
  """

  result = 1
  try:
    result = cpu_count()
  except NotImplementedError:
    try:
      import psutil
      result = psutil.NUM_CPUS
    except:
      log.error("Cannot get number of cores, default to 1")

  return result

def file_len(fname):
  """Count the number of lines in file

  Parameters:
    - fname: file to read number of lines from

  Returns:
    - Number of lines in file
  """
  with open(fname,encoding="latin-1") as f:
    for i, l in enumerate(f):
      pass

  # Last line is not counted, so add it
  result = i + 1

  log.debug("%s, has %d lines",fname,result)
  return result

def start_multicore(wordlists,hashing_algorithm,output,use_database):
  """Start the multicore process.

  This devides words that needs to be hashed between cores

  Parameters:
    - wordlist: list containing words that need to be hashed
    - hashing_algorithm: which hashing algorithm should be used
    - output: format of the output file
    - use_database: if results should be stored in a database
  """

  global core_list
  chunk_size = 25000
  core_list = list()

  # Save 1 core for writing
  num_cores = cpuCount()
  num_hash_cores = num_cores -1

  result_queue = JoinableQueue()
  work_queue = JoinableQueue(num_hash_cores)

  # Start hash cores
  for core in range(num_hash_cores):

    cur_core = Process(target=hash_core_run,args=(core,result_queue,work_queue,hashing_algorithm))
    cur_core.start()
    core_list.append(cur_core)

  # Start output core
  out_core = Process(target=output_core_run,args=(result_queue,output,use_database))
  out_core.start()

  result_lines = []
  for wordlist in wordlists:
    with open(wordlist,encoding="latin-1") as fwordlist:

      for index,line in enumerate(fwordlist):
        result_lines.append(line)

        # Divides number of lines between hashcores
        if (index % chunk_size) == 0:
          work_queue.put(result_lines)
          result_lines = []

  if len(result_lines) > 0:
    work_queue.put(result_lines)

  # Send stop signal to hash cores
  for i in range(num_hash_cores):
    work_queue.put(None)

  # Wait for hashing cores to finish
  for hash_core in core_list:
    hash_core.join()

  # Send stop signal to output core to finish
  # and then wait for it
  result_queue.put(None)
  out_core.join()

  # Close Joinable queues
  work_queue.close()
  result_queue.close()

def output_core_run(result_queue,output,use_database):
  """Output process

  This process receives all generated hash values and writes it to the 
  appropiate output stream

  Parameters:
    - result_queue: queue containing the hash results
    - output: the output file format
    - use_database: if results should be stored in a database
  """

  from .rainbow import _hash_wordlist, create_rainbow_table, close_output_stream,write_output,create_output_stream

  core_log = logging.getLogger("leprechaun.core.output")
  core_log.debug("Output core started")

  # Open output stream
  output_stream = create_output_stream(output, use_database)

  while True:
    result_list = result_queue.get()

    # If result_list is None than al words are hashed so close the output stream
    if result_list is None:
      result_queue.task_done()
      break

    # store everything from the result list
    for result in result_list:
      write_output(output_stream,result,use_database)

    result_queue.task_done()

  close_output_stream(output_stream,use_database)
  core_log.debug("Output core exited")

def hash_core_run(core,result_queue,work_queue,hashing_algorithm):
  """Hash process

  This hash process will receive words from the work_queue and calculates
  them into hashes.

  Parameters:
    - core: identification of the process
    - result_queue: this queue will contain all the generated results that needs to be written
    - work_queue: containing words which needs to be hashed
    - hashing_algorithm: the hashing algorithm that should be used
  """

  from .rainbow import _hash_wordlist, create_rainbow_table, close_output_stream,write_output

  core_log = logging.getLogger("leprechaun.core.hash")
  core_log.debug("Hash-Core[%d] started",core)

  while True:
    work_list = work_queue.get()
    result_list = list()

    # if work_list is None that means input is empty, so finish
    if work_list is None:
      work_queue.task_done()
      break

    # hash the wordlist and store it in result queue
    for result in _hash_wordlist(work_list,hashing_algorithm):
        result_list.append(result)

    result_queue.put(result_list)
    work_queue.task_done()

  core_log.debug("Hash-Core[%d] is stopped",core)
