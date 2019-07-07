import json
import re
from urllib import request
from urllib.request import urlretrieve
import os
from urllib.parse import quote
import requests
from datetime import datetime, timedelta
import random

headers = {
    'accept': "application/json, text/plain, */*",
    'origin': "https://wx.zsxq.com",
    'x-version': "1.10.14",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'x-request-id': "7adc91b9-1cbb-3b23-2a2b-d2ede785eeb5",
    'referer': "https://wx.zsxq.com/dweb/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    'cookie': "zsxq_access_token=(自己登陆知识星球的token);UM_distinctid=(这个也是自己的);sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b8edb6fae484-0579c4f3b8620a-e343166-2073600-16b8edb6faf3ed%22%2C%22%24device_id%22%3A%2216b8edb6fae484-0579c4f3b8620a-e343166-2073600-16b8edb6faf3ed%22%2C%22props%22%3A%7B%7D%7D;avatar_url=https%3A//images.zsxq.com/Fk_1g2If9P5yo9swO1IKTaoPvP8j%3Fe%3D1906272000%26token%3DkIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD%3A7VlL6OAaOxQE17Kk5hkm4npuDik%3D;_uab_collina=156152430848883409461935;user_id=88481814585182;name=Cx001;upload_channel=qiniu;ws_address=wss%3A//ws.zsxq.com/ws%3Fversion%3Dv1.10%26access_token%3D94744347-A07C-B14C-1294-7C8EFC5F8E9F",
}


#加入的圈子id
def get_group(headers):
    url = "https://api.zsxq.com/v1.10/groups"
    #对URL发起get请求获取页面内容
    response = requests.request("GET",url,headers=headers)
    #将json对象转化为python对象
    jsonobj = json.loads(response.text)
    # print(jsonobj)
    # json1 = json.loads(jsonobj)
    # print(type(jsonobj))
    try:
        for number in range(len(jsonobj['resp_data']['preferences']['sorts'])):
            print("星球ID：",jsonobj['resp_data']['groups'][number]['group_id'])
            print("星球的名字：",jsonobj['resp_data']['groups'][number]['name'])
            print("星球的星主是：",jsonobj['resp_data']['groups'][number]['owner']['name'])
            print('\n')
    except Exception:
        print("已没有再多的星球")
    # print(type(jsonobj['resp_data']['preferences']['sorts']))
    # print(len(jsonobj['resp_data']['preferences']['sorts']))
    
#获取文件id后下载文件（zip,doc,xls  ....）
def get_gobal_file(file_url,file_name,headers,savepath='./'):
    # #对URL发起get请求获取页面内容
    response = requests.request("GET",file_url,headers=headers)
    #将json对象转化为python对象
    jsonobj = json.loads(response.text)
    # r = requests.get(jsonobj['resp_data']['download_url'])
    # with open(file_name,"wb") as f:
    #     f.write(r.content)
    # print(jsonobj)
    # print(jsonobj['resp_data']['download_url'])
    # with open(file_name,"wb") as f:
    #     f.write()
    # for download_url in jsonobj['resp_data']['download_url']:
    #     pass
    def reporthook(a, b, c):
        print("\r  Downloading: %5.1f%%" % (a * b * 100.0 / c), end="")

    filename = os.path.basename(file_name)
    if not os.path.isfile(os.path.join(savepath, filename)):
        print('Downloading data from %s' % jsonobj['resp_data']['download_url'])
        urlretrieve(jsonobj['resp_data']['download_url'], os.path.join(savepath,filename), reporthook=reporthook)
        print('\nDownloading finished')
    else:
        print('File already exists!')

    filesize = os.path.getsize(os.path.join(savepath,filename))

    print('File size = %.2f Mb' % (filesize/1024/1024))

#生成时间对应的格式
def time():
    now = datetime.now()
    print(now)
    time1 = now.strftime('%Y-%m-%d')
    print(time1)
    time2 = now.strftime('%H:%M:%S')
    print(time2)
    number = str(random.randint(100,999))
    # print (type(random.randint(100,999)))
    end_time = time1+'T'+time2+'.'+number+'+0800'
    return end_time




#获取某个星球下的文件id
def get_download_url(headers,group_id):
    # url = "https://api.zsxq.com/v1.10/groups/"+group_id+"/files?count=3"
    end_time = time()
    url = "https://api.zsxq.com/v1.10/groups/"+group_id+"/files?count=20&end_time="+quote(end_time)
    print(url)
    #对URL发起get请求获取页面内容
    response = requests.request("GET",url,headers=headers)
    jsonobj = json.loads(response.text)
    print(type(jsonobj))
    # print(jsonobj['resp_data']['files'][0]['file']['file_id'])
    # print(len(jsonobj['resp_data']['files']))
    try:
        for file_id in range(len(jsonobj['resp_data']['files'])):
            file_url = 'https://api.zsxq.com/v1.10/files/'+str(jsonobj['resp_data']['files'][file_id]['file']['file_id'])+'/download_url'
            print(file_url)
            file_name = jsonobj['resp_data']['files'][file_id]['file']['name']
            print(file_name)
            get_gobal_file(file_url,file_name,headers,savepath='./')
            file_write(file_name,file_url)
    except IOError as e:
        print('Not have any files!')
    

def file_write(file_name,file_url):
    try:
        f = open('test1.log','a',encoding='utf-8')
        f.write(file_name+'\n')
        f.write(file_url+'\n\n')
        f.close()
    except IOError as e:
        print('读写文件失败！')


if __name__ == "__main__":
    get_group(headers)
    # get_gobal_file(headers)
    group_id = input("请输入星球id：")
    get_download_url(headers,group_id)
