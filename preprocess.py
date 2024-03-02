import cv2


#for image preprocessing (from internet) (resize / invert / gray / threshold)
def resize(image , flag):
    if flag == "id":
        bigger = cv2.resize(image, (650, 800))
        return bigger
    elif flag == 1:
        stretch_near = cv2.resize(image, (780, 540), 
                    interpolation = cv2.INTER_LINEAR)
        return stretch_near
    elif flag == "firstname":
        forname = cv2.resize(image, (600, 200))
        return forname
    elif flag == "secondname":
         forname = cv2.resize(image, (500, 200))
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
