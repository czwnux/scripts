#! /usr/bin/env python
#coding=utf-8
import time
import httplib
import redis


report_host = ""
report_method = "/infra/stats/index.php"
app = "treasure"
db_user=""
db_passwd=""
redis_host = '192.168.8.202'
redis_port = 6379
redis_db = 0
timezone = 8
appid = "1"

action_map = {
              'login':'mixi-takara-unique-dailylogin',
              'install':'mixi-takara-dailyinstall-user',
              'visitFriend':'mixi-takara-friend-visit-click',
              'openFriendBox':'mixi-takara-friend-treasure-get',
              'wizardStart':'mixi-takara-tutorial-start',
              'completeGuide':'mixi-takara-tutorial-complete',
              'inviteFriendCount':'mixi-takara-invite-send-count-everyday',
              'inviteAccept':'mixi-takara-invite-accept-click',
              'inviteRefuse':'mixi-takara-invite-cancel-click',
              'synthesisTimes':'mixi-takara-item-composition-times',
              'openWish':'mixi-takara-wishitem-share-click',
              'gift':'mixi-takara-present-friend-times',
              'backIsland':'mixi-takara-goto-myisland-click',
              'myShoplist':'mixi-takara--myisland-shop-click',
              'minigameClick':'mixi-takara-minigame-timeplus-click',
              'achievementClick':'mixi-takara-trophy-get-(trophyID)',
              'rankingmapClick':'mixi-takara-maplank-click',
              'userShop':'mixi-takara-shop-click',
              'costGp':'mixi-takara-kira-spent-total',
              'costPp':'mixi-takara-Tcoin-spent-total',
             }
 

             
ts = time.gmtime( time.time() + 3600 * timezone)
today = time.strftime('%Y-%m-%d', ts)
             
def send_report(data):
        conn = httplib.HTTPConnection(report_host)
    
        for k in data:
            if data[k]:
                print "%s?app=%s&event=%s&count=%s" % (report_method,app,k,data[k])
                conn.request("GET", "%s?app=%s&event=%s&count=%s" % (report_method,app,k,data[k]))
                r1 = conn.getresponse()
                print r1.status, r1.reason
                data1 = r1.read()
                print data1



def get_report():

        data = {}

        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        for k in action_map:
            key = "%s_%s_%s" % (appid,k,today)
            data[action_map[k]] = r.get(key)
             
        for k in r.keys("%s_map*Complate_%s" % (appid,today)):
            strlen_start = len("%s_map" % appid)
            strlen_end = len("Complate_%s" % today)
            itemid = k[strlen_start:-strlen_end]
            key = "mixi-takara-map-%s-complete-user" % itemid
            action_map["map%sComplate" % itemid] = key
            data[key] = r.get(k)

        for k in r.keys("%s_*Pay_%s" % (appid,today)):
            strlen_start = len("%s_" % appid)
            strlen_end = len("Pay_%s" % today)
            itemid = k[strlen_start:-strlen_end]
            key = "mixi-takara-shop-pay-%s" % itemid
            action_map["%sPay" % itemid] = key
            data[key] = r.get(k)

        for k in r.keys("%s_buy*Usegp_%s" % (appid,today)):
            strlen_start = len("%s_buy" % appid)
            strlen_end = len("Usegp_%s" % today)
            itemid = k[strlen_start:-strlen_end]
            
            key = "mixi-takara-shop-kira-spent-itemid-%s" % itemid
            action_map["buy%sUsegp" % itemid] = key
            data[key] = r.get(k)
            data["mixi-takara-shop-numItemPurchased-itemid-%s" % itemid] = data[key]

        for k in r.keys("%s_buy*Usepp_%s" % (appid,today)):
            strlen_start = len("%s_buy" % appid)
            strlen_end = len("Usepp_%s" % today)
            itemid = k[strlen_start:-strlen_end]
            key = "mixi-takara-shop-Tcoin-spent-itemid-%s" % itemid
            action_map["buy%sUsepp" % itemid] = key
            data[key] = r.get(k)
            
            key_numItemPurchased = "mixi-takara-shop-numItemPurchased-itemid-%s" % itemid
            if data.has_key(key_numItemPurchased):
                data[key_numItemPurchased] = data[key_numItemPurchased] + data[key]
            else:
                data[key_numItemPurchased] = data[key]
            
            if data.has_key("inviteAccept_count"):
                data['mixi-takara-invite-click-everyday'] = data['inviteAccept_count'] + data['inviteRefuse_count']
                data['mixi-takara-invite-send-everyday'] = data['mixi-takara-invite-click-everyday']
                data['mixi-takaral-invite-popup'] = data['mixi-takara-invite-click-everyday']

            
        return data

#def data_init():
    
    #r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    

        
        
    #for k in action_map:
    #    key = "%s_%s_%s" % (appid,k,today)
    #    if not r.exists(key):
    #        r.set(key,0)

def main():
        #data_init()
        data = get_report()
        send_report(data)
if  __name__  ==  "__main__":
    main()
