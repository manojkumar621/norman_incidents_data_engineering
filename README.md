Name: Manoj Kumar Galla

# Project Description
1. FEATURES
This python package takes a file that contains a list of urls as the input parameter and does the following actions - 
1 - Fetches the file data using urlib.requests library in python and downloads the file to a local directory.
2 - Parses the data in the downloaded file to extract the time, number, location, nature and ori code of the incidents.
3 - augments the data and prints out the tab seperated rows with each row containing - Day of the Week, Time of Day, Weather, 	Location Rank, Side of Town, Incident Rank, Nature, EMSSTAT
4 - Queries the data to print to standard out a pipe-seperated list of nature of the incident and the number of occurences of such incidents in the file in a descending order.

2. PROJECT STRUCTURE
The project is structured to have assignment2 file that is triggered initially, which then utilizes three different modules, namely - fetchincidents, extractdata and dbmanager to perform the above described actions. All these files are in the assignment0 folder which lies in the root directory, hence the modules are individually imported in the main.py file to make use of the functions in those modules.

The downloaded pdf file is saved into the 'resources/tmp/' directory path. This is later accessed to read the pages using python's pypdf package to extract the data. Also, in the resources folder, the database file is saved after it is created. Similarly, the pdf that is downloaded during testing is saved in the 'test_files' directory.

3. TESTING
This project can be classified into 3 parts - data download, data extraction, and saving the data. Three test files are designed to test each phase. test_download.py file tests the data download phase, test_extraction.py file tests all functions that are written to extract each information from the raw text, and the test_dbmanager.py file implemented to test all the functions related to creation and handling the data in the sqlite database.


# How to install
pipenv install

## How to run
pipenv run python3 assignment2.py --urls <file_name>


## How to test
pipenv run python3 -m pytest <test_file_path>

## Functions
#### assignment2.py \ 
process_urls() - This function takes each url and passes it to the corresponding functions to augment the data from the extracted values and then print the records on the output console.

augment_emsstat() - This function takes the incidents list as parameter, processes each incident string, and creates a new boolean value by following a set of instructions that has to do with the incident ORI value.

augment_incident_ranks() - This function takes the incidents list as parameter, processes each incident string, and new integer value that represents the ranks of the incident with ties preserved.

augment_location_ranks() - This function takes the incidents list as parameter, processes each incident string, and new integer value that represents the ranks of the location with ties preserved.

#### main.py \
main() - This functions takes url as the parameter. This function downloads data, extracts incidents information from the raw data, saves this information in a database as a table and prints the status of the incidents and returns nothing.

#### fetchincidents.py \
fetchincidents() - This function takes url as the parameter. This function takes the url and gets the binary data from the url, and returns the binary data.

#### extractdata.py \
extractdata() - This function takes a pdf file path as the parameter. This function extracts raw data from pdf file and processes the raw data to extract relavant information from the raw data, and returns the incidents data in the form of a list.

process_incidents_by_page() - This function takes a list of raw incidents text as the parameter and processes the whole incidents data page-by-page, then line-by-line in each page to extract relavant keys and values. Finally returns a list of tuples that contain parsed information.

extract_time() - This function takes the raw incident string as the parameter and parses the time when incident occurred from the raw incident string, and returns a string that contains time of occurrence.

extract_number() - This function takes the raw incident string as the parameter and parses the incident number from the raw incident string, and returns a string that contains incident number.

extract_address() - This function takes the raw incident string as the parameter and parses the location of the incident from the raw incident string. The function returns two values - address and last index. The last index is a crucial value that will be passed into the extract_nature_and_ori() function as the start_index to parse the nature of the incident from the raw incident string.

extract_nature_and_ori() - This function takes the raw incident string and a starting index as the parameter and parses the nature of the incident and the ori number from the raw incident string. The starting index is used to parse the nature of the incident from the raw incident string. Finally, the function returns two strings - nature of the incidents, and ori number.


## Bugs and Assumptions
1. ORI number is any of the following values - ['OK0140200', 'EMSSTAT', '14005', '14009']. If a pdf file contains ori numbers that are not in this list, they can't be extracted using this code.
2. Address is only a street address and in NOT in any other form (like ending with country, state, etc.). Global address cannot be captured using this code.
3. This code is limited to parsing only US street addresses.

