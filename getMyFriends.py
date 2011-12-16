# coding: utf-8
#
#
# Copyright 2011 Hisao Soyama <hisao.soyama@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Twitter API���玩����friends���擾����

import json
import urllib

import MySQLdb
import oauth2 as oauth

# Oauth�N���C�A���g���쐬
consumer = oauth.Consumer(key=YOUR_APP_KEY, secret=YOUR_APP_SECRET)
token = oauth.Token(key=YOUR_TOKEN_KEY, secret=YOUR_TOKEN_SECRET)
client = oauth.Client(consumer, token)

# �G���h�|�C���gURL�ƃp�����[�^
url = 'http://api.twitter.com/1/friends/ids.json'
params = {}

# Oauth�N���C�A���g����API�ɐڑ��Dcontent�����o��
res = client.request(url+'?'+urllib.urlencode(params), 'GET')
content = json.loads(res[1])

"""
MySQL���twitterNetwork�f�[�^�x�[�X���쐬�ς݂Ƃ���D
�e�[�u���� myFriends �� friends �̂Q�D

myFriends
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| target      | int(11)     | YES  |     | NULL    |       |
| ended       | int(11)     | YES  |     | 0       |       |
| screen_name | varchar(20) | YES  |     | NULL    |       |
+-------------+-------------+------+-----+---------+-------+

friends
+--------+---------+------+-----+---------+-------+
| Field  | Type    | Null | Key | Default | Extra |
+--------+---------+------+-----+---------+-------+
| source | int(11) | YES  |     | NULL    |       |
| target | int(11) | YES  |     | NULL    |       |
+--------+---------+------+-----+---------+-------+
"""

con = MySQLdb.connect(user=USRE, passwd=PASSWD, db='twitterNetwork', charset='UTF8')
cur = con.cursor()

# myFriends�e�[�u����friends��id�����
for id in content[u'ids']:
    print id
    sql = "INSERT INTO myFriends (target) VALUES (%d)" % id
    cur.execute(sql)
con.commit()