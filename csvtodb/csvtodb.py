import csv
import dataset
from normality import normalize

def jsonify(csvlist, preheadings=None, heading_line = 0, data_start_line = 1):
    """
    Convert CSV into a JSON
    using either `preheadings` or csvilst[heading_line]
    as keys. Yields generator of dicts.
    """
    if not preheadings:
        preheadings = csvlist[0]
        headings = [normalize(x).replace(' ', '_') for x in preheadings]
    

    csvlist_data_only = csvlist[data_start_line:]
    for line in csvlist_data_only:
        yield dict(zip(headings, line))
        

def upload_to_db(csv_as_list, tablename, db_url):
    db = dataset.connect(db_url)
    table = db[tablename]
    json_gen = jsonify(csv_as_list)
    for x in json_gen:
        print(x)
        table.insert(x)
    return table
