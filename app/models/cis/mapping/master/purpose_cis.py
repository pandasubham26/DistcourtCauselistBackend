from app.models.cis.base.master.purpose import PurposeTBaseTable


class PurposeT_CIS1(PurposeTBaseTable):
    __tablename__ = 'purpose_t'
    __bind_key__ = 'cis_db_1'


class PurposeT_CIS2(PurposeTBaseTable):
    __tablename__ = 'purpose_t'
    __bind_key__ = 'cis_db_2'


class PurposeT_CIS3(PurposeTBaseTable):
    __tablename__ = 'purpose_t'
    __bind_key__ = 'cis_db_3'


class PurposeT_CIS4(PurposeTBaseTable):
    __tablename__ = 'purpose_t'
    __bind_key__ = 'cis_db_4'