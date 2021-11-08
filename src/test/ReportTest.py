from src.model.Report import Report
id_informer = 0
id_informed = 0
info = {
    "informer": "rendon.luisgerardo@gmail.com",
    "informed": "rendon.luisgerardo@gmail.com",
    "reason": "1"
}


def test_validate_informer_equals_informed():
    assert not Report.validate_info(info)


def test_validate_reason_decimal():
    info["reason"] = "2.5"
    assert not Report.validate_info(info)


def test_validate_reason_word():
    info["reason"] = "hola"
    assert not Report.validate_info(info)

def test_report_doesnt_exist():
    report = Report()
    report.informer =""
    report.informed = ""

