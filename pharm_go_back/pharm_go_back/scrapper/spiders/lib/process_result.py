from scrapy.http import JsonRequest
from scrapy.utils.project import get_project_settings



def send_result_data(data):
    return JsonRequest(
        url=get_project_settings().get('BACKEND_ADDRESS'),
        headers={'Content-Type': 'application/json'},
        method='POST',
        data=data,
        dont_filter=True,
    )
