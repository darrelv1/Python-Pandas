from abc import ABC, abstractmethod
from nbformat import write

import pandas as pd
from datetime import datetime

class Basereports(ABC): 

    date = ""
    
    
    def __init__(self, link):
        
        self.name = "Reporting"
        self.stringlink = ""


    @abstractmethod

    def dictionarydf():
        pass


    @abstractmethod
    
    def printer(stringlink):
        pass

    @abstractmethod
    def get_name(self):
        pass


class Reports(Basereports):
    
    
    date = datetime.today().strftime("%m-%d-%y")

    alberta_sold = [
        "10199 Mount Royal Care Centre", 
        "10200 Jasper Place",
        "10201 South Terrace",
        "10202 Riverview",
        "10203 Bow-Crest Care Centre",
        "10204 McKenzie Towne Continuing Care",
        "10205 Miller Crossing Care Centre"
        ]
    
    
    def __init__(self, link):
        super().__init__(link)
        self.link = link
        self.name = Reports.date
        self.stringlink = "output/"+self.name+".xlsx"
        self.raw_report = pd.read_excel(link)
        self.jobcostdf = self.raw_report[self.raw_report["Ledger Account"] == "24110:Construction in Progress"]
        self.reports=None
        self.reports_str=None
        self.reportname_list = []
        
        
    def dictionarydf(self):

        dictionaryholder = {}
        index = 0 
        for k in self.reports_str:
            dictionaryholder[k] = self.reports_list[index]
            index += 1

        return dictionaryholder

    
       
    def printer(self):

        dictionaryholder = self.dictionarydf() 
    
        with pd.ExcelWriter(self.stringlink) as writer:
            for k,v in dictionaryholder.items():


                v.to_excel(writer, sheet_name= k )


            for i in dictionaryholder.keys():
                
                temp = dictionaryholder[i]
                if temp.empty:
                            continue

                temp = temp.pivot_table(index = "Source", aggfunc= sum)
                
            
                total = temp["Amount"]
                temp = pd.concat([temp, total], axis =1)



                name = i + " PivotTable"
                totalname = i + "Total"
                #print(f"{name}: {temp}")
                temp.to_excel(writer,sheet_name= name)

        return "Completed"

    def reportbysite(self, report):
        return report.groupby(['Site']).sum()

    def get_name(self):
        return(self.name)
    def get_jobcost(self):
        return(self.jobcostdf)
    






class Jobcostreport(Reports):
        

 

    def __init__(self, link):
        super().__init__(link)
        self.name= "JobCostRFJL-"+Reports.date
        self.stringlink = "output/"+self.name+".xlsx"
        self.jobcostdf2 = self.jobcostdf.loc[:,:][self.jobcostdf.Source != "Asset Disposal"]
        self.jobcostdfRAW = self.jobcostdf
        source =  set()
        for i in self.jobcostdf2.Source:
            source.add(i)

        #Reports by Filters 
        self.disposaldf = self.jobcostdf2.loc[:,:][self.jobcostdf2.Source == "Asset Disposal"]
       
        self.transferdf = self.jobcostdf2[(~self.jobcostdf2['Worktags'].str.contains('fund') & ~self.jobcostdf2['Worktags'].str.contains('Fund') ) & ((self.jobcostdf2['Line Memo'].str.contains('Tsfr', na = False)) | (self.jobcostdf2['Journal Memo'].str.contains('Tsfr', na = False)) | ((self.jobcostdf2.Source == 'Asset Assign Accounting')))]
        self.Additiondf =  self.jobcostdf2[(self.jobcostdf2.Source.isin(source) & (self.jobcostdf2['Worktags'].str.contains('fund') | self.jobcostdf2['Worktags'].str.contains('Fund') | ~self.jobcostdf2['Line Memo'].str.contains('Tsfr', na = False) & ~self.jobcostdf2['Line Memo'].str.contains('Trsfr', na = False)  & ~self.jobcostdf2['Journal Memo'].str.contains('Tsfr', na = False) & ~self.jobcostdf2['Journal Memo'].str.contains('Trsfr', na = False)))]
        self.Additiondf = self.Additiondf[ (self.Additiondf['Worktags'].str.contains('fund') | self.Additiondf['Worktags'].str.contains('Fund')) | ~self.Additiondf['Source'].str.contains("Asset Assign Accounting")]

        #Container
        self.reports_list= [self.jobcostdfRAW, self.disposaldf, self.jobcostdf, self.transferdf, self.Additiondf]
        self.reports_str= ["jobcostdfRAW","disposaldf", "jobcostdf", "transferdf" , "Additiondf" ]
        
        self.reportname_list = []



    def get_name(self):
        return (self.name)


    def get_additions(self):
        print(self.Additiondf)
        return (self.Additiondf)

    def get_disposals(self):
        return (self.disposaldf)    

    def get_transfers(self):
        return(self.transferdf)

    def get_jobcostdf(self):
        return(self.jobcostdf)


        


class Capital_Jobcostreport(Jobcostreport):

    def __init__(self, link):
        super().__init__(link)

        self.name= "JobCostRFJL_cap-"+Reports.date
        self.stringlink = "output/"+self.name+".xlsx"
        self.jobcostdf2 = self.jobcostdf.loc[:,:][self.jobcostdf.Source != "Asset Disposal"]
        self.jobcostdfRAW = self.jobcostdf

        source =  set()
        for i in self.jobcostdf2.Source:
            source.add(i)


        self.transferdf = self.jobcostdf[(~self.jobcostdf['Worktags'].str.contains('fund') & ~self.jobcostdf['Worktags'].str.contains('Fund') ) & (self.jobcostdf['Line Memo'].str.contains('Tsfr', na = False)) | ((self.jobcostdf['Line Memo'].str.contains('Trsfr', na = False)) | (self.jobcostdf['Journal Memo'].str.contains('Tsfr', na = False))|  (self.jobcostdf['Journal Memo'].str.contains('Trsfr', na = False))  | ((self.jobcostdf.Source == 'Asset Assign Accounting')))]
        self.transferdf = self.transferdf[(self.transferdf["Supplier"].isna()) & (self.transferdf.Source == "Asset Assign Accounting")]
        self.Additiondf = self.jobcostdf2[(self.jobcostdf2.Source.isin(source) & (self.jobcostdf2['Worktags'].str.contains('fund') | self.jobcostdf2['Worktags'].str.contains('Fund') | ~self.jobcostdf2['Line Memo'].str.contains('Tsfr', na = False) & ~self.jobcostdf2['Line Memo'].str.contains('Trsfr', na = False)  & ~self.jobcostdf2['Journal Memo'].str.contains('Tsfr', na = False) & ~self.jobcostdf2['Journal Memo'].str.contains('Trsfr', na = False)))]
        self.Additiondf = self.Additiondf[ ((self.Additiondf["Source"] == 'Asset Assign Accounting') & (self.Additiondf["Supplier"].notna()) |  self.Additiondf['Worktags'].str.contains('fund') | self.Additiondf['Worktags'].str.contains('Fund')) | ~self.Additiondf['Source'].str.contains("Asset Assign Accounting")]


    #Container
        self.reports_list= [self.jobcostdfRAW, self.disposaldf, self.jobcostdf, self.transferdf, self.Additiondf]
        self.reports_str= ["jobcostdfRAW","disposaldf", "jobcostdf", "transferdf" , "Additiondf" ]
        
        self.reportname_list = []



    def get_name(self):
        return (self.name)


    def get_additions(self):
        print(self.Additiondf)
        return (self.Additiondf)

    def get_disposals(self):
        return (self.disposaldf)    

    def get_transfers(self):
        return(self.transferdf)

    def get_jobcostdf(self):
        return(self.jobcostdf)




  
class flowthrough(Reports): 

    def __init__(self, link):
        super().__init__(link)

        self.name= "FlowthroughRFJL-" + Reports.date
        self.stringlink = "output/"+self.name+".xlsx"
        self.costAdditionsdf = self.raw_report[self.raw_report["Ledger Account"] == "25200:Property & Equipment"]
        self.accumDeprndf = self.raw_report[self.raw_report["Ledger Account"] == "26000:Accumulated Depreciation"]
        self.deprnAmordf = self.raw_report[self.raw_report["Ledger Account"] == "91000:Depreciation & Amortization"]
        

        self.costDisposal = self.costAdditionsdf[self.costAdditionsdf["Source"] == "Asset Disposal"]
        self.costAdditionsdf = self.costAdditionsdf[self.costAdditionsdf["Source"] != "Asset Disposal"]
        
        #Sold Site Activity 
        self.cost_sold = self.costAdditionsdf[self.costAdditionsdf['Site'].isin(Reports.alberta_sold)]
        self.accum_sold = self.accumDeprndf[self.accumDeprndf['Site'].isin(Reports.alberta_sold)]
        self.deprn_sold = self.deprnAmordf[self.deprnAmordf['Site'].isin(Reports.alberta_sold)]


        #Container
        self.reports_list= [self.costAdditionsdf, self.accumDeprndf, self.deprnAmordf, self.costDisposal]
        self.reports_str =["costAdditionsdf","accumDeprndf","deprnAmordf","costDisposal"]
        
        
    def get_additions(self):
        print(self.costAdditionsdf)
        return (self.costAdditionsdf)

    def get_disposal(self):
        return (self.costdisposaldf)

    def get_accumdeprn(self):
        return (self.accumDeprndf)  

    def get_deprnamor(self):
        print(self.deprnAmordf)
        return (self.deprnAmordf)


class Holdbacks(flowthrough):

    def __init__(self, link): 
        super().__init__(link)

        self.name="Holdbacks -" + Reports.date
        self.holdbackdf =  self.raw_report[self.raw_report["Ledger Account"] == "32412:Holdbacks Payable"]
        

    def get_holdback(self):
        return (self.holdbackdf)





