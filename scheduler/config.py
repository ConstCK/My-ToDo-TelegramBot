from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

job_stores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
}
