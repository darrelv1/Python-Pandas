import pandas as pd 
from ProjectStatusGenerator import masterdataframe
from ProjectStatusGenerator import accountant



CapitalSpenddf = pd.read_excel("POGeneratorSourcefiles/Capital Spend by CEA MAY.xlsx", sheet_name= "Sheet1", usecols = "A:Q", header = 9)

#Removal of all n/a and null from the projects columns 
# "~" --> it will invert the bool series
CapitalSpenddf = CapitalSpenddf[~CapitalSpenddf['Project'].isnull()]
#Removal of all n/a and null from the PO Line columns 
CapitalSpenddf = CapitalSpenddf[~CapitalSpenddf['PO Line#'].isnull()]


CapitalSpenddf = CapitalSpenddf[["Company", "Project", "PO Line#", "Requisition Line Amount", "Purchase Order Line Amount", "Requisition #","Spend Category",'Uninvoiced Amount in Reporting Currency']]


CSdf = CapitalSpenddf

mdf = masterdataframe()
mdf = mdf.rename(columns= {"Project Number:" : "Project"})
mdf = mdf[['Project', 'PM', 'Accountant_x','Balance']]
mdf['Completed Y/N?'] = ""
mdf["Project Manager's Notes"] = ""



result_left = pd.merge(mdf,CSdf, how= "left", on= ['Project'])
result_left = result_left[['Project','PO Line#','Balance', 'Uninvoiced Amount in Reporting Currency', 'Completed Y/N?','Purchase Order Line Amount', 'PM', 'Accountant_x',"Project Manager's Notes"]]
#from the class i'm getting the list of PMs
Darrel_PMs = masterdataframe.pms

#creating dic of DF
finaldict = {elem : pd.DataFrame() for elem in Darrel_PMs}
for i in finaldict.keys(): 
    finaldict[i] = result_left[result_left.PM == i]

#Filtering to only include whats > 0 for the  Uninvoiced Amount of the purchase order
for i in finaldict.keys():
    df = finaldict[i]
    if df.empty:
        continue
    else: 
        accruals_filter = df["Uninvoiced Amount in Reporting Currency"] > 0 
        df = df.loc[accruals_filter]
    finaldict[i] = df

#Sorting 
for i in finaldict.keys():
    df = finaldict[i]
    if df.empty:
        continue
    if df['Project'].apply(type).eq(int).any():
        df = df.applymap(str)
        print("Inner"+i)
    finaldict[i] = df.sort_values(by= ["Project"])
    print("reached")



#creating workbooks for PM dataframes
for i in finaldict.keys():
    pm = i.replace(" ","")
    stringlink = 'outputfiles/DistrubtionReady/'+pm+' - '+accountant+'.xlsx'

    finaldict[i].to_excel(stringlink)



#notifies when it complete
print("finished")