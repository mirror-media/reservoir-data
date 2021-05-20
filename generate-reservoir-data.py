from datetime import datetime, timezone, timedelta
from google.cloud import storage
from pytz import timezone
import __main__
import gzip
import json
import requests
import dashboard

__taipei_tz__ = timezone('Asia/Taipei')

__api_time_format__ = '%Y-%m-%dT%H:%M:%S'


def get_daily_operational_statistics() -> dict:
    api = 'https://data.wra.gov.tw/Service/OpenData.aspx?format=json&id=50C8256D-30C5-4B8D-9B84-2E14D5C6DF71'

    r = requests.get(api)
    j = r.json()['DailyOperationalStatisticsOfReservoirs_OPENDATA']

    ids = set()
    for reservoir in j:
        ids.add(reservoir['ReservoirIdentifier'])

    return {id: max(filter(lambda r: r['ReservoirIdentifier'] == id, j), key=lambda r: datetime.strptime(r['RecordTime'], __api_time_format__)) for id in ids}


def get_reservoir_condition_data() -> dict:
    api = 'https://data.wra.gov.tw/Service/OpenData.aspx?format=json&id=1602CA19-B224-4CC3-AA31-11B1B124530F'

    r = requests.get(api)
    j = r.json()['ReservoirConditionData_OPENDATA']

    ids = set()
    for reservoir in j:
        ids.add(reservoir['ReservoirIdentifier'])

    return {id: max(filter(lambda r: r['ReservoirIdentifier'] == id, j), key=lambda r: datetime.strptime(r['ObservationTime'], __api_time_format__)) for id in ids}


def update_data(parent: dict, id: str, key: str, update_time: datetime, data):
    if id not in parent:
        parent[id] = {}
    if key not in parent[id]:

        parent[id][key] = {
            'updateTime': datetime(2, 1, 1, 0, 0, 0).astimezone().isoformat(),
        }
    if datetime.fromisoformat(update_time) > datetime.fromisoformat(parent[id][key]['updateTime']):
        parent[id][key] = {
            'data': data,
            'updateTime': update_time,
        }


def get_normalized_time(time: str) -> str:
    return __taipei_tz__.localize(datetime.strptime(
        time, __api_time_format__)).isoformat()


def get_observation_time(data: dict) -> str:
    return get_normalized_time(data['ObservationTime'])


def get_record_time(data: dict) -> str:
    return get_normalized_time(data['RecordTime'])


def calculate_effective_water_storage_storage_percentage(data: dict):
    for id in data:
        data[id]['effectiveWaterStorageStoragePercentage'] = {
            'data': '{:.2%}'.format(float(
                data[id]['effectiveWaterStorageCapacity']['data'])/float(data[id]['effectiveCapacity']['data'])) if data[id]['effectiveWaterStorageCapacity']['data'] != '' and data[id]['effectiveCapacity']['data'] != '' else '',
            'updateTime': data[id]['effectiveWaterStorageCapacity']['updateTime'],
        }


def add_reservoir_identifier(data: dict):
    for id in filter(lambda key: type(key) is str and key.isnumeric(), data.keys()):
        data[id]['reservoirIdentifier'] = {'data': id}


def upload_data(bucket_name: str, data: bytes, content_type: str, destination_blob_name: str, is_public: bool):
    '''Uploads a file to the bucket.'''
    # bucket_name = 'your-bucket-name'
    # data = 'storage-object-content'

    # Instantiates a client
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.content_encoding = 'gzip'

    print(
        '[%s] uploadling data to gs://%s/%s' % (__main__.__file__, bucket_name, destination_blob_name))

    blob.upload_from_string(
        data=gzip.compress(data=data, compresslevel=9), content_type=content_type, client=storage_client)
    blob.content_language = 'zh'
    blob.cache_control = 'max-age=60,public'
    if is_public:
        blob.make_public()
    blob.patch()

    print('[%s] finished uploading gs://%s/%s' %
          (__main__.__file__, bucket_name, destination_blob_name))


def now_with_timezone(tz: timezone) -> datetime:
    return datetime.now().astimezone().astimezone(tz)


def generate_data() -> dict:
    data = {}

    reservoir_condition = get_reservoir_condition_data()
    for id in reservoir_condition.keys():
        update_data(data, id, 'effectiveWaterStorageCapacity',
                    get_observation_time(reservoir_condition[id]), reservoir_condition[id]['EffectiveWaterStorageCapacity'])

    daily_operational_statistics = get_daily_operational_statistics()

    for id in reservoir_condition.keys():
        update_data(data, id, 'effectiveCapacity',
                    get_record_time(daily_operational_statistics.get(id, {'RecordTime': now_with_timezone(__taipei_tz__).strftime(__api_time_format__)})), daily_operational_statistics.get(id, {'EffectiveCapacity': ''})['EffectiveCapacity'])
        update_data(data, id, 'reservoirName',
                    get_record_time(daily_operational_statistics.get(id, {'RecordTime': now_with_timezone(__taipei_tz__).strftime(__api_time_format__)})), daily_operational_statistics.get(id, {'ReservoirName': ''})['ReservoirName'])

    calculate_effective_water_storage_storage_percentage(data)
    data['updateTime'] = now_with_timezone(
        __taipei_tz__).isoformat(timespec='seconds')

    add_reservoir_identifier(data)

    return data


def main():

    data = generate_data()

    upload_data(bucket_name='projects.readr.tw',
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8', destination_blob_name='data/reservoir.json', is_public=True)

    dd = dashboard.convert_data_for_taiwan_dashboart(data)
    dd['updated'] = now_with_timezone(
        __taipei_tz__).isoformat(timespec='seconds')

    upload_data(bucket_name='projects.readr.tw',
                data=json.dumps(dd, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8', destination_blob_name='taiwan-dashboard/reservoir.json', is_public=True)


if __name__ == '__main__':
    main()
