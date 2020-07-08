import sys
import os
import requests
import re
from bs4 import BeautifulSoup
from colorama import init, Fore
from collections import deque


# main
def main():
	init(autoreset=True)  # to reset the color of text back to normal.
	web_buffer = deque()  # for saving of buffer of previous visited sites.
	args = sys.argv  # saving the arguments.
	path = ""  # variable to save path.

	# if there is 2 arguments this block will create a new directory from the
	# second argument
	if len(args) == 2:
		# making a directory according to the argument given
		if not os.path.exists(args[1]):
			os.mkdir(args[1])
			path = args[1]+"/"
		else:
			# if the directory already exists update that to the user.
			path = args[1]+"/"
			print("Directory ", args[1],  " already exists")

	# infinite loop until the user types in exit
	# this loop prompts for URL
	while True:
		URL = input("URL   : ")  # prompts the user for a URL
		# checks if the user want to quit
		if URL == "exit":
			# qutting the program
			break
		# checks if the user want to go back
		elif URL == "back":
			if len(web_buffer) >= 2:
				web_buffer.pop()  # to pop the current webpage from the list
				prev = web_instance(web_buffer.pop(), args, path)  # instance with previous
				prev.open_saved()  # opening the previous URL   from saved files.
				continue  # skipping further code.
			else:
				continue  # if there is no back.
		#  creating a web instance with the URL
		webpage = web_instance(URL, args, path)
		if webpage.ifsaved():  # checks if the URL  is in saved ones
			webpage.open_saved()  # opens the saved files
		elif webpage.exists():  # checks if the domain exists
			webpage.open_web()  # opens the domain
			web_buffer.append(URL)  # opens the URL
		else:
			print("Error : Incorrect URL   ")  # prints the error in the URL


# web page class to store all the information about a webpage
class web_instance:
	def __init__(self, URL, args, path):
		self.URL = URL
		self.path = path  # path given through the 2nd argument
		self.args = args  # saving the argments.
		self.response = ""  # variable to save response of the URL
		self.webpage_string = []  # variable to store each line of the opened website
		# so that it can stored in the txt file
		URL = re.sub(r'(www|docs).', "", self.URL)  # removes www or docs from the UR
		# removes .com or similar things from the URL   string
		URL = re.sub(r'\.(net|com|org|info|edu|gov|uk|de|ca|jp|fr|au|us|ru|ch|it|nel|se|no|es|mil)', "", URL)
		self.new_path = self.path + URL + ".txt"  # creates a variable called new_path to store path to file

	def save_webpage(self):  # change this to save the text based webpage.
		"""Saves the webpage"""
		with open(self.new_path, "w", encoding="utf-8") as file_:  # creating/opening the txt file to save the webpage
			for lines in self.webpage_string:
				file_.writelines(lines)  # writing lines in the .txt file
				file_.writelines("\n")

	def exists(self):
		"""checks weather the URL   exists in web"""
		try:
			self.response = requests.get(f"https://{self.URL   }")  # trying the requests using request.get() method
		except requests.exceptions.ConnectionError:
			return False  # returns false if the attempt was failed
		else:
			if self.response.status_code == 200:
				return True  # returns true if the response was secured and the webpage exists.
			return False  # returns false if the response was secured but the webpage doesnt exist.

	def ifsaved(self):
		"""checks weather the URL   exist in the stored files"""
		if len(self.args) == 2:
			if os.path.isfile(self.path + self.URL + ".txt"):
				return True  # returns true if the URL  is saved files
		return False  # returns false if the URL    doesnt exist

	def open_web(self):
		"""opens the webpage from the web"""
		self.open_webpage()  # prints the webpage from the internet
		if len(self.args) == 2:
			self.save_webpage()  # saves the webpage if there is 2nd argument

	def open_saved(self):
		"""opens the webpage from the saved files"""
		with open(self.new_path, "r", encoding="utf-8") as back_webpage:  # opening from the directory
			for lines in back_webpage:
				print(lines.strip())

	def open_webpage(self):  # opening a html page formatted.
		webpage_soup = BeautifulSoup(self.response.content, 'html.parser')  # soup of the html page.
		listoftext = list(webpage_soup.find_all(["h1", "p", "a", "ol", "ul", "li", "title"]))  # making a list of all the said tags
		for elements in listoftext:  # going through each item in that list
			try:  # try except statement to avoid NavigableString error
				text = str(elements.find(text=True, recursive=False).strip())  # exracting the text only from the current tag not its children or descendents
				# Also converting the text into a string to remove the unwanted spaces
				if text not in ["", "»"]:  # removing unwanted space and characters
					if elements.name == "a":
						print(Fore.BLUE + text.strip())
						self.webpage_string.append(Fore.BLUE + text.strip())
					else:
						print(Fore.WHITE + text.strip())
						self.webpage_string.append(Fore.WHITE + text.strip())
			except AttributeError:
				pass


main()
