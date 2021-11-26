from http import HTTPStatus

from src.data_access.ConnectionDataBase import ConnectionDataBase
from src.model.Player import Player


class Report:
    def __init__(self):
        self.informer = None
        self.informed = None
        self.reason = None
        self.comment = None

    def make_json_get_reports_by_player(self) -> dict:
        return {
            "reason": self.reason,
            "informer": self.informer,
            "comment": self.comment
        }

    def instanciate(self, info: dict) -> bool:
        instanciated = False
        player_informer = Player()
        player_informed = Player()
        player_informer.nickname = info["informer"]
        player_informed.nickname = info["informed"]
        reason = info["reason"]
        if player_informed.get_id_by_nickname() != -1 and player_informer.get_id_by_nickname() != -1 and Report.exist_reason(
                reason):
            self.informer = player_informer.player_id
            self.informed = player_informed.player_id
            self.reason = int(info["reason"])
            self.comment = str(info["comment"])
            instanciated = True
        return instanciated

    @staticmethod
    def exist_reason(reason: int) -> bool:
        query = "SELECT * FROM reason WHERE id_reason = %s;"
        values = [reason]
        result = ConnectionDataBase.select(query, values)
        return len(result) > 0

    def report_exist(self) -> bool:
        query = "SELECT reason FROM report WHERE informed = %s AND informer = %s;"
        values = [self.informed, self.informer]
        result = ConnectionDataBase.select(query, values)
        return len(result) > 0

    @staticmethod
    def validate_info(info: dict) -> bool:
        informer = str(info["informer"])
        informed = str(info["informed"])
        reason = str(info["reason"])
        comment = str(info["comment"])
        return reason.isdigit() and informer != informed and 0 < len(comment) <= 50

    def add(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if not self.report_exist() and self.increase_reports_player():
            query = "INSERT into report (informed, informer, reason, comment) VALUES (%s, %s, %s, %s);"
            values = [self.informed, self.informer, self.reason, self.comment]
            if ConnectionDataBase.send_query(query, values):
                status = HTTPStatus.CREATED
        else:
            status = HTTPStatus.CONFLICT
        return status

    def increase_reports_player(self) -> bool:
        query = "UPDATE player SET reports = reports +1 WHERE player_id = %s"
        values = [self.informed]
        flag = ConnectionDataBase.send_query(query, values)
        return flag

    @staticmethod
    def get_players_reported(page: int):
        page = page * 10
        players = []
        query = "SELECT nickname, reports FROM player WHERE reports > 0  and player.status = 1 ORDER BY reports" \
                " DESC LIMIT %s, 10;"
        values = [page]
        result = ConnectionDataBase.select(query, values)
        if result:
            for individual_player in result:
                player_aux = Player()
                player_aux.nickname = individual_player["nickname"]
                player_aux.reports = individual_player["reports"]
                players.append(player_aux.make_json_players_reports())
        return players

    @staticmethod
    def get_reports_by_player(nickname):
        reports = []
        player = Player()
        player.nickname = nickname
        player.get_id_by_nickname()
        if player.player_id != -1:
            query = "SELECT r.reason, p.nickname as informer, comment FROM report INNER JOIN reason r INNER JOIN " \
                    "player p on" \
                    " report.informer = p.player_id WHERE informed = %s and r.id_reason = report.reason;"
            values = [player.player_id]
            result = ConnectionDataBase.select(query, values)
            if result:
                for individual_report in result:
                    report = Report()
                    report.reason = individual_report["reason"]
                    report.informer = individual_report["informer"]
                    report.comment = individual_report["comment"]
                    reports.append(report.make_json_get_reports_by_player())

        return reports

