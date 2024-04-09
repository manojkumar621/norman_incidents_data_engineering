import argparse
from .fetchincidents import fetchincidents
from .extractdata import extractdata
from .dbmanager import createdb, populatedb, status
import sys
# from assignment0 import fetchincidents
# from . import fetchincidents
PDF_PATH = 'resources/incident_data.pdf'
DB_NAME = 'normanpd.db'
DB_PATH = 'resources/'
def main(url):
    """Function Downloads data, extracts incidents data, saves the data in a database 
        and prints the status of the incidents"""

    # # Download data
    incident_data = fetchincidents(url)
    # print("WRITING DATA")
    with open(PDF_PATH,'wb') as file:
        file.write(incident_data)
    # print("Data Fetched and Downloaded!")

    # # Extract data
    # all_incidents = extractdata(incident_data)
    all_incidents = extractdata(PDF_PATH)
    # print(all_incidents)
	
    # # Create new database
    # db = createdb(DB_PATH + DB_NAME)
	
    # # Insert data
    # populatedb(db, all_incidents)
	
    # # Print incident counts
    # status(db)
    # sys.exit(0)
    return all_incidents




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)