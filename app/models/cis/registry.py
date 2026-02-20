from app.models.cis.mapping.cases.civil_t_cis import CivilT_CIS1, CivilT_CIS2, CivilT_CIS3, CivilT_CIS4
from app.models.cis.mapping.causelist.daily_proc_cis import DailyProc_CIS1, DailyProc_CIS2, DailyProc_CIS3, \
    DailyProc_CIS4
from app.models.cis.mapping.master.casetype_cis import CaseType_CIS1, CaseType_CIS2, CaseType_CIS3, CaseType_CIS4
from app.models.cis.mapping.master.designation_cis import Designation_CIS1, Designation_CIS2, Designation_CIS3, \
    Designation_CIS4
from app.models.cis.mapping.master.district_cis import District_CIS1, District_CIS2, District_CIS3, District_CIS4
from app.models.cis.mapping.master.judge_cis import JudgeName_CIS1, JudgeName_CIS2, JudgeName_CIS3, JudgeName_CIS4
from app.models.cis.mapping.master.judgecourt_cis import JudgeCourt_CIS1, JudgeCourt_CIS2, JudgeCourt_CIS3, \
    JudgeCourt_CIS4
from app.models.cis.mapping.master.purpose_cis import PurposeT_CIS1, PurposeT_CIS3, PurposeT_CIS2, PurposeT_CIS4
from app.models.cis.mapping.master.state_cis import State_CIS1, State_CIS3, State_CIS2, State_CIS4
from app.models.cis.mapping.master.court_cis import Court_CIS1, Court_CIS2, Court_CIS3, Court_CIS4

CIS_MODELS = {
    'cis_db_1': {
        'state': State_CIS1,
        'district_t': District_CIS1,
        'court_name': Court_CIS1,
        'case_type_t': CaseType_CIS1,
        'judge_name_t': JudgeName_CIS1,
        'desg_t': Designation_CIS1,
        'judge_t': JudgeCourt_CIS1,
        'civil_t': CivilT_CIS1,
        'purpose_t': PurposeT_CIS1,
        'daily_proc': DailyProc_CIS1
    },
    'cis_db_2': {
        'state': State_CIS2,
        'district_t': District_CIS2,
        'court_name': Court_CIS2,
        'case_type_t': CaseType_CIS2,
        'judge_name_t': JudgeName_CIS2,
        'desg_t': Designation_CIS2,
        'judge_t': JudgeCourt_CIS2,
        'civil_t': CivilT_CIS2,
        'purpose_t': PurposeT_CIS2,
        'daily_proc': DailyProc_CIS2
    },
    'cis_db_3': {
        'state': State_CIS3,
        'district_t': District_CIS3,
        'court_name': Court_CIS3,
        'case_type_t': CaseType_CIS3,
        'judge_name_t': JudgeName_CIS3,
        'desg_t': Designation_CIS3,
        'judge_t': JudgeCourt_CIS3,
        'civil_t': CivilT_CIS3,
        'purpose_t': PurposeT_CIS3,
        'daily_proc': DailyProc_CIS3
    },
    'cis_db_4': {
        'state': State_CIS4,
        'district_t': District_CIS4,
        'court_name': Court_CIS4,
        'case_type_t': CaseType_CIS4,
        'judge_name_t': JudgeName_CIS4,
        'desg_t': Designation_CIS4,
        'judge_t': JudgeCourt_CIS4,
        'civil_t': CivilT_CIS4,
        'purpose_t': PurposeT_CIS4,
        'daily_proc': DailyProc_CIS4
    }
}


def get_cis_model(db_key: str, table: str):
    return CIS_MODELS[db_key][table]