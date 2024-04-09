Name: Manoj Kumar Galla

# Project Description
1. FEATURES
This python package takes a file url (incidents file from the norman police department website) as the input and does the following actions - 
1 - Fetches the file data using urlib.requests library in python and downloads the file to a local directory.
2 - Parses the data in the downloaded file to extract the time, number, location, nature and ori code of the incidents.
3 - Creates an sqlite database, makes a connection to the database and puts the data into it as a table.
4 - Queries the table to print to standard out a pipe-seperated list of nature of the incident and the number of occurences of such incidents in the file in a descending order.

2. PROJECT STRUCTURE
The project is structured to have a main file that is triggered initially, which then utilizes three different modules, namely - fetchincidents, extractdata and dbmanager to perform the above described actions. All these files are in the assignment0 folder which lies in the root directory, hence the modules are individually imported in the main.py file to make use of the functions in those modules.

The downloaded pdf file is saved into the 'resources/tmp/' directory path. This is later accessed to read the pages using python's pypdf package to extract the data. Also, in the resources folder, the database file is saved after it is created. Similarly, the pdf that is downloaded during testing is saved in the 'test_files' directory.

3. TESTING
This project can be classified into 3 parts - data download, data extraction, and saving the data. Three test files are designed to test each phase. test_download.py file tests the data download phase, test_extraction.py file tests all functions that are written to extract each information from the raw text, and the test_dbmanager.py file implemented to test all the functions related to creation and handling the data in the sqlite database.


# How to install
pipenv install

## How to run
pipenv run python3 assignment0/main.py --incidents <url>

[![Watch the video](https://img.youtube.com/vi/775e0nLt4gs/0.jpg)](https://www.youtube.com/watch?v=775e0nLt4gs)

## How to test
pipenv run python3 -m pytest <test_file>

## Functions
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

#### dbmanager.py \
createdb() - This function takes the database file path as the string parameter. This function creates an sqlite3 database (if not created) and makes a connection to the db and returns the connection object.

populatedb() - This function takes two parameters - database connection object, list of incident tuples. This function inserts incident data into the database and returns nothing.

status() - This function takes the database connection object as the parameter and prints a list of the nature of incidents and the number of times they have occurred. This function does not return annything.

## Database Development
The database management system software used in this project is sqlite. 
Schema Overview - 
The database contains a single table, and all the incidents information is stored in this table. The table has 5 columns - incident_time, incident_number, incident_location, nature, incident_ori. All these are of string data type.
incident time - Stores the time of the incident
incident number - Stores the unique number of the incident
incident location - Stores the address where the incident occured
nature - Stores the nature of the incident
incident_ori - Stores the ori code for the incident

Sample data - 
0:01|2024-00000001|3603 N FLOOD AVE|Traffic Stop|OK0140200
0:03|2024-00000001|226 CINDY AVE|Chest Pain|14005
0:03|2024-00000001|226 CINDY AVE|Sick Person|EMSSTAT
0:04|2024-00000002|E MAIN ST / N JONES AVE|Traffic Stop|OK0140200

Database Connection - 
The application connects to the database when the main.py calls the createdb() function. Other database related functions use this connection object as the parameter to perform database operations. 

Database commit - 
The database connection performs a commit operation when the database connection is initially made in the createdb() method or when any data is inserted through the populatedb function

Database connection close - 
The connection object is closed after the execution of the status() method, since it is the final method in the whole project flow. 

## Bugs and Assumptions
1. ORI number is any of the following values - ['OK0140200', 'EMSSTAT', '14005', '14009']. If a pdf file contains ori numbers that are not in this list, they can't be extracted using this code.
2. Address is only a street address and in NOT in any other form (like ending with country, state, etc.). Global address cannot be captured using this code.
3. This code is limited to parsing only US street addresses.

