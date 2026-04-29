from app.models.cis.base.causelist.daily_proc import DailyProcBaseTable


class DailyProc_CIS1(DailyProcBaseTable):
    __tablename__ = 'daily_proc'
    __bind_key__ = 'cis_db_1'


class DailyProc_CIS2(DailyProcBaseTable):
    __tablename__ = 'daily_proc'
    __bind_key__ = 'cis_db_2'


class DailyProc_CIS3(DailyProcBaseTable):
    __tablename__ = 'daily_proc'
    __bind_key__ = 'cis_db_3'


class DailyProc_CIS4(DailyProcBaseTable):
    __tablename__ = 'daily_proc'
    __bind_key__ = 'cis_db_4'