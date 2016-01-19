import csv
import dataset
from normality import normalize
from .sissy import StdoutToggle
#from .bar import EnhancedBar
from tqdm import tqdm
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
    sis = StdoutToggle()
    sis.set_to_terminal()
    for x in tqdm(json_gen):
        print("Loading....")
        print(x)
        print("\n")
        print("\n")
        
        table.insert(x)
    sis.set_to_ipython()
    return table
