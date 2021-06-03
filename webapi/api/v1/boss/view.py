import re
import requests
from flask import request, jsonify

from webapi.api.v1.boss import bossinfo
from webapi.src.orm.boss import AddorRestBoss

enemy_base_api = "http://karth.top/api/enemy/"

@bossinfo.route('/set', methods=['POST'])
def set_boss():
    data = request.get_json(silent=True)
    keyid = re.findall("\d+_?+\d*", data['url'])
    api_url = enemy_base_api + keyid + '.json'
    res = requests.get(api_url)
    res = res.json()
    result = AddorRestBoss(res['basicInfo']['enemyID'], res['basicInfo']['name']['ja'])
    if result:
        return jsonify({"msg": "success!"}), 200
    return jsonify({"msg": "failure!"}), 500
