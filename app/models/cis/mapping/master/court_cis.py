from app.models.cis.base.master.court import CourtBaseTable


class Court_CIS1(CourtBaseTable):
    __tablename__ = 'court_name'
    __bind_key__ = 'cis_db_1'


class Court_CIS2(CourtBaseTable):
    __tablename__ = 'court_name'
    __bind_key__ = 'cis_db_2'


class Court_CIS3(CourtBaseTable):
    __tablename__ = 'court_name'
    __bind_key__ = 'cis_db_3'


class Court_CIS4(CourtBaseTable):
    __tablename__ = 'court_name'
    __bind_key__ = 'cis_db_4'