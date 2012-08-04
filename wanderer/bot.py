from datetime import datetime
from apscheduler.scheduler import Scheduler
from wanderer import History

sc = Scheduler()
sc.start()

def job_function():
    import sys
    sys.stdout.write('\a')
    sys.stdout.flush()
    print "testing"
    
sc.add_interval_job(job_function, minutes = 1)
