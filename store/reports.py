
import json
from store.models import Store, Report
from store.time import compute_uptime
from store.database import db
from datetime import datetime
from store.models import Report
from datetime import datetime


def generate_report(report_id):
    report = Report(report_id=report_id, status='Running', data='')
    db.session.add(report)
    db.session.commit()

    report_data = []
    stores = Store.query.all()
    for store in stores:
        uptime, downtime = compute_uptime(store.id)
        report_data.append({
            'store_id': store.id,
            'status': store.status,
            'uptime': round(uptime, 2),
            'downtime': round(downtime, 2)
        })

    report.status = 'Complete'
    report.completed_at = datetime.utcnow()

    report.data = json.dumps(report_data)

    db.session.commit()

    return report


def get_report_status_from_db(report_id):
    report = Report.query.filter_by(report_id=report_id).first()
    if report is None:
        return None
    else:
        return report.status

def get_report_data_from_db(report_id):
    """
    Retrieves the report data from the database for a given report_id.
    """
    report = Report.query.filter_by(report_id=report_id).first()

    if report is None:
        raise ValueError(f"No report found for report_id: {report_id}")

    return report.data