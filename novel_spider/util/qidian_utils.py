import requests
import json


def get_score(book_id, csrf_token):
    """
    获取小说评分
    :param csrf_token: csrf
    :param book_id: 小说ID
    :return: 评分，如果出现错误则返回-1
    """
    api = "https://book.qidian.com/ajax/comment/index"

    querystring = {"_csrfToken": csrf_token, "bookId": str(book_id), "pageSize": "1"}

    response = requests.request("GET", api, params=querystring)
    data = json.loads(response.text)

    return float(data['data']['rate']) if 'suc' in data['msg'] else -1
