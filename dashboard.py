from pytz import timezone
from utils import now_with_timezone

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

__additional_tags__ = {
    'center_area1': {
        '10501': '支援新竹',
    },
    'center_area2': {
        '20101': '支援苗栗',
        '20202': '支援彰雲投',
    },
    'south_area2': {
        '30502': '支援嘉義',
        '30501': '支援嘉義',
        '30503': '支援高雄',
    },
}


def additional_tag(key: str, id: str) -> dict:
    return {'additionalTag': {'data': __additional_tags__.get(key, {}).get(id, ''), 'updateTime': now_with_timezone(timezone('Asia/Taipei')).isoformat(timespec='seconds')}}


def convert_data_for_taiwan_dashboart(data: dict) -> dict:
    status = {}
    north = {
        'main': [data[id] | additional_tag('north_main', id) for id in __north_main__],
        'hydropower': [data[id] | additional_tag('north_hydropower', id) for id in __north_hydropower__],
        'area': {
            '基隆北海岸': [data[id] | additional_tag('north_area1', id) for id in __north_area1__],
            '大臺北': [data[id] | additional_tag('north_area2', id) for id in __north_area2__],
            '板新及桃園': [data[id] | additional_tag('north_area3', id) for id in __north_area3__],
            '新竹': [data[id] | additional_tag('north_area4', id) for id in __north_area4__],
        },
    }
    status['北部'] = north

    center = {
        'main': [data[id] | additional_tag('center_main', id) for id in __center_main__],
        'hydropower': [data[id] | additional_tag('center_hydropower', id) for id in __center_hydropower__],
        'area': {
            '苗栗': [data[id] | additional_tag('center_area1', id) for id in __center_area1__],
            '臺中': [data[id] | additional_tag('center_area2', id) for id in __center_area2__],
            '彰雲投': [data[id] | additional_tag('center_area3', id) for id in __center_area3__],
        },
    }
    status['中部'] = center

    south = {
        'main': [data[id] | additional_tag('south_main', id) for id in __south_main__],
        'hydropower': [data[id] | additional_tag('south_hydropower', id) for id in __south_hydropower__],
        'area': {
            '嘉義': [data[id] | additional_tag('south_area1', id) for id in __south_area1__],
            '臺南': [data[id] | additional_tag('south_area2', id) for id in __south_area2__],
            '高雄': [data[id] | additional_tag('south_area3', id) for id in __south_area3__],
            '屏東': [data[id] | additional_tag('south_area4', id) for id in __south_area4__],
        },
    }
    status['南部'] = south

    return {'status': status}
