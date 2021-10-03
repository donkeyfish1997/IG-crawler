import pickle
import requests
import re
import json

with open('./api/info.pickle', 'rb') as f:
    info = pickle.load(f)
session = requests.session()


def getIdByName(name):
    global session, cookies
    url = f'https://www.instagram.com/{name}/'
    res = session.get(url, cookies=cookies)
    tmp = re.search(r'"logging_page_id":"profilePage_(\d+)"', res.text).group()
    id = re.search(r'\d+', tmp).group()
    return id


def getIgArticlesJsonByidAndAfter(id, after=''):
    global session, cookies
    if not hash:    # first time
        url = f'https://www.instagram.com/graphql/query/?query_hash=ea4baf885b60cbf664b34ee760397549&variables={{"id":"{id}","first":12}}'
    else:           # after
        url = f'https://www.instagram.com/graphql/query/?query_hash=ea4baf885b60cbf664b34ee760397549&variables={{"id":"{id}","first":12,"after":"{after}"}}'
    print(url)
    res = session.get(url, cookies=cookies)
    return res.text


def getIgCommentsJsonByshortcodeAndAfter(shortcode, after=''):
    global session, cookies
    if not after:    # first time
        url = f'https://www.instagram.com/graphql/query/?query_hash=afa640b520008fccd187e72cd59b5283&variables={{"shortcode":"{shortcode}","child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":24,"has_threaded_comments":true}}'
    else:           # after
        after = after.replace('"','\\"') .replace(' ','+')
        url = f'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={{"shortcode":"{shortcode}","first":12,"after":"{after}"}}'
    res = session.get(url,cookies=cookies)
    return res.text


#分析許多文章的淺資訊
def getInfoByIgArticlesJson(dicHtml):
    tmp = json.loads(dicHtml)['data']['user']['edge_owner_to_timeline_media']
    dic = {}
    dic["has_next_page"]= tmp['page_info']['has_next_page']
    dic["after"]=   tmp['page_info']['end_cursor']
    dataArr = []
    for info in tmp['edges']:
        info = info['node']
        tmp = {}
        # 文章
        tmp['text'] = info['edge_media_to_caption']['edges'][0]['node']['text']
        # 圖片
        tmp['img']=info['display_url']
        # 留言數
        tmp['comment_count']=info['edge_media_to_comment']['count']
        # 按讚數
        tmp['like']=info['edge_media_preview_like']['count']
        # 時戳
        tmp['timestamp']=info['taken_at_timestamp']
        # 留言查詢
        tmp['shortcode']=info['shortcode']
        dataArr.append(tmp)
    dic['datas'] = dataArr
    return dic

#分析單一文章的身資訊
def getInfoByIgCommitsJson(dicHtml):
    tmp = json.loads(dicHtml)['data']['shortcode_media']['edge_media_to_parent_comment']
    dic = {}
    dic["has_next_page"]= tmp['page_info']['has_next_page']
    dic["after"]=   tmp['page_info']['end_cursor']
    dataArr = []
    for info in tmp['edges']:
        info = info['node']
        tmp = {}
        # 留言訊息
        tmp['text']=info['text']
        # 留言時間
        tmp['timestamp']=info['created_at']
        # 留言作者
        tmp['user']=info['owner']['username']
        # 此留言按讚人數
        tmp['like']=info['edge_liked_by']
        # 此留言的留言(未詳細分析)
        tmp['threaded_comments']=info['edge_threaded_comments']
        dataArr.append(tmp)
    dic['datas'] = dataArr
    return dic


def getIgImgsByNameAndPages(name, page):
    imgs = []
    id = getIdByName(name)
    after = ''
    for i in range(1, page+1):
        dicHtml = getIgArticlesJsonByidAndAfter(id, after)
        dic = getInfoByIgArticlesJson(dicHtml)
        for data in dic['datas']:
            imgs.append(data['img'])
        if dic['has_next_page']:
            after = dic['after']
        else:
            print('no page')
            break
    return imgs

def getIgICommitsByshortcodeAndPages(shortcode, page):
    commits = []
    after = ''
    for i in range(1, page+1):
        dicHtml = getIgCommentsJsonByshortcodeAndAfter(shortcode, after)
        dic = getInfoByIgCommitsJson(dicHtml)
        for data in dic['datas']:
            commits.append(data['text'])
        if dic['has_next_page']:
            after = dic['after']
        else:
            print('no page')
            break
    return commits

if __name__ == '__main__':
    pass