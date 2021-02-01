"""Helper functions module"""
import pandas
import json
import requests 
import urllib
import io



"""GitHub login credentials (Mia's)"""
user = 'mbendy'
pao = 'ce9aec01691d2a8efde6a73dc3a6a5e337960199'


def get_json_file(url):
  """
  Parameter: link to GitHub with JSON file
  Return: Dictionary with JSON data
  Author: Connor
  """



  github_session = requests.Session()
  github_session.auth = (user, pao)

  file_download = github_session.get(url).content

  data_dictionary = json.loads(file_download)

  return data_dictionary



def get_csv_file(url):
  """
  Parameter: link to GitHub with CSV file
  Return: Dictionary with JSON data
  Author: Connor
  """

  

  github_session = requests.Session()
  github_session.auth = (user, pao)

  file_download = github_session.get(url).content
  dataframe = pandas.read_csv(io.StringIO(file_download.decode('utf-8')), error_bad_lines=False)


  return dataframe
