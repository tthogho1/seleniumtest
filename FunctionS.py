from collections import Counter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

class Functions:

	functions = Counter()
	driver = None
	
	def __init__(self):
		print("****init****")
		#
		self.functions["send"]=self.func_send
		self.functions["radio"]=self.func_radio
		self.functions["check"]=self.func_check
		self.functions["select"]=self.func_select
		self.functions["inputval"]=self.func_inputval
		self.functions["checkid"]=self.func_checkid
		self.functions["idaction"]=self.func_idaction
		self.functions["sleep"]=self.func_sleep
		self.functions["cleartxt"]=self.func_clearText
		self.functions["print"]=self.func_print

	def set_driver(self,driver):
		self.driver = driver

	def execute_function(self,name):
		return self.functions[name]

	def func_clearText(self,name,text):
		try:
			# print(self.driver.page_source)
			target = self.driver.find_element_by_name(name)
			target.clear()
		except:
			print('{} is no such name or error'.format(name))

	def func_send(self,name,text):
		try:
			target = self.driver.find_element_by_name(name)
			target.send_keys(text)
		except:
			print('{} is no such name or error'.format(name))

	def func_checkid(self,name,value):
		try:
			element = self.driver.find_element(By.XPATH, "//input[@id='"+ name+ "']")
			element.click();
		except:
			print('{} is no such name or error'.format(name))

	def func_radio(self,name,value):
		try:
			print("$('input[name=" + name + "]:eq(" + value + ")').prop('checked', true)")
			self.driver.execute_script("$('input[name=" + name + "]:eq(" + value + ")').prop('checked', true)")
		except:
			print('{} {} is no such name or error'.format(name,value))

	def func_select(self,name,index):
		try:
			target = self.driver.find_element_by_name(name)
			select = Select(target)        
			select.select_by_index(index) 
		except:
			print('{} is no such name or error'.format(name))
        
	def func_check(self,name,dummy):
		try:
			target = self.driver.find_element_by_name(name)
			target.click()
		except:
			print('{} is no such name or error'.format(name))


	def func_inputval(self,name,value):
		try:
			self.driver.execute_script("$('#" + name + "').val('" + value + "')")
		except:
			print('{} is no such name or error'.format(name))
        
	def func_idaction(self,name,value):
		try:
			if value == "click":
				self.driver.find_element_by_id(name).click()
		except:
			print('{} is no such name or error'.format(name))

	def func_sleep(self,name,value):
		try:
			time.sleep(int(value))
		except:
			print('{} {} is no such name or error'.format(name,value))
	
		
	def func_print(self,name,value):
		try:
			print(value)
		except:
			print('error')