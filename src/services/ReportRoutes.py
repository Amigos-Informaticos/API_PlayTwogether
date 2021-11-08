from http import HTTPStatus

from flask import Blueprint, request, Response

from src.model.Report import Report

report_routes = Blueprint("report_routes", __name__)


@report_routes.route("/player/report", methods=["POST"])
def add():
    status_response = HTTPStatus.BAD_REQUEST
    report_json = request.json
    values_required = {"informed", "informer", "reason"}
    report = Report()
    if report_json is not None and all(key in report_json for key in values_required) and \
            Report.validate_info(report_json) and report.instanciate(report_json):
            status_response = report.add()

    return Response(status=status_response)
