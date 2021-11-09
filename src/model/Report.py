from http import HTTPStatus

from src.data_access.ConnectionDataBase import ConnectionDataBase
from src.model.Player import Player


class Report:
    def __init__(self):
        self.informer = None
        self.informed = None
        self.reason = None
        self.comment = None

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
        if not self.report_exist():
            query = "INSERT into report (informed, informer, reason, comment) VALUES (%s, %s, %s, %s);"
            values = [self.informed, self.informer, self.reason, self.comment]
            if ConnectionDataBase.send_query(query, values):
                status = HTTPStatus.CREATED
        else:
            status = HTTPStatus.CONFLICT
        return status
