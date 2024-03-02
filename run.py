import shutil
import cv2 
import pytesseract 
from PIL import Image
import numpy as np
from ultralytics import YOLO
import os
import time
import pandas as pd 
import convert_numbers 
import arabic_reshaper
from bidi.algorithm import get_display
from preprocess import processing
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import sys

#delete folder preditct 2 to stop saving past detections
path_to_delete = r'C:\\Users\\yassi\\Desktop\\egyptian id project\\runs\\detect\\predict2'
if os.path.exists(path_to_delete):
    shutil.rmtree(path_to_delete)
    print("Folder deleted successfully")
else:
    print("Folder does not exist")

source = ""
def getsource():
    source = input("please enter path of the Id picture : ")
    return source


source = getsource()


#function of yolov8 model to detect and crop (fname ,sname ,location  , national id , pic   , manf. id )
def predict_id():
    model = YOLO(r'c:\Users\yassi\Downloads\best (13).pt')
    results = model(source, save=True, conf=0.6, imgsz=640 ,show=False , save_crop = True)

def return_source():
    return source 

predict_id()

image_names = ['firstname' , "national_id" , "second name" , "manfucturing_id"]



def get_images():
    file_name = os.path.basename(source)
    images = []
    for name in image_names:
        img_file = rf'runs\detect\predict2\crops\{name}'+ '\\'  + file_name
        image = cv2.imread(img_file)
        images.append(image)
    return images


#getting images
try:
    images = get_images()
    firstname_image = images[0]
    id_image = images[1]
    secondname_image = images[2]
    manf_image = images[3]
except FileNotFoundError:
    print('*************************************')
    print("not found file")
    print("Insert new image please and try again!!")
    print("Notice: the clearity and resolution should be clear and perfectly skewed and the image not to far and not too close")
    print('*************************************')
    sys.exit()

#preprocssing images
threshold_id_image = processing(id_image , "id")
threshold_manf_image = processing(manf_image , -1)
threshold_firstname_image = processing(firstname_image, "firstname")
threshold_secondname_image = processing(secondname_image,"seondname")



def get_first_name():
     res = pytesseract.image_to_string(threshold_firstname_image , lang='ara')
     return res

def get_second_name():
     res = pytesseract.image_to_string(threshold_secondname_image , lang='ara')
     return res


def get_national_id():
   res = pytesseract.image_to_string(threshold_id_image, lang="ara_number_id").split()
   if res != []:
    return res[0]


def get_manf_id():
    res = pytesseract.image_to_string(threshold_manf_image)
    return res


#save thresholed pic    
def save_threshold():
    cv2.imwrite('temp/output_id.jpg' , threshold_id_image)
    cv2.imwrite('temp/output_name.jpg' , threshold_firstname_image)
    cv2.imwrite('temp/output_manf.jpg' , threshold_manf_image)
    cv2.imwrite('temp/output_second_name.jpg' , threshold_secondname_image)

save_threshold()


#get national_id , fname , lname , manf_id
national_id = get_national_id()
manf_id = get_manf_id()
firstname = get_first_name()
secondname = get_second_name()

print(national_id)
temp_fname = arabic_reshaper.reshape(firstname)
temp_sname = arabic_reshaper.reshape(secondname)
arabic_fname = get_display(temp_fname)
arabic_sname = get_display(temp_sname)

#convernt national id to english 
try:
    english_id = convert_numbers.arabic_to_english(national_id)
except TypeError:
    print('*************************************')
    print("no id")
    print("Insert new image please and try again!!")
    print("Notice: the clearity and resolution should be clear and perfectly skewed and the image not to far and not too close")
    print('*************************************')
    sys.exit()


save_threshold()

number_mapping = {
    '01': "cairo",
    '02': "alexandria",
    '03': "portsaid",
    '04': "suez",
    '11': "damieta",
    '12': "dakahlya",
    '13': "elsharkya",
    '14': "elkalyobia",
    '15': "kafr elsheikh",
    '16': "elgharbia",
    '17': 'elmenofya',
    '18': "elbehira",
    '19': "elesmaalyaa",
    '21': "giza",
    '22': "beni suief",
    '23': "fayium",
    '24': "elmenya",
    '25': "assiut",
    '26': "sohag",
    '27': "qena",
    '28': "aswan",
    '29': "luxor",
    '31': "red sea governate",
    '32': "wadi el-gadid",
    '33': "matrouh",
    '34': "north sinai",
    '35': "south sinai",
    '88': "outside the country"
}

df = pd.read_csv("ids.csv")
try:
    century = english_id[0]
    year_born = english_id[1] + english_id[2]
    month = english_id[3]+english_id[4]
    day = english_id[5]+english_id[6]
    temp_born = english_id[7]+english_id[8]
    place_of_birth = number_mapping[temp_born]
    your_count_of_day  = english_id[9]+english_id[10]+english_id[11]
    gender = english_id[12]
    verify_id = english_id[13]
except IndexError:
    print('*************************************')
    print('no full id')
    print("Insert new image please and try again!!")
    print("Notice: the clearity and resolution should be clear and perfectly skewed and the image not to far and not too close")
    print('*************************************')
    sys.exit()





def print_info():
    print("your national id is :" , national_id , " || " , english_id)
    print("your manfucture id is :" , manf_id)
    print("first name : " , arabic_fname)
    print("lastname : " , arabic_sname)

    if century == "3" :
        print(f"born in : {day}-{month}-20{year_born} ")
    elif century == "2":
        print(f"born in : {day}-{month}-19{year_born} ")

    
    print("your place of birth is : " , place_of_birth)
    if int(gender) % 3 == 0 and int(gender) != 6:
        print("gender : Male")
    elif int(gender) %2 ==0:
        print("gender : Female")
    
    print("your count of the births in this day is : " , your_count_of_day)
    print("verify_id :" , verify_id)


print_info()


