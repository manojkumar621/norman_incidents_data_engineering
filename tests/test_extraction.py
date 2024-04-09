import pytest
from assignment0.extractdata import extractdata, extract_time, extract_address
from assignment0.extractdata import extract_nature_and_ori, extract_number


@pytest.fixture
def sample_pdf_path():
    '''Provides a sample pdf path to test data extraction'''
    return "test_files/test_incident_data.pdf"

@pytest.fixture
def sample_incident_string():
    '''Provides a sample incident string to test each data parsing method'''
    return "1/1/2024 0:01 2024-00000001 3603 N FLOOD AVE Traffic Stop OK0140200"

def test_data_extraction(sample_pdf_path):
    '''Tests extractdata method that extracts all the relevant keys from the raw data'''
    all_incidents = extractdata(sample_pdf_path)
    assert all_incidents is not None
    assert len(all_incidents)>0

def test_extract_time(sample_incident_string):
    '''Tests extract_time method that extracts time from the raw incident string'''
    time = extract_time(sample_incident_string)
    assert time is not None
    assert time == '0:01'

def test_extract_number(sample_incident_string):
    '''Tests extract_number method that extracts number from the raw incident string'''
    number = extract_number(sample_incident_string)
    assert number is not None
    assert number == '2024-00000001'

def test_extract_nature_and_ori(sample_incident_string):
    '''Tests extract_nature_and_ori method that extracts the nature of the incident 
    and its ori number from the raw incident string'''
    nature, ori = extract_nature_and_ori(sample_incident_string, 43)
    assert nature is not None
    assert ori is not None
    assert nature == "Traffic Stop"
    assert ori == "OK0140200"

def test_extract_address(sample_incident_string):
    '''Tests extract_address method that extracts the location of 
    the incident from the raw incident string'''
    address = extract_address(sample_incident_string)[0]
    assert address is not None
    assert address == "3603 N FLOOD AVE"