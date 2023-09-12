from scrapy.http import JsonRequest

BACKEND_ADDRESS = 'http://localhost:8080/med'


def send_result_data(data):
    return JsonRequest(
        url=BACKEND_ADDRESS,
        headers={'Content-Type': 'application/json'},
        method='POST',
        data=data,
        dont_filter=True,
    )
