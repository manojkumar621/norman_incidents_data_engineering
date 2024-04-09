import pytest
import os
from assignment0.dbmanager import createdb, populatedb, status

@pytest.fixture
def temp_db_connection():
    db_path = "resources/test_sample.db"
    con = createdb(db_path)
    yield con
    con.close()
    os.remove(db_path)

def test_createdb(temp_db_connection):
    '''tests createdb function'''
    assert temp_db_connection is not None

def test_populatedb(temp_db_connection):
    '''tests populatedb function'''
    incidents_data = [
        ("2022-01-01 12:30", "2022-000001", "123eAFA Main St", "Suspicious", "OK123456"),
        ("2022 qw4G", " 2arsdGTQ", "qefQR", "Gunshots", "qeEAFr")
    ]
    populatedb(temp_db_connection, incidents_data)

    cursor = temp_db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    total_rows = cursor.fetchone()[0]
    assert total_rows > 0

def test_status(temp_db_connection, capsys):
    '''tests populatedb function'''
    status(temp_db_connection)
    captured = capsys.readouterr()

    assert captured.out is not None
