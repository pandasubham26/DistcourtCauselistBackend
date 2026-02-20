from app.models.cis.base.master.state import StateBaseTable


class State_CIS1(StateBaseTable):
    __tablename__ = 'state'
    __bind_key__ = 'cis_db_1'


class State_CIS2(StateBaseTable):
    __tablename__ = 'state'
    __bind_key__ = 'cis_db_2'


class State_CIS3(StateBaseTable):
    __tablename__ = 'state'
    __bind_key__ = 'cis_db_3'


class State_CIS4(StateBaseTable):
    __tablename__ = 'state'
    __bind_key__ = 'cis_db_4'