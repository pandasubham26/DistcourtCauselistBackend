from app.models.cis.base.master.district import DistrictBaseTable


class District_CIS1(DistrictBaseTable):
    __tablename__ = 'district_t'
    __bind_key__ = 'cis_db_1'


class District_CIS2(DistrictBaseTable):
    __tablename__ = 'district_t'
    __bind_key__ = 'cis_db_2'


class District_CIS3(DistrictBaseTable):
    __tablename__ = 'district_t'
    __bind_key__ = 'cis_db_3'


class District_CIS4(DistrictBaseTable):
    __tablename__ = 'district_t'
    __bind_key__ = 'cis_db_4'