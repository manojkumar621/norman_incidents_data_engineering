import os
import pytest
from assignment0.fetchincidents import fetchincidents

@pytest.fixture
def sample_pdf_url():
    '''Provides a constant sample url to test downloading the data'''
    return "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"

def test_fetchincidents_success(sample_pdf_url):
    '''Test function to test the function to download the data and 
    write the data into a file'''
    tmp_dir = 'test_files/'
    # Construct the path to save the downloaded PDF file
    pdf_path = tmp_dir + "test_incident_data.pdf"

    # Fetch incidents and save the PDF file
    data = fetchincidents(sample_pdf_url)
    assert data is not None
    assert len(data) > 0
    with open(pdf_path, 'wb') as file:
        file.write(data)

    # Check if the file is created and not empty
    assert os.path.getsize(pdf_path) > 0