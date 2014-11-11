#!/usr/bin/env python3

from multiprocessing import Process, Queue, cpu_count,Pool,JoinableQueue
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

def start_rainbow_cores(wordlist,hashing_algorithm,output,use_database):
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
  num_cores = cpuCount()
  result_queue = JoinableQueue()
  work_queue = JoinableQueue(num_cores)

  for core in range(num_cores-1):

    cur_core = Process(target=core_run,args=(core,result_queue,work_queue,hashing_algorithm))
    cur_core.start()
    core_list.append(cur_core)

  out_core = Process(target=output_run,args=(result_queue,output,use_database))
  out_core.start()
  log.debug("Output core started")

  with open(wordlist,encoding="latin-1") as fwordlist:

    result_lines = list()
    for index,line in enumerate(fwordlist):
      result_lines.append(line)
      if (index % chunk_size) == 0:
        work_queue.put(result_lines)
        result_lines = list()

    if len(result_lines) > 0:
      work_queue.put(result_lines)

  work_queue.join()
  work_queue.close()

  result_queue.join()
  result_queue.close()
  log.debug("Result queue is finished")

  out_core.terminate()
  for core in core_list:
    core.terminate()

def output_run(result_queue,output,use_database):

  from .rainbow import save_rainbow_values

  core_log = logging.getLogger("leprechaun.core.output")

  with open(output+".txt","a") as out:
    core_log.debug("Output file opened %s",output+".txt")
    while True:
      result_list = result_queue.get()
      for result in result_list:
        out.write(result)
      result_queue.task_done()

def core_run(core,result_queue,work_queue,hashing_algorithm):

  from .rainbow import _hash_wordlist

  core_log = logging.getLogger("leprechaun.core")
  while True:
    work_list = work_queue.get()
    result_list = list()
    for result in _hash_wordlist(work_list,hashing_algorithm):
        result_list.append(result)
    result_queue.put(result_list)
    work_queue.task_done()
