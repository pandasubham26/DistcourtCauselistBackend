from app.models.cis.base.master.judge import JudgeNameBaseTable


class JudgeName_CIS1(JudgeNameBaseTable):
    __tablename__ = 'judge_name_t'
    __bind_key__ = 'cis_db_1'


class JudgeName_CIS2(JudgeNameBaseTable):
    __tablename__ = 'judge_name_t'
    __bind_key__ = 'cis_db_2'


class JudgeName_CIS3(JudgeNameBaseTable):
    __tablename__ = 'judge_name_t'
    __bind_key__ = 'cis_db_3'


class JudgeName_CIS4(JudgeNameBaseTable):
    __tablename__ = 'judge_name_t'
    __bind_key__ = 'cis_db_4'