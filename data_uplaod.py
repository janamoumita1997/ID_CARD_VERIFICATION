
from tika import parser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pdf2image
import pytesseract
import numpy as np
import cv2
from pytesseract import Output

import json
from tika import parser 

# path="/home/phloxblog/adhar_land_deed_verification/land_deeds_sample.pdf"

# nltk.download('stopwords')



class content_extractor:
	def __init__(self,path):
		self.path=path


	def text_filter(self,text):
		try:
			swa=[]
			for i in text:
				if i != '':
					if i !=' ':
						swa.append(i.strip())
			return swa
		except Exception as e:
			print(e)


	def content(self):
		try:
			files=pdf2image.convert_from_path(self.path)

			text=[]
			for file in files:
				#text = pytesseract.image_to_string(file)
				#print(text)
				image = np.array(file)
				rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
				text=text+results['text']
			#print(f"text   ",text)

			swa_1= self.text_filter(text)
			main_content=" ".join(str(x) for x in swa_1)
			#print(f"main_content  : {main_content}" )

			filtered_words = [word for word in swa_1 if word not in stopwords.words('english')]
			#print(filtered_words)
			stop_content= " ".join(str(x) for x in filtered_words)

			# #print(f"stop_content  : {stop_content}")

			return stop_content
		except Exception as e:
			print(e)

# content_pdf=content_extractor(path)
# stop_content=content_pdf.content()
# print("stop_content>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",stop_content)



class ExtractFile:
    def __init__(self, file_path):
        self.file_path = file_path 

    
    def extractPDF(self):
        try:
            file = self.file_path
            # FileName = self.fileName
            parsed_pdf = parser.from_file(file)
            metadata=parsed_pdf.get("metadata")

            stop_content=content_extractor(file).content()

            # print("stop_content >>>>>>>>>>>>>>>>>>>>>>>> ",stop_content)

            # result={"filename": FileName,"content":stop_content,"metadata":json.dumps(metadata)} 

            punc = '''!“()-[]{};:'"\,<>./?@#$%^&*_~|‘'''

            for ele in stop_content:
                if ele in punc:
                    stop_content = stop_content.replace(ele, "")
            content_str = stop_content.replace(" ","").lower()

            # print("stop_content >>>>>>>>>>>>>>>>>>>>>>>> ",content_str)

            return content_str

        except Exception as e:
            print(e)
            return "extraction can not possible"


    def verifictaion_status(self,search_key_list):

    	try:
    		search_string = self.extractPDF()

    		match_element_lst = []

    		for i in search_key_list:
    			search_key = i.lower().replace(' ','').strip()
    			# print("search_key >>",search_key)
    			if search_key in search_string:
    				match_element_lst.append(i)

    		if len(match_element_lst) == len(search_key_list):
    			result = 1
    			# print("all elements are match")
    		elif len(match_element_lst) >= 1:
    			result = 2
    			# print(f" match element is {match_element_lst} and not match {list(set(search_key_list)-set(match_element_lst))}")
    		else:
    			return "search list not match"

    		

    		if len(match_element_lst) >= 1:

    			return 1


    	except Exception as e:
    		print (e)




# # fileName = "Treasury_Treasury_Analyst_Spec.pdf"
# fileDirectory = "/home/phloxblog/adhar_land_deed_verification/Treasury_Treasury_Analyst_Spec.pdf"

# data = ExtractFile(fileDirectory)
# # print(" >>>>>> ",data)
# input_string = ['mobile money marketplace','Key responsibilities','Skills','brail']
# print(data.verifictaion_status(input_string))






