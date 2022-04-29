""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-03-11  J.Dalby   Initial creation
  2022-04-27  J.Daler   Adding my personal API key and fininshing the todos' at the beginning.
  2022-04-28  J.Daler   Worked on def download_apod_image.
  2022-04-28  J.Daler   Joining the pieces of the code together by completing the rest of the To-dos.

"""
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from os import path
from os.path import exists
import os.path
from pip._vendor import requests
import hashlib
import shutil
from pprint import pprint
import sqlite3

def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dict = get_apod_info(apod_date)
    
    # Download today's APOD
    image_url = download_apod_image(apod_info_dict)
    image_msg = download_apod_image(image_url)
    sha256_ = hashlib.sha256(image_url.encode())
    image_sha256 = str((sha256_.digest())) 
    image_size = os.path.getsize(image_path)
    image_path = get_image_path(image_url, image_dir_path)

    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    url =image_url #image url
    filename= url.split("/")[-1] #get the picture's name
    
    resides =  dir_path 
    
    full_path= os.path.join(resides,filename)
    print(full_path)
    return resides

def get_apod_info(date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    
    #return {"todo" : "TODO"}
    key = 'TNm06SRKykzfokhyJrt5JucyZaaPFf5bzBgKYi2Y'
    nasa_api = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + key)
    
    params= (nasa_api + key +"&date=" + str(date))    
    print(params)
    print("Getting  APOD info......")
    
    response = requests.get(params)

    if response.status_code == 200:
        
        
        print('Response:',response.status_code, '🎉🎉🎉', '\n')
        print("Success Date obtained")
        info =response.json()
        info_dict= dict(info)
        return info_dict
        
    else:
        print('Uh Oh, Unsucessful',response.status_code)
        return None

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD
    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """    
    print("the Url is " + image_url,".")
    print("Full path is " + image_path,".")
    print("The Image size is ", image_size,"KB.")
    print("The Sha-256 is ", image_sha256)
    
    return None

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """
    #return "TODO"
    image =(image_url['url'])
    image_data = requests.get(image) 
    
    if image_data.status_code == 200:
        print('Response:',image_data.status_code, '🎉🎉🎉', '\n')
        print("Success connection")
        return image
                   
    else:
        print('failed to download photo',image_data.status_code)
        return None


def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    url =image_msg #url of the photo that is going to be saved
    req=requests.get(url,stream = True) 
    if req.status_code == 200:
        print('Response:',req.status_code, '🎉🎉🎉', '\n')
        print("Successfully saved")

    else:
        print('failed to download photo',req.status_code)

    filename = url.split("/")[-1] 
    req.raw.decode_content = True 
    path = image_path 
    complete = os.path.join(path,filename)
    with open(complete,'wb') as f: 
        shutil.copyfileobj(req.raw, f)



    return None

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """
    path = db_path
    
    
    f_exist= exists(path)
    if f_exist == False:
        db_path =sqlite3.connect(path) 
        c = db_path.cursor() 
        c.execute("""CREATE TABLE 'NASA Pictures'(
            image_path text,
            image_url text,
            image_size integer,
            image_sha256 text
)
                """)
        
        db_path.commit() 
        
        db_path.close()
        
    return None

def add_image_to_db(db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    connect =sqlite3.connect(db_path) 
    c =connect.cursor()
    c.execute("INSERT INTO 'NASA Pictures'( image_path, image_url, image_size, image_sha256) VALUES (?,?,?,?)",(db_path, image_path, image_size, image_sha256))
    connect.commit()
    connect.close()
    return None

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 
    connect=sqlite3.connect(db_path)
    c =connect.cursor()
    c.execute("SELECT image_sha256 FROM 'NASA Pictures'")
    all_sh =c.fetchall()
    c.close()
    if (image_sha256,)in all_sh:
        return True
    else:
        return False
def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    return #TODO

main()