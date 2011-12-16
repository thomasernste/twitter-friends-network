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

# friends��friends���擾����

import json
import urllib

import MySQLdb
import oauth2 as oauth

con = MySQLdb.connect(user=USRE, passwd=PASSWD, db='twitterNetwork', charset='UTF8')
cur = con.cursor()

# id���o��
cur.execute("SELECT target FROM myFriends WHERE ended = 0")
ids = [id[0] for id in cur.fetchall()]

# Oauth�N���C�A���g���쐬
consumer = oauth.Consumer(key=YOUR_APP_KEY, secret=YOUR_APP_SECRET)
token = oauth.Token(key=YOUR_TOKEN_KEY, secret=YOUR_TOKEN_SECRET)
client = oauth.Client(consumer, token)

# �G���h�|�C���gURL
url = 'http://api.twitter.com/1/friends/ids.json'

for id in ids:
    print id
    params = {'user_id': id}
    cursor = -1 # cursor������
    targets = []
    
    # cursor���[���ɂȂ�܂ŌJ��Ԃ��iAPI�̎d�l���Q�Ɓj
    while cursor:
        params['cursor'] = cursor
        # Oauth�N���C�A���g����API�ɐڑ�
        res = client.request(url+'?'+urllib.urlencode(params), 'GET')
        
        # �X�e�[�^�X400�ԑ�Ȃ��΂�
        if str(res[0].status).startswith('40'):
            break
        
        # content�����o����id��targets�ɒǉ�
        content = json.loads(res[1])
        targets += content[u'ids']
        cursor = content[u'next_cursor']
    
    print len(targets)
    # �擾����id���t�H���[��id�ƂƂ���frineds�e�[�u���ɓ����
    for target in targets:
        sql = "INSERT INTO friends VALUES (%d, %d)" % (id, target)
        cur.execute(sql)
    
    # �I���t���O1��
    if targets:
        cur.execute("UPDATE myFriends SET ended = 1 WHERE target = %d" % id)
    con.commit()
    print
