# Import libraries
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
from datetime import datetime
from utils import *
from pattern import * 
from glob import glob
import pandas as pd
import mysql.connector

def handler_OCR(file_name:str)->list:

    # Path of the pdf
    PDF_file = file_name

    '''
    Part #1 : Converting PDF to images
    '''

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')

    # Counter to store images of each page of PDF to image
    image_counter = 1

    # Iterate through all the pages stored above
    for page in pages:

        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = "page_"+str(image_counter)+".jpg"
        
        # Save the image of the page in system
        page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

    '''
    Part #2 - Recognizing text from the images using OCR
    '''
    # Variable to get count of total number of pages
    filelimit = image_counter-1

    # Creating a text file to write the output
    outfile = "out_text.txt"

    # Open the file in append mode so that
    # All contents of all images are added to the same file
    f = open(outfile, "wb")
    content = []
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):

        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = "page_"+str(i)+".jpg"
            
        # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(filename),lang = 'vie'))))
        content.append(text)
        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')	

        # Finally, write the processed text to the file.
        f.write(text.encode('utf-8'))

    # Close the file after writing all the text.
    f.close()   
    return content

def extract_data_from_OCR(content:list)->list:
    try:
        new_content = ' '.join(content)
        if get_MSDN(pattern_MSDN,new_content):
            list_MSDN = get_MSDN(pattern_MSDN,new_content)
        else:
             list_MSDN = ["N/a"]
        if get_name_company(pattern_company,new_content):
            list_name_company = get_name_company(pattern_company,new_content)
        else:
            list_name_company = ["N/a"]
        if get_NTL(pattern_NTL,new_content):
            list_NTL = get_NTL(pattern_NTL,new_content)
        else:
            list_NTL = ['N/a']
        if get_address(pattern_address,new_content):
            list_address = get_address(pattern_address,new_content)
        else:
            list_address = ['N/a']
        if get_phone(pattern_phone,new_content):
            list_phone =get_phone(pattern_phone,new_content)
        else:
            list_phone = ["N/a"]
        if get_name_director(pattern_name_director,new_content):
            list_name_director = get_name_director(pattern_name_director,new_content)
        else:
            list_name_director = ["N/a"]
        if get_city(pattern_province,''.join(list_address)):
            list_city = get_city(pattern_province,''.join(list_address))
        else:
            list_city = ["N/a"]
        if "Thành phố Thủ Đức" in ' '.join(list_address):
            list_district = ["Thành phố Thủ Đức"]
        elif get_district(pattern_district,''.join(list_address)):
            list_district = get_district(pattern_district,''.join(list_address))
        else:
            list_district = ["N/a"]
    except Exception as e:
        print(f"Error in extract data:{e}")
    return list_MSDN,list_name_company,list_NTL,list_address,list_phone,list_name_director,list_city,list_district

def create_csv(file_name:str,city:str,date:str):
    list_MSDN,list_name_company,list_NTL,list_address,list_phone,list_name_director,list_city,list_district = extract_data_from_OCR(handler_OCR(file_name))
    data_dict = {
    "BussinessId" : list_MSDN,
    'CompanyName' : list_name_company,
    'FoundedDate' : list_NTL,
    "Address"     : list_address,
    "City"        : list_city,
    "District"    : list_district,
    'DirectorName': list_name_director,
    'Phone'       : list_phone
    }
    df = pd.DataFrame(data_dict)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_file = file_name.split('\\')[-1].replace('.pdf','_')
    file = f'C:\\Users\\ADMIN\\Desktop\\OCR_Project\\Output\\{city}\\{date}\\'+f'{city}'+'_'+str(new_file)+ str(stamp)+'.csv'
    df.to_csv(file)

def create_list_csv(address:str,city:str,date:str):
    list_file = glob(address+"\\*.pdf")
    for file in list_file:
        create_csv(file,city = city,date=date)

mydb = mysql.connector.connect(
    host = "meowhouse.cn5wfkua0ike.ap-southeast-2.rds.amazonaws.com",
    user = "admin",
    password = "Meowhouse123.",
    database = "meowhouse"
)

def insert_db(file:str):
    val = []
    try:
        cursor = mydb.cursor()
        df = pd.read_csv(file)
        query = """INSERT INTO bussiness_management(BussinessId,CompanyName,FoundedDate,Address,City,District,DirectorName,Phone,Source)
            VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s,%s
            )"""
        for index,row in df.iterrows():
            BussinessId = str(row['BussinessId'])
            CompanyName = str(row['CompanyName'])
            FoundedDate = str(row['FoundedDate'])
            Address = str(row['Address'])
            City = str(row['City'])
            District = str(row['District'])
            DirectorName = str(row['DirectorName'])
            if "." in str(row['Phone']):
                Phone = str(row['Phone'])
            else:
                Phone = "0"+str(row['Phone'])
            Source = file.split('\\')[-1]
            val.append(BussinessId)
            val.append(CompanyName)
            val.append(FoundedDate)
            val.append(Address)
            val.append(City)
            val.append(District)
            val.append(DirectorName)
            val.append(Phone)
            val.append(Source)
        val = list(map(lambda x : str(x).replace("N/a","NULL") if("N/a" in x) else x ,val))
        cursor.execute(query,tuple(val))
        mydb.commit()
        print(val[-1],cursor.rowcount, "was inserted.")
    except Exception as e:
        print(f"Error in insert data to db:{e}")
    return val

def insert_many_files_to_db(address):
    list_file = glob(address+"\\*.csv")
    for file in list_file:
        insert_db(file)
    
