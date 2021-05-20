
__north_main__ = ['10205', '10201', '10204']
__north_area1__ = ['10205']
__north_area2__ = ['10204', '10203']
__north_area3__ = ['10201']
__north_area4__ = ['10405', '10501']

__center_main__ = ['20201','20502','20101']
__center_area1__ = ['10501','20101','10601']
__center_area2__ = ['20202','20101']
__center_area3__ = ['20509','20503','20202']

def convert_data_for_taiwan_dashboart(data:dict)->dict:
    status = {}
    north = {
        'main': [data[id] for id in __north_main__],
        'area': {
            'area1': [data[id] for id in __north_area1__],
            'area2': [data[id] for id in __north_area2__],
            'area3': [data[id] for id in __north_area3__],
            'area4': [data[id] for id in __north_area4__],
        },
    }
    status['north'] = north

    center = {
        'main': [data[id] for id in __center_main__],
        'area': {
            'area1': [data[id] for id in __center_area1__],
            'area2': [data[id] for id in __center_area2__],
            'area3': [data[id] for id in __center_area3__],
        },
    }
    status['center'] = center

    return {'status': status}
