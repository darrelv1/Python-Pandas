from datetime import date
import pandas as pd

class Tools:



    def __init__(self):
        return self



    """-----(PARAMETER DOCUMENTATION)------
     $1 - search match
     $2 - dataframe or csv 
     $3 - column in array to search - String
     $4 - column to in which to return from - Int
     $5 - xl - boolean
     $6 - csv columns for datafram - List"""
    #CSV & XL I/O inputs 
    def vlookup( lookup= None , array=None ,col_name = None ,col=None, xl=None, columnsnames=None ):
        df = pd.DataFrame
        #Validate the import 
        if xl:
            df = array
        else:
            data = pd.read_csv(array)
            df =pd.DataFrame(data, columns= columnsnames)

        print(f"Lookup: {lookup}, type: {type(lookup)}")
        print(f"array: {array}, type: {type(array)}")
        print(f"col: {col}, type: {type(col)}") 
        print(f"import_ready: {columnsnames}, type: {type(columnsnames)}") 

        
        
        result = []
        #used different method for indices
        for ind in df.index:
            if df[col_name][ind] == lookup:
                result.append(df.loc[ind][col])

        print(result)
        return result 

"""     def dataframe_generator(name):
        name = pd.
    return name
 """

        



        


    
