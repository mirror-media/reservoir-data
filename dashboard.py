__north_main__ = ['10205', '10201', '10204']
__north_hydropower__ = []
__north_area1__ = ['10204', '10203']
__north_area2__ = ['10205']
__north_area3__ = ['10201']
__north_area4__ = ['10405']

__center_main__ = ['20201', '20502', '20101']
__center_hydropower__ = ['20201', '20502']
__center_area1__ = ['10501', '10601']
__center_area2__ = ['20101', '20202']
__center_area3__ = ['20509', '20503']

__south_main__ = ['30502', '30503', '30501']
__south_hydropower__ = []
__south_area1__ = ['30301', '30302']
__south_area2__ = ['30502', '30501', '30503']
__south_area3__ = ['30803', '30901']
__south_area4__ = ['31201']


def convert_data_for_taiwan_dashboart(data: dict) -> dict:
    status = {}
    north = {
        'main': [data[id] for id in __north_main__],
        'hydropower': [data[id] for id in __north_hydropower__],
        'area': {
            '基隆北海岸': [data[id] for id in __north_area1__],
            '大臺北': [data[id] for id in __north_area2__],
            '板新及桃園': [data[id] for id in __north_area3__],
            '新竹': [data[id] for id in __north_area4__],
        },
    }
    status['北部'] = north

    center = {
        'main': [data[id] for id in __center_main__],
        'hydropower': [data[id] for id in __center_hydropower__],
        'area': {
            '苗栗': [data[id] for id in __center_area1__],
            '臺中': [data[id] for id in __center_area2__],
            '彰雲投': [data[id] for id in __center_area3__],
        },
    }
    status['中部'] = center

    south = {
        'main': [data[id] for id in __south_main__],
        'hydropower': [data[id] for id in __south_hydropower__],
        'area': {
            '嘉義': [data[id] for id in __south_area1__],
            '臺南': [data[id] for id in __south_area2__],
            '高雄': [data[id] for id in __south_area3__],
            '屏東': [data[id] for id in __south_area4__],
        },
    }
    status['南部'] = south

    return {'status': status}
