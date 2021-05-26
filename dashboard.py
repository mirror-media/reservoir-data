from pytz import timezone
from utils import now_with_timezone

__dashboard_data_set__ = {
    'status': {
        'north': {
            'main': ['10205', '10201', '10204'],
            'hydropower': [],
            'area': {
                '基隆北海岸': ['10204', '10203'],
                '大臺北': ['10205'],
                '板新及桃園': ['10201'],
                '新竹': ['10405'],
            },
        },
        'center': {
            'main': ['20201', '20502', '20101'],
            'hydropower': ['20201', '20502'],
            'area': {
                '苗栗': ['10501', '10601'],
                '臺中': ['20101', '20202'],
                '彰雲投': ['20509', '20503'],
            },
        },
        'south': {
            'main': ['30502', '30503', '30501'],
            'hydropower': [],
            'area': {
                '嘉義': ['30301', '30302'],
                '臺南': ['30502', '30501', '30503'],
                '高雄': ['30803', '30901'],
                '屏東': ['31201'],
            },
        },
    },
}

__additional_tags__ = {
    '苗栗': {
        '10501': '支援新竹',
    },
    '臺中': {
        '20101': '支援苗栗',
        '20202': '支援彰雲投',
    },
    '彰雲投': {
        '30502': '支援嘉義',
        '30501': '支援嘉義',
        '30503': '支援高雄',
    },
}


def convert_according_to_data_set(data, key, data_set):
    if type(data_set) == list:
        for id in range(len(data_set)):
            data_set[id] = data[data_set[id]
                                ] | additional_tag(key, data_set[id])
    elif type(data_set) == dict:
        for k in data_set.keys():
            convert_according_to_data_set(data, k, data_set[k])


def additional_tag(key: str, id: str) -> dict:
    return {'additionalTag': {'data': __additional_tags__.get(key, {}).get(id, ''), 'updateTime': now_with_timezone(timezone('Asia/Taipei')).isoformat(timespec='seconds')}}


def convert_data_for_taiwan_dashboart(data: dict) -> dict:
    for key in __dashboard_data_set__.keys():
        convert_according_to_data_set(data, key, __dashboard_data_set__[key])

    return __dashboard_data_set__
