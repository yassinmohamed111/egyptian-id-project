import cv2 
import pytesseract 
from PIL import Image
import numpy as np
from ultralytics import YOLO
import os
import time
import pandas as pd 



df = pd.read_csv("ids.csv")



#put here the file path of the id you want to read
source = r'C:\Users\yassi\Desktop\egyptian id project\117113533_669803296952913_6945067801334766223_n.jpg'

#function of yolov8 model to detect and crop (fname ,sname ,location  , national id , pic   , manf. id )
def predict():
    model = YOLO(r'c:\Users\yassi\Downloads\best (13).pt')
    results = model(source, save=True, conf=0.6, imgsz=640 ,show=False , save_crop = True)

#run the prediction
predict()

#get the current prediction
def current_folder():
    directory = r'C:\Users\yassi\Desktop\egyptian id project\runs\detect'
    directories = next(os.walk(directory))[1]
    num_folders = len(directories)
    return num_folders

curr = current_folder()

#getting national id image from the folder
def get_id_image():
    file_name = os.path.basename(source)
    img_file = rf'runs\detect\predict{curr}\crops\national_id'+ '\\'  + file_name
    image = cv2.imread(img_file)
    return image

#getting manf. id from the folder
def get_manf_image():
    file_name = os.path.basename(source)
    img_file = rf'runs\detect\predict{curr}\crops\manfucturing_id'+ '\\'  + file_name
    image = cv2.imread(img_file)
    return image

#runs 
id_image = get_id_image()
manf_image = get_manf_image()



#for image preprocessing (from internet) (resize / invert / gray / threshold)
def resize(image , flag):
    if flag == 0:
        bigger = cv2.resize(image, (1050, 1610))
        return bigger
    elif flag == 1:
        stretch_near = cv2.resize(image, (780, 540), 
                    interpolation = cv2.INTER_LINEAR)
        return stretch_near
    else:
        return image

def invert(image):
    return  cv2.bitwise_not(image)

def gray(image):
    return cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

def threshold(image):
    im_bw, th = cv2.threshold(image , 160 , 195, cv2.THRESH_BINARY)
    return th 


#running the preprocessing based on flag - > manf. id takes -1 , national_id takes 0
def processing(image, flag):
    resized_image = resize(image , flag)
    inverted_image = invert(resized_image)
    gray_image = gray(inverted_image)
    threshold_image = threshold(gray_image)
    return threshold_image

#runs
threshold_id_image = processing(id_image , 0)
threshold_manf_image = processing(manf_image , -1)



#get national id number using ocr tesseract
def get_national_id():
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   res = pytesseract.image_to_string(threshold_id_image, lang="ara_number_id").split()
   if res != []:
    for i in res:
        if len(i) > 13 and len(i) < 15:
            print(i)

    print(res)
    return res

#get manf. id number using ocr tesseract
def get_manf_id():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    res = pytesseract.image_to_string(threshold_manf_image)
    print(res)
    return res


#save thresholed pic    
def save_threshold():
    cv2.imwrite('temp/output_id.jpg' , threshold_id_image)
    cv2.imwrite('temp/output_manf.jpg' , threshold_manf_image)


#save thresholds in a dir 
save_threshold()
# run of the detection
national_id = get_national_id()
manf_id = get_manf_id()

df['national_id'] = national_id[0]
df['manfucture_id'] = manf_id 
df.to_csv('ids.csv' , index=False)






