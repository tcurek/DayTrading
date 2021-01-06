from os import listdir, getcwd
from os.path import isfile, join
from datetime import datetime
from datetime import timedelta
from typing import TextIO
from stock import Stock


def _parse_file_Name(file_name: str) -> (str, str, str, str):
    rd_index = file_name.find("202")
    left_underscore_index = file_name.find("_")
    right_underscore_index = file_name.find("_", left_underscore_index+1)

    symbol = file_name[:rd_index]
    run_date = file_name[rd_index:left_underscore_index]
    version = file_name[left_underscore_index+1:right_underscore_index]
    file_type = file_name[right_underscore_index + 1:-4]

    return symbol, run_date, version, file_type


def format_file(reader: TextIO) -> [datetime, str, str, str]:
    lines = reader.readlines()
    table = [x.split(' ') for x in lines]
    result = []
    for row in table:
        if row[2] == 'nan' or row[0] == '0.0':
            continue
        for x in range(3):
            result.append([datetime.strptime(row[0], "%Y-%m-%d") + timedelta(x+1), row[1], row[2+x], row[5+x]])

    return result


def todays_data(file_type: str) -> dict:
    path = f"{getcwd()}/Models"
    dirs = listdir(path)
    result = {}
    for f in dirs:
        if not isfile(join(path, f)) or file_type not in f:
            continue

        file_data = format_file(open(join(path, f)))
        todays_file_data = list(filter(lambda x: x[0].date() == datetime.today().date(), file_data))

        if len(todays_file_data) == 0:
            continue

        for t in todays_file_data:
            result[t[1]] = (float(t[2]), float(t[3]))

        return result

    return result


def get_todays_projections() -> [Stock]:
    result = []
    buy_projections = todays_data('_buy_pred')
    for key in buy_projections:
        result.append(Stock(
            symbol=key,
            buy_prediction=buy_projections[key][0],
            buy_std_dev=buy_projections[key][1]
        ))
    return result
