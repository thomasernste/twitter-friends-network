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

# �l�b�g���[�N�`��

import matplotlib.pyplot as plt
import MySQLdb
import networkx as nx

con = MySQLdb.connect(user=USRE, passwd=PASSWD, db='twitterNetwork', charset='UTF8')
cur = con.cursor()

# Twitter��Directed Graph
g = nx.DiGraph()

# id��screen_name�Ή��t��������
cur.execute("SELECT target, screen_name FROM myFriends")
ids = {}
for id in cur.fetchall():
    ids[id[0]] = id[1]

# friends���m�̊֌W�݂̂����o���ăO���t�ɒǉ�
cur.execute("SELECT * FROM friends")
for edge in cur.fetchall():
    if edge[1] in ids:
        g.add_edge(ids[edge[0]], ids[edge[1]])

# �m�[�h�̑傫����������ɔ�Ⴓ����
node_size = {}
for v in g:
    node_size[v] = float(g.in_degree(v)) * 2 + 2

# �����������ȏゾ��screen_name�\���c�݂����ȏ���
"""
labels = {}
for name in ids.values():
    if node_size[name] > 1000:
        labels[name] = name
    else:
        labels[name] = ''
"""

# �`��̍ۂɂ�Undirected Graph�ɕϊ�
g = nx.Graph(g)
nx.draw(g, pos=nx.spring_layout(g), with_labels=False, node_size=[node_size[v] for v in g],
        node_color='red', width=0.1, alpha=0.7)
plt.show()