
from datetime import datetime
import pandas as pd
from xlsxwriter import workbook
import ProjectStatusGenerator_helper
import subprocess
import openpyxl
from xlsxwriter.workbook import *
import xlwt





pd.set_option("display.max_rows", None, "display.max_columns", None)




masterdf = pd.DataFrame()


date = datetime(datetime.today().year, datetime.today().month,  1)

date = date.strftime("%m/%y")

#IMPORTANT - THIS WILL DICTATE THE ACCOUNTANT IT WILL PRODUCE REPORTS FOR
accountant = "Darrel"
month_of_status_report_three_digit= "may"

file = "ProjectGeneratorSourcefiles/"+ month_of_status_report_three_digit + "_project_status.xlsx"
 
PMs_columns = ['PM','Total','Funded','Remaining','Accountant']


PMs = pd.read_excel(file, sheet_name = "Accountant per PM", usecols = "A:E", nrows=63)
Project_status = pd.read_excel(file, sheet_name = "Project Status", usecols = "A:G", header = 3, na_filter = True)


Project_status.drop('Monthly Status', axis = 1, inplace = True)
Project_status.drop(' Next Steps', axis = 1, inplace = True)
Project_status['Completed Y/N?'] = None

collist_rearranged = ['Project Number:', ' Date of Completion or Last PM Check', 'Balance','Completed Y/N?', 'PM','Accountant']


#Pre-Filters
#Remove all Funding Projects out
filter_notfunded = Project_status["Project Number:"].str.contains('fund')| Project_status["Project Number:"].str.contains('Fund') | Project_status["Project Number:"].str.contains('IPAC')
filter_cancelled = Project_status[" Date of Completion or Last PM Check"].str.contains('cancel') |  Project_status[" Date of Completion or Last PM Check"].str.contains('Cancel')


Project_status = Project_status.loc[~filter_notfunded]
Project_status = Project_status.loc[~filter_cancelled]


# $1 - search match
# $2 - dataframe or csv 
# $3 - column in array to search - String
# $4 - column to in which to return from - Int
# $5 - xl - boolean
# $6 - csv columns for datafram - List

Darrel_PMs = ProjectStatusGenerator_helper.Tools.vlookup(accountant,  PMs, "Accountant", 0, True, PMs_columns)

DarrelPMs_df= pd.DataFrame(Darrel_PMs)
DarrelPMs_df["Accountant"] = accountant

""" print(Project_status)
print(DarrelPMs_df)
print(DarrelPMs_df.columns) """
DarrelPMs_df.rename(columns={0: "PM"})
DarrelPMs_df.columns = ["PM", "Accountant"]
""" print(DarrelPMs_df)

print(type(DarrelPMs_df.columns[0]))
print(Project_status) """



#print(DarrelPMs_df.columns)
#Merge of the PM listing and the ProjectStatus DataFrame
merge1 = Project_status.merge(DarrelPMs_df, on= 'PM')


#print(merge1.columns)
#print(merge1["Accountant"])
#print(type(merge1))



#print(merge1)

#create a datafram for each to the PM,
#Link of assistance https://newbedev.com/create-multiple-dataframes-in-loop

#creation of unique names 
    #already did that 

#Creation of a datafram dictionary to store my data frames

Darrel_PMs_dict = {elem : pd.DataFrame() for elem in Darrel_PMs}




#print(Darrel_PMs_d




""" for i in Darrel_PMs:
   print("\n")
   print(i) 
   print("\n")
   print(pd.DataFrame(merge1[merge1.PM == i])) 
   happ = pd.DataFrame(merge1[merge1.PM == i]) """



for i in Darrel_PMs_dict.keys():
    Darrel_PMs_dict[i] = merge1[merge1.PM == i]

Darrel_PMs_dict.values

#print(Darrel_PMs_dict["Adam Moy"])

#Creation of Each indivdual Dataframe for the PMs
# """ AdamMoy_df = Darrel_PMs_dict["Adam Moy"]

# Alex_df = Darrel_PMs_dict['Alex Bruce']
# Andrew_df = Darrel_PMs_dict[ 'Andrew Bautista']
# Franco_df = Darrel_PMs_dict["Franco D'Angelo"]
# Joan_df = Darrel_PMs_dict['Joan Dewaele']
# Robert_df = Darrel_PMs_dict[ 'Robert Laporte']
# Trevor_df = Darrel_PMs_dict['Trevor Shoemaker']
# Vanessa_df = Darrel_PMs_dict['Vanessa Fuentes-Castro']
# Cameron_df = Darrel_PMs_dict[ 'Cameron Scully']
# Maeve_df = Darrel_PMs_dict[ 'Maeve Paterson']
# Jeff_df = Darrel_PMs_dict[ 'Jeff Krusky'] """


#AdamMoy_df = AdamMoy_df[(AdamMoy_df[' Date of Completion or Last PM Check '].str.contains("New")) | AdamMoy_df[' Date of Completion or Last PM Check '].str.contains("Not Complete")]
#Maeve_df = Maeve_df[(Maeve_df[' Date of Completion or Last PM Check '].str.contains("New")) | Maeve_df[' Date of Completion or Last PM Check '].str.contains("Not Complete")]
#Jeff_df = Jeff_df[(Jeff_df[' Date of Completion or Last PM Check '].str.contains("New")) | Jeff_df[' Date of Completion or Last PM Check '].str.contains("Not Complete")]


#new - "Non Completed Projects"
New_Darrel_PMs_dict ={}

for name in  Darrel_PMs_dict.keys():
    New_Darrel_PMs_dict[name] = pd.DataFrame()

#new - "Completed and now Accural based Projects"
Accrual_Darrel_PMs_dict = {}

for name in Darrel_PMs_dict.keys():
    Accrual_Darrel_PMs_dict[name] = pd.DataFrame()



for name in  Darrel_PMs_dict.keys():
    temp = Darrel_PMs_dict[name]
    if Darrel_PMs_dict[name].empty:
        print(f"{name} in if condition")
        continue
    
    elif (temp[' Date of Completion or Last PM Check'].apply(type).eq(str).any()):
        print(temp[temp[' Date of Completion or Last PM Check'].str.contains("New", na= False)])
        New_Darrel_PMs_dict[name] =  temp[(~temp[' Date of Completion or Last PM Check'].apply(type).eq(datetime)) & (temp[' Date of Completion or Last PM Check'].str.contains("New") | temp[' Date of Completion or Last PM Check'].str.contains("Not Complete") | temp[' Date of Completion or Last PM Check'].str.contains("Completion") | temp[' Date of Completion or Last PM Check'].str.contains("", na= True))]
    else:
        print(f"{name} in Else condition")
        continue

#filters
"""filter_notcomplete = Accrual_Darrel_PMs_dict[' Date of Completion or Last PM Check'].str.contains("complete",na= False)| Accrual_Darrel_PMs_dict[' Date of Completion or Last PM Check'].str.contains("Complete",na= False) |Accrual_Darrel_PMs_dict[' Date of Completion or Last PM Check'].str.contains("completion",na= False)
"""
#Small exact loop for the non completed - this is in effort to create accrual database        
for name in  Darrel_PMs_dict.keys():
    temp = Darrel_PMs_dict[name]
    
    
    if Darrel_PMs_dict[name].empty:
        print(f"{name} in if condition")
        continue
    
    elif temp[' Date of Completion or Last PM Check'].apply(type).eq(str).any():
            filter_notcomplete = temp[' Date of Completion or Last PM Check'].str.contains("complete",na= False)| temp[' Date of Completion or Last PM Check'].str.contains("Complete",na= False) | temp[' Date of Completion or Last PM Check'].str.contains("completion",na= False) | temp[' Date of Completion or Last PM Check'].str.contains("New") 
            Accrual_Darrel_PMs_dict[name] = temp.loc[~filter_notcomplete]

    
    elif temp[' Date of Completion or Last PM Check'].apply(type).eq(datetime).any() :
            filter_datatype = temp[' Date of Completion or Last PM Check'].apply(type).eq(datetime)
            Accrual_Darrel_PMs_dict[name] = temp.loc[filter_datatype]

    else:
        print(f"{name} in Else condition")
        continue
        #New_Darrel_PMs_dict[name] =  temp[(temp['Date of Completion or Last PM Check'].str.contains("New")) | (temp['Date of Completion or Last PM Check'].str.contains("Not Complete"))]
    
#writing to an excel sheet
##output = workbook('outputfiles/Project Status Report -  November.xlsx')

##writer = pd.ExcelWriter(output) 


#am_df=New_Darrel_PMs_dict['Adam Moy']

#am_df.to_excel('outputfiles/sheet1.xlsx')

#Sorting
for i in New_Darrel_PMs_dict.keys():
    df = New_Darrel_PMs_dict[i]
    if df.empty:
        continue
    if df['Project Number:'].apply(type).eq(int).any():
        df = df.applymap(str)
        print("Inner"+i)
    New_Darrel_PMs_dict[i] = df.sort_values(by= ["Project Number:"])
    print("reached")


#Sorting for accural dfs
for i in Accrual_Darrel_PMs_dict.keys():
    df = Accrual_Darrel_PMs_dict[i]
    if df.empty:
        continue
    if df['Project Number:'].apply(type).eq(int).any():
        df = df.applymap(str)
        print("Inner"+i)
    Accrual_Darrel_PMs_dict[i] = df.sort_values(by= ["Project Number:"])
    print("reached")




#creating xl workbooks for PM dataframes
for i in New_Darrel_PMs_dict.keys():
    pm = i.replace(" ","")
    stringlink = 'outputfiles/'+pm+' - '+accountant+'.xlsx'

    New_Darrel_PMs_dict[i].to_excel(stringlink)



#creating xl workbooks for PM accrual dataframes
for i in Accrual_Darrel_PMs_dict.keys():
    pm = i.replace(" ","")
    stringlink = 'outputfiles/Accrual'+pm+' - '+accountant+'.xlsx'

    Accrual_Darrel_PMs_dict[i].to_excel(stringlink)






#creating a master dataframe to index and match 

concat_dataframe = []

for ind in Accrual_Darrel_PMs_dict.keys():
    concat_dataframe.append(Accrual_Darrel_PMs_dict[ind])

masterdf = pd.concat(concat_dataframe)


class masterdataframe:

    master = pd.DataFrame()
    pms = Darrel_PMs
    getter_PM = []

    def __new__(cls):  
        master = masterdf
        pms = Darrel_PMs
        return master
 


 
   
  