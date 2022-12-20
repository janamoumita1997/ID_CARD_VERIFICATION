from contour_and_text import *
from invoice_digitisation import *
from data_uplaod import *
import sys
import json
import ast


sample_name = sys.argv[1]


input_string = sys.argv[2]


input_status = sys.argv[3]


def document_verification(sample_name,input_string,input_status):

	
	


	input_path = sample_name

	if int(input_status) == 1:

		try:

			if len(input_string.strip()) == 0:
				input_string = ' random initialisation '
			
			adhar = adhar_card_verifictaion()
			result = adhar.text_extraction(input_path)

			input_string = input_string.lower().replace(' ','').strip()

			if input_string in result.lower():
				return 1

			else:
				pan = pan_verification()
				result = pan.pan_text_detection(input_path,input_string)

				if result == 'yes':
					return 1
				else:
					return 0

		except Exception as e:
			return "id verification failed"



	else:

		try:

			input_string= ast.literal_eval(input_string)

			data = ExtractFile(input_path)

			result = data.verifictaion_status(input_string)

			# print("result >>> ",result)

			return result

		except Exception as e:

			return e






print(document_verification(sample_name,input_string,input_status))




