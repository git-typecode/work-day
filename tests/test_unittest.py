from datetime import datetime, timedelta

from work_day.main import calc_flex, calc_working_hours

# from main import check_work_day
# from WorkLogWriter import read_log


# def test_load_workday_from_file():
#     assert type(str)


# def test_date_of_latest_workday():
#     check_work_day()


# def test_should_create_logdir_and_logfile():
#    create_log()


def test_flex_time_calculation():

    assert calc_flex(8, 8) == 0
    assert calc_flex(9, 8) == 1
    assert calc_flex(7, 8) == -1


def test_calc_of_working_hours():
    start = datetime.now()
    stop = datetime.now() + timedelta(hours=8)

    assert calc_working_hours(start, stop) == 8.0
