from app.models.cis.base.master.judgecourt import JudgeCourtBaseTable


class JudgeCourt_CIS1(JudgeCourtBaseTable):
    __tablename__ = 'judge_t'
    __bind_key__ = 'cis_db_1'


class JudgeCourt_CIS2(JudgeCourtBaseTable):
    __tablename__ = 'judge_t'
    __bind_key__ = 'cis_db_2'


class JudgeCourt_CIS3(JudgeCourtBaseTable):
    __tablename__ = 'judge_t'
    __bind_key__ = 'cis_db_3'


class JudgeCourt_CIS4(JudgeCourtBaseTable):
    __tablename__ = 'judge_t'
    __bind_key__ = 'cis_db_4'