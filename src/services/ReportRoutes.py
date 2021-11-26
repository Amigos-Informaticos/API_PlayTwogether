import json
from http import HTTPStatus
from sqlite3 import DatabaseError, InterfaceError

from flask import Blueprint, request, Response

from src.model.Report import Report
from src.services.Auth import Auth

report_routes = Blueprint("report_routes", __name__)


@report_routes.route("/player/report", methods=["POST"])
@Auth.requires_authentication()
def add():
    status_response = HTTPStatus.BAD_REQUEST
    response = Response(status=status_response)
    report_json = request.json
    values_required = {"informed", "informer", "reason", "comment", "email"}
    report = Report()
    try:
        if report_json is not None and all(key in report_json for key in values_required) and \
                Report.validate_info(report_json) and report.instanciate(report_json):
            status_response = report.add()
            response = Response(status=status_response)
    except (DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        print(e)

    return response


@report_routes.route("/report/players/<page>", methods=["GET"])
def get_players_more_reported(page):
    response = Response(status=HTTPStatus.NOT_FOUND)
    page_str = str(page)
    if page_str.isdigit():
        try:
            players_reported = Report.get_players_reported(page)
            if len(players_reported) > 0:
                players_json = json.dumps(players_reported)
                response = Response(players_json, status=HTTPStatus.OK, mimetype="application/json")
        except (DatabaseError, InterfaceError) as e:
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return response


@report_routes.route("/players/<nickname>/reports", methods=["GET"])
def get_reports_by_player(nickname):
    response = Response(status=HTTPStatus.NOT_FOUND)
    try:
        reports = Report.get_reports_by_player(nickname)
        if len(reports) > 0:
            reports_json = json.dumps(reports)
            response = Response(reports_json, status=HTTPStatus.OK, mimetype="application/json")
    except(DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return response
