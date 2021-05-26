from pytz import timezone
from utils import now_with_timezone


__additional_tag_for_area_reservoirs__ = {
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
    '中部': {
        '20201': '主要供發電',
        '20502': '主要供發電',
    }
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
    return {'additionalTag': {'data': __additional_tag_for_area_reservoirs__.get(key, {}).get(id, ''), 'updateTime': now_with_timezone(timezone('Asia/Taipei')).isoformat(timespec='seconds')}}


def convert_data_for_taiwan_dashboart(data: dict) -> dict:

    dashboard_data_set = {
        'status': {
            '北部': {
                'main': ['10205', '10201', '10204'],
                # 'hydropower': [],
                'area': {
                    '基隆北海岸': ['10204', '10203'],
                    '大臺北': ['10205'],
                    '板新及桃園': ['10201'],
                    '新竹': ['10405'],
                },
            },
            '中部': {
                'main': ['20201', '20502', '20101'],
                # 'hydropower': ['20201', '20502'],
                'area': {
                    '苗栗': ['10501', '10601'],
                    '臺中': ['20101', '20202'],
                    '彰雲投': ['20509', '20503'],
                    '中部': ['20201', '20502'],
                },
            },
            '南部': {
                'main': ['30502', '30503', '30501'],
                # 'hydropower': [],
                'area': {
                    '嘉義': ['30301', '30302'],
                    '臺南': ['30502', '30501', '30503'],
                    '高雄': ['30803', '30901'],
                    '屏東': ['31201'],
                },
            },
        },
    }

    for key in dashboard_data_set.keys():
        convert_according_to_data_set(data, key, dashboard_data_set[key])

    return dashboard_data_set
