import re
import string
import urlparse
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ArchitectFinderScraper(object):
    def __init__(self):
    	self.driver = webdriver.Firefox();
        self.driver.set_window_size(1120, 550);
        self.url = "https://ccmt.nic.in/ccmtregistration/report/PreviousMaxMin.aspx?boardid=105012021";

    def scrape(self):
	    self.driver.get(self.url)
	    self.driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlYear').style.display = 'block';")
	    
	   
	    
	    output_rows = [] 
	    is_table_header_added = False  
	    wait = WebDriverWait(self.driver, 20)
	    # Select year selection dropdown
	    # year_select = Select(wait.until(lambda driver: driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlYear')))
	    year_select = Select(self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlYear'));
	    # year_select = wait.until(EC.element_to_be_clickable((By.XPATH , "//select[@id='ctl00_ContentPlaceHolder1_ddlYear']")));
	    # year_select = Select(self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlYear'));
	    year_option_indexes = range(1, len(year_select.options))
	    time.sleep(5);
	    # Iterate through each year
	    for index in year_option_indexes:
	        year_select.select_by_index(index)
	        # Select round selection dropdown
	        # round_select = Select(wait.until(lambda driver: driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlRoundno')))
	        self.driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlRoundno').style.display = 'block';")
	        round_select = Select(self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlRoundno'));
	        # round_select = wait.until(EC.element_to_be_clickable((By.XPATH , "//select[@id='ctl00_ContentPlaceHolder1_ddlRoundno']")));
	        round_option_indexes = range(1, len(round_select.options))
	        # Iterate through each round
	        # time.sleep(5);
	        for index in round_option_indexes:
		        round_select.select_by_index(index)
		        # Select institution selection dropdown
		        self.driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlInstCd').style.display = 'block';")
		        institute_select = Select(self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlInstCd'));
		        institute_option_indexes = range(2, len(institute_select.options))
		        # Iterate through each institution
		        # time.sleep(5);
		        for index in institute_option_indexes:
		        	institute_select.select_by_index(index)
		        	# Select branch selection dropdown
		        	self.driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_ddlBrCd').style.display = 'block';")
		        	branch_select = Select(self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlBrCd'));
		        	branch_option_indexes = range(1, len(branch_select.options))
		        	# Iterate through each branch
		        	# time.sleep(5);
		        	for index in branch_option_indexes:
		        		branch_select.select_by_index(index)
		        		self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSubmit').click()
		        		# Wait for results to finish loading
		        		self.driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_pnlORCR').style.display = 'block';")
		        		# wait.until(lambda driver: driver.find_element_by_id('ctl00_ContentPlaceHolder1_pnlORCR').is_displayed() == False)
		        		soup = BeautifulSoup(self.driver.page_source, "html.parser");
		        		table = soup.find("table")
		        		for table_row in table.findAll('tr'):
		        			if is_table_header_added == False:
		        				columns = table_row.findAll('th')
		        				is_table_header_added = True
		        			else:
		        				columns = table_row.findAll('td')
							
							output_row = [];
							for column in columns:
								output_row.append(column.text)
							output_rows.append(output_row)
							print output_rows.len()
		with open('output.csv', 'wb') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(output_rows)

if __name__ == '__main__':
    scraper = ArchitectFinderScraper()
    scraper.scrape()


