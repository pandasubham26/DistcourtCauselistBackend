import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
import pandas as pd
from flask import Blueprint, request, current_app, send_file
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.utils import secure_filename

from app.estcode_db import get_cis_db_key
from app.extensions import db
from app.models.casefile.casefile_uploads import CaseFileHeader, CaseFileDetail
from app.models.casefile.civil_t import CivilT
from app.models.cis.registry import get_cis_model
from app.models.master.case_type_t import CaseTypeT
from app.models.master.judge import Judge_Name
from app.schemas.casefile_upload_schema import casefile_upload_schema
from app.utils import error_response, success_response

bulkupload_casefile_bp = Blueprint('bulkupload_casefile_bp', __name__)

ALLOWED_ZIP_EXTENSIONS = {".zip"}
ALLOWED_EXCEL_EXTENSIONS = {".xls", ".xlsx"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}

def generate_bulk_no(estcode):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{estcode}-{timestamp}"


@bulkupload_casefile_bp.route('/up/uploadcasefilebycsvorexcel', methods=['POST'])
def upload_casefile_by_csv_or_excel(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        request_data = request.get_json()
        payload = request_data.get("payload")
        records = payload.get("records")
        uploaded_by = payload.get("uploaded_by")
        judge = payload.get("judge")

        if not records or not isinstance(records, list):
            return error_response(error='invalid_date', message='Invalid data format', status=400)

        query = db.session.query(Judge_Name).filter_by(judge_name=judge).first()
        if query:
            estcode = query.est_code_src
        else:
            return error_response(error='invalid_est', message='Invalid est code for the records', status=404)

        bulk_no = generate_bulk_no(estcode)

        for row in records:
            # Check if main case record already exists
            existing_case = CaseFileHeader.query.filter_by(
                cis_case_type=row.get("cis_case_type"),
                cis_case_no=row.get("cis_case_no"),
                cis_case_year=row.get("cis_case_year"),
                est_code=estcode
            ).first()

            # If main case does not exist → Create main entry
            if not existing_case:
                existing_case = CaseFileHeader(
                    court=row.get("court_name"),
                    judge=judge,
                    barcode=row.get("barcode"),
                    cis_case_type=row.get("cis_case_type"),
                    cis_case_no=row.get("cis_case_no"),
                    cis_case_year=row.get("cis_case_year"),
                    reg_case_type=row.get("reg_case_type"),
                    reg_case_no=row.get("reg_case_no"),
                    reg_case_year=row.get("reg_case_year"),
                    est_code=estcode,
                    uploaded_by=uploaded_by
                )
                db.session.add(existing_case)
                db.session.flush()

            # Always insert detail file record
            detail_record = CaseFileDetail(
                casefile_id=existing_case.id,
                bulk_no=bulk_no,
                file_path=row.get("file_path"),  # Must come from CSV/Excel
                pages=row.get("page_count") or 0,
                uploaded_by=uploaded_by
            )
            db.session.add(detail_record)

            target_folder = os.path.join("app",
                                         "static",
                                         "pdf",
                                         str(row.get("cis_case_year")),
                                         str(row.get("court_name"))
                                         )
            os.makedirs(target_folder, exist_ok=True)

        db.session.commit()

        return success_response(status=200, message=f"Bulk upload data saved successfully and Bundle generate"
                                                    f"with a special unique code {bulk_no}", data=None)

    except Exception as e:
        current_app.logger.exception('Error fetching user list')
        return error_response('server_error', f'An unexpected error occurred in {e}', status=500)


@bulkupload_casefile_bp.route('/up/getcasefilelist', methods=['GET'])
@jwt_required()
def get_casefile_list(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )
        
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'name').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'id', 'barcode', 'cis_case_type', 'reg_case_type', 'cis_case_no', 'reg_case_no',
                             'cis_case_year', 'reg_case_year'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'barcode'

        # Fetch all users
        query = CaseFileHeader.query.filter(CaseFileHeader.display == 'Y')

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(CaseFileHeader.barcode).contains(search),
                    db.func.lower(CaseFileHeader.cis_case_type).contains(search),
                    db.func.lower(CaseFileHeader.reg_case_type).contains(search),
                    db.func.lower(db.cast(CaseFileHeader.cis_case_no, db.String)).contains(search),
                    db.func.lower(db.cast(CaseFileHeader.reg_case_no, db.String)).contains(search),
                    db.func.lower(db.cast(CaseFileHeader.cis_case_year, db.String)).contains(search),
                    db.func.lower(db.cast(CaseFileHeader.reg_case_year, db.String)).contains(search)
                )
            )

        sort_column = getattr(CaseFileHeader, sort_key, CaseFileHeader.barcode)
        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        total = query.count()
        pages = (total + page_size - 1) // page_size
        casefile = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no users found
        if not casefile:
            return error_response(
                details={
                    'casefile': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_casefile',
                message='No case-file found',
                status=404
            )

        casefile_list = casefile_upload_schema.dump(casefile, many=True)
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'casefile': casefile_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': (total + page_size - 1)
                }
            },
            message='case file fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching user list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@bulkupload_casefile_bp.route('/up/updatecasefiledetails', methods=['PUT'])
@jwt_required()
def put_casefile_list():
    try:
        request_data = request.get_json()

        if not request_data:
            return error_response(error='invalid_request', message='Request data missing', status=400)

        barcode = request_data.get('barcode')

        if not barcode:
            return error_response(error='invalid_barcode', message='Invalid barcode selected', status=400)

        existing_case = CaseFileHeader.query.filter_by(barcode=barcode).first()

        if not existing_case:
            return error_response(error='not_found', message='Case not found for the selected barcode', status=404)

        cis_case_type = CaseTypeT.query.filter_by(type_name=existing_case.cis_case_type).first()

        if not cis_case_type:
            return error_response(error='not_found', message='Case type not found in CIS mapping table',
                                  status=404)

        cis_civil_case = CivilT.query.filter_by(
            regcase_type=cis_case_type.case_type,
            reg_no=existing_case.cis_case_no,
            reg_year=existing_case.cis_case_year
        ).first()

        if not cis_civil_case:
            return error_response(error='not_found', message='Case not found in CIS Civil Records',
                                  status=404)

        existing_case.cino = cis_civil_case.cino or existing_case.cino
        existing_case.pet_name = cis_civil_case.pet_name or existing_case.pet_name
        existing_case.pet_adv = cis_civil_case.pet_adv or existing_case.pet_adv
        existing_case.res_name = cis_civil_case.res_name or existing_case.res_name
        existing_case.res_adv = cis_civil_case.res_adv or existing_case.res_adv

        db.session.commit()

        return success_response(message='Case updated successfully', status=200, data={
            "barcode": existing_case.barcode
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception('Error fetching case details')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@bulkupload_casefile_bp.route('/up/getcasefilepdf', methods=['GET'])
@jwt_required()
def get_case_file_pdf(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )
        casetype = request.args.get('casetype')
        caseno = request.args.get('caseno', type=int)
        caseyear = request.args.get('caseyear', type=int)

        if not casetype or not caseno or not caseyear:
            return error_response('invalid_request', 'Missing required query parameters', 400)

        header = CaseFileHeader.query.filter_by(
            reg_case_type=casetype,
            reg_case_no=caseno,
            reg_case_year=caseyear,
            display='Y'
        ).first()

        if not header:
            return error_response('not_found', 'Case record not found', 404)

        detail = CaseFileDetail.query.filter_by(casefile_id=header.id).order_by(
            CaseFileDetail.uploaded_at.desc()
        ).first()

        if not detail:
            return error_response('no_file', 'No PDF file uploaded for this case', 404)

        # === IMPORTANT FIX: Use absolute base path ===
        project_root = current_app.root_path

        # Create target folder structure
        target_folder = os.path.join("static", "casefiles", header.court, str(caseyear))

        # Original uploaded PDF path (stored absolute in DB)
        original_pdf_path = os.path.join(project_root, target_folder, detail.file_path.lstrip("/"))

        if not os.path.exists(original_pdf_path):
            return error_response("file_missing", f"Original PDF missing: {original_pdf_path}", 404)

        # Return PDF file to Angular
        return send_file(original_pdf_path, mimetype='application/pdf')

    except Exception as e:
        current_app.logger.exception("Error while fetching case PDF")
        return error_response('server_error', f'Unexpected server error: {e}', 500)


@bulkupload_casefile_bp.route('/up/getcasefiledetails', methods=['GET'])
@jwt_required()
def get_case_file_details(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        casetype = request.args.get('casetype')
        caseno = request.args.get('caseno', type=int)
        caseyear = request.args.get('caseyear', type=int)

        if not casetype or not caseno or not caseyear:
            return error_response('invalid_request', 'Missing required query parameters', 400)

        header = CaseFileHeader.query.filter_by(
            reg_case_type=casetype,
            reg_case_no=caseno,
            reg_case_year=caseyear,
            display='Y'
        ).first()

        if not header:
            return error_response('not_found', 'Case record not found', 404)

        casefile_list = casefile_upload_schema.dump(header)
        # Serialize with schema (many=True for lists)
        return success_response(
            data=casefile_list,
            message='case file fetched successfully',
            status=200
        )

    except Exception as e:
        current_app.logger.exception("Error while fetching case PDF")
        return error_response('server_error', f'Unexpected server error: {e}', 500)


@bulkupload_casefile_bp.route("/up/uploadcasefilebyzip", methods=["POST"])
def upload_zip(estcode):

    if "file" not in request.files:
        return error_response("not_found", "no file part", 404)
    
    db_key = get_cis_db_key(estcode)
    Judge_Name = get_cis_model(db_key, 'judge_name_t')

    file = request.files["file"]
    user = request.form.get("uploaded_by")
    judge = request.form.get("judge")
    if file.filename == "":
        return error_response("not_found", "no selected file", 400)

    if not judge or not user:
        return error_response("not_found", "no user and judge connected to the files", 400)

    judge_row = db.session.query(Judge_Name).filter_by(judge_name=judge).first()
    if not judge_row:
        return error_response("invalid_judge", "Judge not found", 404)

    bulk_no = generate_bulk_no(estcode)

    filename = secure_filename(file.filename)
    if Path(filename).suffix.lower() != ".zip":
        return error_response("invalid", "only .zip allowed", 400)

    project_root = current_app.root_path
    target_base = os.path.join(project_root, "static", "zip")
    unique_folder = datetime.now().strftime("%Y%m%d")
    upload_folder = os.path.join(target_base, unique_folder)
    os.makedirs(upload_folder, exist_ok=True)

    # Path for saving uploaded ZIP
    zip_path = os.path.join(upload_folder, filename)

    try:
        file.save(zip_path)
    except Exception as e:
        shutil.rmtree(upload_folder, ignore_errors=True)
        return error_response(
            "error",
            f"failed to save uploaded file: {str(e)}",
            500
        )

    extract_dir = os.path.join(upload_folder, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    excel_file_path = None
    pdf_files = []

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                if member.endswith("/"):
                    continue

                p = Path(member)
                target_path = Path(extract_dir) / p
                target_path.parent.mkdir(parents=True, exist_ok=True)

                if not str(target_path.resolve()).startswith(str(Path(extract_dir).resolve())):
                    return error_response("error", f"unsafe file detected {member}", 400)

                with zf.open(member) as src, open(target_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                if p.suffix.lower() in [".xls", ".xlsx"]:
                    if p.name.lower().startswith("upload"):
                        excel_file_path = str(target_path)

                if p.suffix.lower() == ".pdf":
                    pdf_files.append(str(target_path))

        if not excel_file_path:
            return error_response("not_found", "Excel file named upload.xlsx not found", 400)
        if not pdf_files:
            return error_response("not_found", "No PDF files found", 400)

        ext = Path(excel_file_path).suffix.lower()
        try:
            if ext == ".xls":
                df = pd.read_excel(excel_file_path, engine="xlrd")
            else:
                df = pd.read_excel(excel_file_path, engine="openpyxl")
        except Exception as e:
            return error_response("invalid_excel", f"Failed to read Excel: {str(e)}", 400)

        required_cols = ["BARCODE", "CIS CASE TYPE", "CIS CASE NUMBER", "CIS CASE YEAR",
                         "REG CASE TYPE", "REG CASE NUMBER", "REG CASE YEAR",
                         "PAGE COUNT", "COURT NAME", "FILE PATH",
                        ]

        for col in required_cols:
            if col not in df.columns:
                return error_response("invalid", f"Excel missing required column: {col}", 400)

        df = df.fillna("")
        df["REG CASE YEAR"] = df["REG CASE YEAR"].astype(str).str.strip()
        df["COURT NAME"] = df["COURT NAME"].astype(str).str.strip()
        df["FILE PATH"] = df["FILE PATH"].astype(str).str.strip()

        move_summary = []
        insert_count = 0

        for _, row in df.iterrows():
            barcode = row["BARCODE"]
            cis_case_type = row["CIS CASE TYPE"]
            cis_case_no = row["CIS CASE NUMBER"]
            cis_case_year = row["CIS CASE YEAR"]
            reg_case_type = row["REG CASE TYPE"]
            reg_case_no = row["REG CASE NUMBER"]
            reg_case_year = row["REG CASE YEAR"]
            page = row["PAGE COUNT"]
            court = row["COURT NAME"]
            pdfname = row["FILE PATH"]

            match_pdf = next((pdf for pdf in pdf_files if Path(pdf).name.lower() == pdfname.lower()), None)

            if not match_pdf:
                move_summary.append({"pdf": pdfname, "status": "NOT FOUND"})
                continue

            header = CaseFileHeader.query.filter_by(
                cis_case_type=cis_case_type,
                cis_case_no=cis_case_no,
                cis_case_year=cis_case_year,
                est_code=estcode
            ).first()

            if not header:
                header = CaseFileHeader(
                    court=court,
                    judge=judge,
                    barcode=barcode,
                    cis_case_type=cis_case_type,
                    cis_case_no=cis_case_no,
                    cis_case_year=cis_case_year,
                    reg_case_type=reg_case_type,
                    reg_case_no=reg_case_no,
                    reg_case_year=reg_case_year,
                    est_code=estcode,
                    uploaded_by=user
                )
                db.session.add(header)
                db.session.flush()

            dest_dir = os.path.join(project_root, "static", "casefiles", court, reg_case_year)
            os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, pdfname)

            shutil.copy(match_pdf, dest_path)

            detail = CaseFileDetail(
                casefile_id=header.id,
                bulk_no=bulk_no,
                file_path=pdfname,
                pages=page,
                uploaded_by=user
            )
            db.session.add(detail)
            insert_count += 1

            move_summary.append({"pdf": pdfname, "stored_to": dest_path, "status": "OK"})
        db.session.commit()
        return success_response(
            'success',
            f'ZIP processed successfully. {insert_count} records saved. BULK NO: {bulk_no}',
            200
        )

    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)


@bulkupload_casefile_bp.route('/up/updatecasefiledetailsall', methods=['PUT'])
@jwt_required()
def put_casefile_list_all(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )
        request_data = request.get_json()

        if not request_data:
            return error_response(error='invalid_request', message='Request data missing', status=400)

        barcode = request_data.get('barcode')

        if not barcode:
            return error_response(error='invalid_barcode', message='Invalid barcode selected', status=400)

        for r in barcode:
            existing_case = CaseFileHeader.query.filter_by(barcode=r).first()

            if not existing_case:
                return error_response(error='not_found', message='Case not found for the selected barcode', status=404)

            db_key = get_cis_db_key(estcode)
            CaseTypeT = get_cis_model(db_key, 'case_type_t')
            CivilT = get_cis_model(db_key, 'civil_t')

            cis_case_type = CaseTypeT.query.filter_by(type_name=existing_case.cis_case_type).first()

            if not cis_case_type:
                return error_response(error='not_found', message='Case type not found in CIS mapping table',
                                      status=404)

            cis_civil_case = CivilT.query.filter_by(
                regcase_type=cis_case_type.case_type,
                reg_no=existing_case.cis_case_no,
                reg_year=existing_case.cis_case_year
            ).first()

            if not cis_civil_case:
                return error_response(error='not_found', message='Case not found in CIS Civil Records',
                                      status=404)

            existing_case.cino = cis_civil_case.cino or existing_case.cino
            existing_case.pet_name = cis_civil_case.pet_name or existing_case.pet_name
            existing_case.pet_adv = cis_civil_case.pet_adv or existing_case.pet_adv
            existing_case.res_name = cis_civil_case.res_name or existing_case.res_name
            existing_case.res_adv = cis_civil_case.res_adv or existing_case.res_adv

        db.session.commit()

        return success_response(message='Case updated successfully', status=200)
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception('Error fetching case details')
        return error_response('server_error', 'An unexpected error occurred', status=500)