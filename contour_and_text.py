
import cv2
import numpy as np
import pytesseract
import os
import re



class pan_verification:

    def __init__(self):
        pass


    def image_pre_process(self,img):    #,save_in_file

        pre = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Otsu threshold
        pre = cv2.threshold(pre, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # dilate the text to make it solid spot
        cpy = pre.copy()
        struct = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
        cpy = cv2.dilate(~cpy, struct, anchor=(-1, -1), iterations=1)
        pre = ~cpy

        # cv2.imwrite(save_in_file, pre)

        pre = 255-pre

        return pre

    def find_text_boxes(self,pre):
        contours, hier = cv2.findContours(pre,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   #cv2.RETR_LIST

        boxes = []
        for cnt in contours:
            if 9<cv2.contourArea(cnt)<75000:
                (x,y,w,h) = cv2.boundingRect(cnt)
                if h >= 5:
                    (x,y,w,h) = cv2.boundingRect(cnt)
                    box = (x,y,w,h)
                    boxes.append(box)
                    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

        return boxes



    # if __name__ == "__main__":

    def pan_text_detection(self,input_path,input_string):


        
        in_file = os.path.join("data", input_path)
     

        img = cv2.imread(os.path.join(in_file))
        # img = cv2.resize(img,(450,500))
        pre_processed = self.image_pre_process(img)      #, pre_file
        text_boxes = self.find_text_boxes(pre_processed)

        # Visualize the result
        vis = img.copy()

        text = ''
        
        for box in text_boxes:
            (x,y,w,h) = box
            image = cv2.rectangle(vis, (x,y), (x+w,y+h), (0,255,0), 1)


            cropped = vis[y:y+h, x:x+w]


            text1 = pytesseract.image_to_string(cropped)
            if text1 != " ":
                text += text1
                
            text2 = pytesseract.image_to_string(cropped,config=r'-l eng --oem 1 --psm 6 ')     # "--psm 6 digits"
            if text2 != " ":
                text += text2





        text = text.replace ('\x0c','').replace("\n",'')

        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~|‘'''

        for ele in text:
            if ele in punc:
                text = text.replace(ele, "")
        test_str = text.replace(" ","")


        if input_string in test_str.lower():
            return "yes"
        else:
            return "no"



# pan = pan_verification()
# input_path = '/home/phloxblog/adhar_land_deed_verification/sample/pan_sample_10.jpeg'

# # pre_img_path = '/home/phloxblog/adhar_land_deed_verification/pre_process_image/pan_sample_10.jpg'
# input_string= 'AHEP'

# status = pan.pan_text_detection(input_path,input_string)
# print("status >>>",status)
