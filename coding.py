#coding:utf-8
import requests
import json
import time

def doit(password,email,username,task,projectName):

    s = requests.Session()
    logininfo = {'password':password,'remember_me':'false','email':email}
    s.post('https://coding.net/api/login',params=logininfo)

    #操作任务
    s.put('https://coding.net/api/task/'+task+'/status?status=1')
    s.put('https://coding.net/api/task/'+task+'/status?status=2')

    #提交代码
    code = s.get('https://coding.net/api/user/'+username+'/project/'+projectName+'/git/treeinfo/master');
    #print(code.text)
    codejson = json.loads(code.text)
    lastCommitId = codejson['data']['infos'][0]['lastCommitId']
    print(lastCommitId)

    changeinfo = {'content':'#test time:'+time.ctime(),'message':'update README.md','lastCommitSha':lastCommitId}
    change = s.post('https://coding.net/api/user/'+username+'/project/'+projectName+'/git/edit/master%252FREADME.md',params=changeinfo)

    #合并分支
    mergeinfo = {'srcBranch':'dev','desBranch':'master','title':'demo'}
    merge = s.post('https://coding.net/api/user/'+username+'/project/'+projectName+'/git/merge',params=mergeinfo)
    mergejson = json.loads(merge.text)
    mergeid=mergejson['data']['merge_request']['iid']
    print(mergeid)

    #拒绝合并
    refuse = s.post('https://coding.net/api/user/'+username+'/project/'+projectName+'/git/merge/'+ str(mergeid) +'/refuse')
    
    #WebIDE
    ide = s.get('https://ide.coding.net/ws/?ownerName='+username+'&projectName='+projectName)
    ideinfo = {'ownerName':username,'projectName':projectName,'memory':'128'}
    s.post('https://ide.coding.net/backend/ws/create',params=ideinfo)

    #账户余额
    balance = s.get('https://coding.net/api/point/balance')
    balancejson = json.loads(balance.text)
    point = balancejson['data']['point_left']
    print(time.ctime()+'successful!'+ username +' money:')
    print(point)
    print('--------------------------------------------------------------')






