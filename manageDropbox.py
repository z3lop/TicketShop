import dropbox
import pandas as pd
import pathlib
import os
import time

import loginData

def get_dropbox_client():
  access_token = loginData.read_from_env('ACCESS_TOKEN')
  expire = float(loginData.read_from_env('TOKEN_TIME')) + float(loginData.read_from_env("EXPIRE_TIME"))

  if time.time() > expire:
    loginData.get_access_code()

  return dropbox.Dropbox(access_token)

def dropbox_list_files(path = '', files_list = None):
  """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
  """
  dbx = get_dropbox_client()
  response = dbx.files_list_folder(path)
  if not files_list:
    files_list = []
  
  for entry in response.entries:
    try:
      df, files_list = dropbox_list_files(dbx, entry.path_display, files_list)
    except:
      metadata = {
        'name' : entry.name,
        'path_display' : entry.path_display,
        'server_modified': entry.server_modified
      }
      files_list.append(metadata)
      print(f"{entry.name}: {entry.path_display}")
  df = pd.DataFrame.from_records(files_list)
  return df, files_list

def dropbox_upload_file():
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns:
        meta: The Dropbox file metadata.
    """
    local_path = os.path.dirname(__file__)
    local_file = "persons.xlsx"
    dropbox_file_path = '/persons.xlsx'
    

    try:
        dbx = get_dropbox_client()

        local_file_path = pathlib.Path(local_path) / local_file
        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except IndexError:
       pass
    # except Exception as e:
    #     print('Error uploading file to Dropbox: ' + str(e))

def dropbox_download_file():
  local_path = os.path.dirname(__file__)
  filename = "persons.xlsx"
  dropbox_file_path = '/persons.xlsx'

  try:
    dbx = get_dropbox_client()

    local_file_path = pathlib.Path(local_path) / filename
    dbx.files_download_to_file(local_file_path, dropbox_file_path)
    print('download complete')
  except Exception as e:
    print('Error downloading file from Dropbox:' + str(e))