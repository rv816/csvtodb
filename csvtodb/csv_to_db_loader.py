from etl_modules.etl_setup import engine, meta
import sqlalchemy as sa
import strconv as sc
import csv
from collections import OrderedDict

def smart_convert(value):
    import strconv as sc
    if sc.infer(value) == 'float' or sc.infer(value) == 'int':
        try:
            return int(value)
        except:
            try:
                return float(value)
            except:
                return str(value)
    elif sc.infer(value) == 'str':
        return str(value)
    else:
        return str(value)

class Loader:
    def __init__(self, tablename, engine = engine):
        self.tablename = tablename
        self.engine = engine
        setattr(self, 'con', self.engine.connect())
        from collections import OrderedDict

    def read_csv(self, csvpath):
        with open(csvpath, 'r') as csvobj:
            self.rowlist = list(csv.reader(csvobj))    
        self.keys = self.rowlist[0]
        self.temp =  [zip(self.keys, x) for x in self.rowlist]
        tempdicts = [dict(x) for x in self.temp]
        self.data = []
        for x in tempdicts:
            self.data.append({key: value for key, value in x.items() if len(key) > 0})

    
    def create_table_object(self):
        setattr(self, self.tablename, sa.Table(self.tablename, meta, autoload=True, autoload_with = engine))
        self.insert_statement = getattr(self, self.tablename).insert()
        print("Table " + str(self.tablename) + " created with the following columns...")
        print(str(getattr(self, self.tablename).columns))
    
    def add_to_table(self, data):

        error_log = []
        count = 0
        self.trans = self.con.begin()
        try:            
            for rownumber in range(1, len(data) -1):
                valdict = {}
                for key, value in data[rownumber].items():
                    print('key '+ str(key))
                    print ('value ' + str(value))
                    keyobj= getattr(self, self.tablename).columns.get(key)
                    if keyobj is not None and key != '' and value != '':
                        valdict[key] = sa.cast(smart_convert(value), keyobj.type)


                try:
                    if len(str(valdict.get('person_id').compile().params.values()[0])) < 3:
                        next
                    else:
                        self.con.execute(self.insert_statement.values(valdict))
                        count +=1
                except Exception as err:
                    print("Error at statement: ")
                    print("\t\t " + str(rownumber) + str(valdict) + str(err))
                    error_log.append([rownumber, valdict, err])

            self.trans.commit() 
        except Exception as err:
            print(err)
            self.trans.rollback()
            raise err
        def job_summary(count, error_log):
            summary = str("Job completed. There were " + str(count) + " statements read correctly out of " + str(rownumber + 1))
            errors = "There were " + str(len(error_log)) + " errors."
            results = {'Summary': summary, 'errors': errors, 'error_log': error_log}
            self.results = results
            return results
        print('\n')
        print(job_summary(count, error_log))
                
                
            

            
        
    def __repr__(self):
        try:
            getattr(self, self.tablename)
            print("SQL Alchemy Table Class: " + self.tablename) 
            for key, value in getattr(getattr(self, self.tablename), 'columns').items():
                print("\tColumn Name: " + str(key))
                try:
                    print('\t\t Corresponding Object: '  + str(value.__repr__()))
                except:
                    pass
            return getattr(self, self.tablename)
        except:
            return "<class Loader for table " + str(self.tablename) + ">"
        

def runner(table, csvfile):            
    load = Loader(table, engine)
    load.create_table_object()
    load.read_csv(csvfile)
    load.add_to_table(load.data)
             
