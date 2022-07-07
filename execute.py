from BaseReport import *

tfile = "May RFJL.xlsx"

March14_flow = flowthrough(tfile)
March14_flow.printer()

March14_job = Jobcostreport(tfile)
March14_job.printer()


March14_jobcap = Capital_Jobcostreport(tfile)
March14_jobcap.printer()