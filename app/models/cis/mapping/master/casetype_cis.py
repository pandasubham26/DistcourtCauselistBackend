from app.models.cis.base.master.casetype import CaseTypeBaseTable


class CaseType_CIS1(CaseTypeBaseTable):
    __tablename__ = 'case_type_t'
    __bind_key__ = 'cis_db_1'


class CaseType_CIS2(CaseTypeBaseTable):
    __tablename__ = 'case_type_t'
    __bind_key__ = 'cis_db_2'


class CaseType_CIS3(CaseTypeBaseTable):
    __tablename__ = 'case_type_t'
    __bind_key__ = 'cis_db_3'


class CaseType_CIS4(CaseTypeBaseTable):
    __tablename__ = 'case_type_t'
    __bind_key__ = 'cis_db_4'