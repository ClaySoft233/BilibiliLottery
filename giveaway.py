import requests
import json
import time
import random
import sys

def list_find(valid_user, text):
    try:
        valid_user.index(text)
        return True
    except ValueError:
        return False

#url = input('请输入b站动态的网页地址(例如https://t.bilibili.com/289717220819569991)')
#endtime = input('请输入截止时间(例如 2019-8-21 10:21:00)')
#count = input('请输入将获奖的用户数量')
#follow = input('用户是否需要关注某些用户?(是/否)') # ! 系统限制只能访问前5页
url="https://t.bilibili.com/289717220819569991"
endtime="2019-8-21 12:53:00"
count="5"
follow="是"
UID="161775300"
if(follow == "是"):
    #UID = input('请输入那个用户的UID,多个请用","分割.')
    if(UID == ""):
        print('请检查您的输入: UID错误')
        sys.exit()

try: #检查url是否正确
    dynamic_id = url.split("/")[3]
    if(str.isdecimal(dynamic_id) == False):
        raise IndexError #抛出错误
except IndexError:
    print("请检查您的输入: URL错误")
    sys.exit()
if(url == "" or endtime == "" or follow == ""  or follow != "是" and follow != "否"):
    print('请检查您的输入: 部分内容为空或不符合条件')
    sys.exit()
else:
    try:
        endtimestamp = int(time.mktime(time.strptime(endtime, "%Y-%m-%d %H:%M:%S"))) #获取截止时间的时间戳
    except ValueError:
        print("时间输入错误")
        sys.exit()
    data = requests.get("http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id="+dynamic_id)
    html = data.content.decode("UTF-8")
    html = json.loads(html)
    total_count=html["data"]["total_count"] #获得总评论页数
    valid_user=[] #初始化有效抽奖用户
    valid_comment=[] #初始化有效评论
    #从第一页开始,遍历所有转发
    for page in range(0,int(total_count)):  
        data = requests.get("http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id="+dynamic_id+"&offset"+str(page))
        html = data.content.decode("UTF-8")
        html = json.loads(html)
        total_count=html["data"]["total_count"]
        for eachmsg in html["data"]["comments"]:
            timestamp = eachmsg["ts"]
            if(timestamp <= endtimestamp and list_find(valid_user,eachmsg["uid"]) == False): #如果未到截止时间且之前没有发过重复评论
                if(follow == "真"):
                    if(follow == "真"):
                        if(UID.find(",")==True): #如果需要关注多个up
                            UID=UID+","
                            UID=UID.split(",") #以,为分割,分割需要关注的uid
                            valid == False
                            for pg in range(0,5):
                                follow_list=json.loads(requests.get("https://api.bilibili.com/x/relation/followings?vmid="+eachmsg["uid"]+"&pn="+str(pg)).content.decode("UTF-8"))
                                for eachuid in UID: #遍历每个需要关注的UID
                                    #获取用户的关注列表
                                    if(follow_list["re_version"]!=""):
                                        for eachfollow in follow_list["data"]["list"]:
                                            #遍历用户关注的人
                                            if(eachfollow["mid"] == eachuid and eachfollow["mtime"] <= endtimestamp):
                                                valid = True
                                                break
                                            else:
                                                valid = False
                                        if(valid == False):
                                            break
                                    else:
                                        break
                                if(valid == False):
                                    break

                        else:
                            for pg in range(0,5):
                                follow_list=json.loads(requests.get("https://api.bilibili.com/x/relation/followings?vmid="+eachmsg["uid"]+"&pn="+str(pg)).content.decode("UTF-8"))
                                #获取用户的关注列表
                                if(follow_list["re_version"]!=""):
                                    for eachfollow in follow_list:
                                        if(eachfollow == UID):
                                            valid = True
                                            break
                                        else:
                                            valid = False
                                
                    if(valid == True):
                        valid_user.append(eachmsg["uid"]) #添加信息
                        valid_comment.append(eachmsg["detail"]["desc"]["dynamic_id"])

                    
                else:
                    valid_user.append(eachmsg["uid"]) #添加信息
                    valid_comment.append(eachmsg["detail"]["desc"]["dynamic_id"])

    done = 0
    luckypep=[] #初始化
    for user in range(0,len(valid_user)): #开始抽奖
        if(done<=int(count)):
            luckypep.append(valid_user[random.randint(0,len(valid_user)-1)])
            done=done+1
        else:
            break
        
        
    strwillprint=""
    for lucky in luckypep:
        content=json.loads(json.loads(requests.get("https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id="+dynamic_id).content)["data"]["card"]["card"])["item"]["description"]
        #哎呀妈耶..
        strwillprint=strwillprint+"幸运用户UID:"+str(lucky)+"评论内容:\r\n"+ content + "   \r\n"
    if(strwillprint==""):
        strwillprint="没有符合条件的用户"
    print("随机抽奖完成!\r\n"+strwillprint)
