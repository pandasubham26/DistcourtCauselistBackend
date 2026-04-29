from app.models.cis.base.master.designation import DesignationBaseTable


class Designation_CIS1(DesignationBaseTable):
    __tablename__ = 'desg_t'
    __bind_key__ = 'cis_db_1'


class Designation_CIS2(DesignationBaseTable):
    __tablename__ = 'desg_t'
    __bind_key__ = 'cis_db_2'


class Designation_CIS3(DesignationBaseTable):
    __tablename__ = 'desg_t'
    __bind_key__ = 'cis_db_3'


class Designation_CIS4(DesignationBaseTable):
    __tablename__ = 'desg_t'
    __bind_key__ = 'cis_db_4'