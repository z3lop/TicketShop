from requests import post
from webbrowser import open as web_open
from os import path
from ast import literal_eval
from time import time
import sys

def write_to_env(variable: str, value: str):
  if getattr(sys, 'frozen', False):
    env_file_path = path.dirname(sys.executable)
  elif __file__:
    env_file_path = path.dirname(__file__)

  file_path = path.join(env_file_path, '.env')
  if not path.isfile(file_path):
    with open(file_path, 'w') as f:
      pass
  
  with open(file_path, 'r') as f:
    index = -1
    bool = False
    for ln in f:
      index += 1
      if ln.startswith(variable):
        bool = True
        break
  
  if bool == True:
    with open(file_path, 'r') as f:
      data = f.readlines()
    data[index] = f"{variable}={value}" + "\n"
    with open(file_path, 'w') as f:
      f.writelines(data)
  else:
    with open(file_path, 'a') as f:
      f.writelines(f"{variable}={value}" + "\n")

def read_from_env(variable: str):
  if getattr(sys, 'frozen', False):
    env_file_path = path.dirname(sys.executable)
  elif __file__:
    env_file_path = path.dirname(__file__)
  with open(path.join(env_file_path, '.env'), 'r') as f:
    for line in f:
      if line.startswith('#') or not line.strip():
        continue
      key, value = line.strip("\n").split('=', 1)
      if key == variable:
        return value
    raise ValueError('Variable not in .env file')

def get_access_code():
  APP_KEY = read_from_env('APP_KEY')
  url = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&' \
    f'response_type=code&token_access_type=offline'
  
  web_open(url)

def get_login_data():
  APP_SECRET = read_from_env('APP_SECRET')
  APP_KEY = read_from_env('APP_KEY')
  ACCESS_CODE_GENERATED = read_from_env('ACCESS_CODE_GENERATED')
  
  data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'
  
  response = post('https://api.dropboxapi.com/oauth2/token',
                           data=data,
                           auth=(APP_KEY, APP_SECRET))
  
  response = literal_eval(response.text)
  write_to_env("ACCESS_TOKEN", response.get("access_token"))
  write_to_env('EXPIRE_TIME', response.get('expires_in'))
  write_to_env('TOKEN_TIME', str(time()))
