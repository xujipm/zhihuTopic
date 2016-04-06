# coding: utf-8
# author: xujipm

import requests
import time
import threading
import queue
import random
import json
import redis
from bs4 import BeautifulSoup

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
        'Cookie': 'q_c1=d79fc5c8af864391bbbf7ee91a48e178|1459571457000|1459571457000; l_cap_id="MmNhN2RiMjgwM2VhNDAzMzgzOWVkZGQ5MTA5NDVkY2I=|1459571457|59af63dfc1bbdad9c6a672d182f7eecd55343e2a"; cap_id="OWFiNjhmMmRiY2M5NGYzNDlhYTk3MWU3MTc5M2JkNjI=|1459571457|9ee39aa2efc70242acb084a789c6e7e1b21f4b48"; _xsrf=a655aea78233e1b6ff152a09153f1bbe; d_c0="ACCA--xitQmPTownLtzTX3OzOMLywzxlgFA=|1459571460"; _za=7e9aa567-a894-43dd-b91b-ddbe10a54737; auth_type=cXFjb25u|1459571631|deefd5c44cdf05955e7ee064a4e2e9286ae130fb; token="NkYyODJFQkU3QTUwMTc4NTQ3Nzc1QTlCOThGQkIyMUE=|1459571631|d3c38bb88722db205e734366ad8d7bfda8815bef"; client_id="QTI4N0FGRUNFMkFCRDlDNDc1OUM1NEI3MTU2OEFFNjQ=|1459571631|a4ec13c9c7020b9cdbecbf869cc7278a05afe2cd"; z_c0="QUZEQUpxaGp0UWtYQUFBQVlRSlZUY1BZSmxlaDRjT25vYjBSbWc3MldRblJsclJQT2t1RWJnPT0=|1459571651|ce5f1e83ef2858108cc2256cf4a3b63aa0330e8f"; n_c=1; __utmt=1; __utma=51854390.1432889541.1459571455.1459571455.1459581663.2; __utmb=51854390.2.10.1459581663; __utmc=51854390; __utmz=51854390.1459581663.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/topic/19555513/organize; __utmv=51854390.100-2|2=registration_date=20160402=1^3=entry_date=20160402=1'
    }, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
        'Cookie': '_za=863ece3d-fad7-4c46-b369-d2bf69de1b57; udid="ACAAaiw9mAmPTuJQNCyp1L2_V5o79vTu3Dk=|1457615406"; _ga=GA1.2.370700666.1452949567; _xsrf=063ca1b5ced5b0299c1adab5f616086e; d_c0="AGDAI8vfowmPTo8shEmMw3Y9wMOHQ5a1j_0=|1458396233"; auth_type=cXFjb25u|1459571135|a45050e81282ea88a419238ce60c6b592eedf67a; token="NkQ0NzY4OTk3OTFDRDVGMTVGNEMwRDI0NTMyQkU1NTk=|1459571135|d6779a7bccca9332a63dfa43d15f04d5cae70ea2"; client_id="RDREMDY4RTg1Nzg3MTc2RDFBQjJBQjJDRkM5QzhBM0Y=|1459571135|45c7271aeffa78b91409226154510953e74b2f88"; q_c1=49e036fff6684615a61063d6123964ca|1459581388000|1459581388000; cap_id="MzMyMjNmMjdhNjczNDkzNzljOTYzYTMxMWNjMjc0MjU=|1459581388|5541d16d6fa9918a89cd4826102c4655108e5132"; l_cap_id="ZGQyNDhiYWRiOWUyNDliNTlmNjBmMGYwYTg4MWUzOTA=|1459581388|3e1523bb9333638298fa7b8e67796cfe270bf309"; __utmt=1; z_c0="QUZEQUpxaGp0UWtYQUFBQVlRSlZUVnpfSmxkZ21oaFNvT1JwWDVLOWJfWUczUmR4MHJpWmpBPT0=|1459581531|a0ce6f3a35e7ca15e2aa1227e79b75849e7b258e"; n_c=1; __utma=51854390.370700666.1452949567.1459571308.1459581388.2; __utmb=51854390.12.10.1459581388; __utmc=51854390; __utmz=51854390.1459581388.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/topic/19552266; __utmv=51854390.100-2|2=registration_date=20160402=1^3=entry_date=20160402=1'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': '_xsrf=33f182ac8eb7dd8de5a6b8acc2caedd2; d_c0="ADBA6EdHtQmPTuJmm3-Q9eM9yiaU7DAGvRk=|1459564212"; _za=01d24a82-e626-45df-b811-621c71d83411; q_c1=55f99dffb9be432888aef3ec2b870d96|1459564222000|1459564222000; __utmt=1; l_cap_id="NDZjOTM3Mzg1NWM3NDgwZmI4MGZmMWMzYmM1MzM5Nzk=|1459581541|5983720fbbf2ed2d5a18db6b3d786f2c136c5121"; cap_id="MGZkZDBmYjE0ZDAwNDVlYWFmNGExYjRlNmI1YmU2ZGY=|1459581541|5f052ea413cd28409da0687b8873667004a23245"; z_c0="QUdCQVU4Vmh0UWtYQUFBQVlRSlZUWFRfSmxmOXJpS0prcy1YRy1abGhsd3Z4OGVTMGVFZEh3PT0=|1459581554|98bd63e569bb0a38f7cdfb81d7f03e5a85ae2350"; n_c=1; __utma=51854390.1360063609.1459564212.1459580059.1459581368.4; __utmb=51854390.12.10.1459581368; __utmc=51854390; __utmz=51854390.1459581368.4.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100-2|2=registration_date=20160402=1^3=entry_date=20160402=1'
        }]

rootUrl = 'https://www.zhihu.com/'
rootTopicId = 19776749

r = redis.Redis(host='127.0.0.1', port=6379)
topicQueue = queue.Queue(maxsize=-1)
if r.llen('Queue') == 0:
    topicQueue.put(rootTopicId)
    r.rpush('Queue', rootTopicId)
maxThread = 100
for tid in r.lrange('Queue', 0, -1):
    topicQueue.put(int(tid))


def exploreTopic(topicId=rootTopicId):
    r.lpop('Queue')
    if r.sismember('DoneTask', topicId):
        return
    requestUrl = rootUrl + 'topic/' + str(topicId) + '/organize'
    webData = requests.get(requestUrl, headers=headers[random.choice(range(2))])
    soup = BeautifulSoup(webData.text, 'lxml')
    topicName = soup.select('#zh-topic-title > h1')
    topicFollow = soup.select('#zh-topic-side-head > div > a > strong')
    sonTopics = soup.select('#zh-topic-organize-child-editor > div.zm-tag-editor-labels.zg-clear > a')
    topicNicks = soup.select('#zh-topic-alias-list > li')
    topicDesc = soup.select('#zh-topic-desc > div.zm-editable-content')

    requestUrl = 'https://www.zhihu.com/node/TopicProfileCardV2?params=%7B%22url_token%22%3A%22' + str(topicId) + '%22%7D'
    webData = requests.get(requestUrl, headers=headers[random.choice(range(1))])
    soup = BeautifulSoup(webData.text, 'lxml')
    topicTop = soup.select('body > div > div.lower.clearfix > div.meta > a:nth-of-type(2) > span.value')
    topicQuestions = soup.select('body > div > div.lower.clearfix > div.meta > a:nth-of-type(1) > span.value')

    nicks = []
    for _nick in topicNicks:
        nicks.append(_nick.get_text(strip=True))
    sonTopic = []
    for _topic in sonTopics:
        sonTopic.append([_topic.get_text(strip=True), _topic.get('data-token')])

    if len(topicFollow) == 0:
        follow = '0'
    else:
        follow = topicFollow[0].get_text(strip=True)
    if len(topicName) == 0:
        name = 'error'
    else:
        name = topicName[0].get_text(strip=True)
    if len(topicDesc) == 0:
        description = 'error'
    else:
        description = topicDesc[0].get_text(strip=True)
    if len(topicTop) == 0:
        answers = 'error'
    else:
        answers = topicTop[0].get_text(strip=True)
    if len(topicQuestions) == 0:
        questions = 'error'
    else:
        questions = topicQuestions[0].get_text(strip=True)

    topicData = {
        'id': topicId,
        'name': name,
        'follow': follow,
        'description': description,
        'nicks': nicks,
        'sonTopics': sonTopic,
        'top-answers': answers,
        'questions': questions
    }

    # time.sleep(0.1)
    for [name, tid] in sonTopic:
        if not (r.sismember('AllTask', tid)):
            r.sadd('AllTask', tid)
            topicQueue.put(tid)
            r.rpush('Queue', tid)
    r.sadd('DoneTask', topicId)
    #print(' '*70,len(doneSet),' | ', topicData)
    file = open('zhihu-thread.txt', 'a')
    file.write('"' + str(topicId) + '":' + json.dumps(topicData) + ',\n')
    file.close()


class topicThread(threading.Thread):

    def __init__(self, threadName):
        threading.Thread.__init__(self, name=threadName)

    def run(self):
        while True:
            if topicQueue.empty():
                print('No Task in Queue, Is Ending?')
                while topicQueue.empty():
                    time.sleep(1)
                    print('|*|', 'Done:', r.scard('DoneTask'), 'Undo', topicQueue.unfinished_tasks, 'Total', r.scard('AllTask'))
            print('Done:', r.scard('DoneTask'), 'Undo', topicQueue.unfinished_tasks, 'Total', r.scard('AllTask'))
            exploreTopic(topicQueue.get())

myThreads = []
for i in range(maxThread):
    myThreads.append(topicThread('No.' + str(i)))
    myThreads[i].start()
