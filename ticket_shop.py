import pandas as pd
import qrcode as qr
from time import localtime, strftime
from random import randint
import os

import pdf

class DataFrameOperations(object):
	def __init__(self):
		filename = r'persons.xlsx'
		self.mother_path = os.path.dirname(__file__)
		self.file_path = os.path.join(self.mother_path, filename)
		self.dataframe = self.initialize_main_df()	
		self.id = 0

	def initialize_main_df(self):
		'''
		### Parameters
		None
  
		### RETURN
		-initizied main data frame
		'''
		try:
			main_df = pd.read_excel(self.file_path)
			main_df.drop(columns=main_df.columns[0], axis=1, inplace=True)
		except:
			main_df = pd.DataFrame([], columns=['Datum','ID', 'Vorname', 'Nachname', 'E-Mail',
                                        'Ticketkäufe', 'Essen (1 / 0)', '[Vegetarisch / Vegan]'])
  	
		return main_df
  
	def add_to_df(self,pren: str, name: str, mail: str, num_ticket: int, eat: bool, veg = None):
		'''
		This functions takes all parameters for a new person and add it to the list

		### Parameters 
		2. pren: str
			- Prename of person
		3. name : str
			- surname of person
		4. mail : str 
			- used mail adress
		5. num_ticket : int
			- how many tickets were ordered
		6. eat: bool 
			- does the person eat at the party
		7. veg: None if eat false
						Else: list of how many dishes [vegetarian, vegan]

		### TO-DO
		- Check if id is already in table
		
		'''
		id = randint(10e12, 9*10e12)
		df = self.dataframe
		while True:
			if id in df['ID'].to_list():
				id = randint(10e12, 9*10e12)
			else:
				break
		self.id = id
		
		time = strftime("%d.%m.%Y %H:%M:%S", localtime())

		tmp_list = [time, id, pren, name, mail, num_ticket, eat, veg]

		if (pren == '') or (name == '') or (mail == '') or (num_ticket == 0):
			return False

		df.loc[len(df)] = tmp_list

		return True
	
	def write_to_csv(self):
		df = self.dataframe
		df.to_excel(self.file_path)

	def make_and_send_qr_code(self):
		df = self.dataframe
		filename = 'my_qr_code.png'
		qr_code = qr.make(df.iloc[-1]['ID'])
		qr_code.save(os.path.join(self.mother_path, filename))

		name = df.iloc[-1]['Nachname']
		prename = df.iloc[-1]['Vorname']
		how_many = df.iloc[-1]['Ticketkäufe']
		date = df.iloc[-1]['Datum']
		eat_bool = df.iloc[-1]['Essen (1 / 0)']

		
		pdf.make_pdf_ticket(eat_bool, how_many, prename, name)
		os.remove(filename)
