
__north_main__ = ['10205', '10201', '10204']
__north_area1__ = ['10204', '10203']
__north_area2__ = ['10201']
__north_area3__ = ['10405', '10501']

def convert_data_for_taiwan_dashboart(data:dict)->dict:
    status = {}
    north = {
        'main': [data[id] for id in __north_main__],
        'area1': [data[id] for id in __north_area1__],
        'area2': [data[id] for id in __north_area2__],
        'area3': [data[id] for id in __north_area3__],
    }
    status['north'] = north

    return {'status': status}
