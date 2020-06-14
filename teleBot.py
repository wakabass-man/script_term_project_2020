import telepot
import time
import http.client
from xml.dom.minidom import parse, parseString

myID = "1273133128"
botTOKEN = "1129600236:AAG2hp53y8cHHsyrn4ZGEOff34u8tO2Ik7w"
bot = telepot.Bot(botTOKEN)

conn = http.client.HTTPConnection("tour.chungnam.go.kr")
conn.request("GET", "/_prog/openapi/?func=stay&start=0&end=150")
req = conn.getresponse()
BooksDoc = req.read().decode('utf-8')
#print(BooksDoc)

locList = ["천안", "공주", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성", "예산", "태안", "보령"]
upsoList = []
infoList = []

infoStr = "관광지 숙박업소 검색 봇입니다.\n지역별 업소들을 보시려면 '지역 지역명'을 입력해주세요.\n" + \
    "업소의 구체적인 정보를 알고싶으시면 '업소 업소명'을 입력해주세요.\n감사합니다.\n"
bot.sendMessage(myID, infoStr)

def findByLoc(loc):
    upsoList.clear()

    parseData = parseString(BooksDoc)
    item_info = parseData.childNodes
    row = item_info[0].childNodes
    for item in row:  # row = <item>
        if item.nodeName == "item":
            subitems = item.childNodes
            if subitems[3].firstChild.nodeValue == loc:
                upsoList.append(subitems[7].firstChild.nodeValue)

    m = "\n".join(upsoList)
    bot.sendMessage(myID, m)
def findByName(name):
    global  infoList

    infoList.clear()

    parseData = parseString(BooksDoc)
    item_info = parseData.childNodes
    row = item_info[0].childNodes
    for item in row:  # row = <item>
        if item.nodeName == "item":
            subitems = item.childNodes
            if subitems[7].firstChild.nodeValue == name:
                if subitems[17].firstChild is not None:
                    tel = subitems[17].firstChild.nodeValue
                else:
                    tel = "-"
                if subitems[21].firstChild is not None:
                    desc = subitems[21].firstChild.nodeValue
                else:
                    desc = "-"
                infoList = [subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                            tel, subitems[11].firstChild.nodeValue, desc]
                break

    if len(infoList) == 0:
        return False
    else:
        m = "업소 이름: " + str(infoList[0]) + "\n업소 분류: " + str(infoList[1]) + "\n업소 번호: " + str(infoList[2])\
        + "\n업소 위치: " + str(infoList[3]) + "\n업소 설명: \n\n" + str(infoList[4])
        return m
def handle(msg):
    content, chat, id = telepot.glance(msg)

    if "지역" in msg["text"]:
        tmp = list(msg["text"].split())
        loc = tmp[1]
        if loc in locList:
            findByLoc(loc)
        else:
            bot.sendMessage(id, "없는 지역 입니다.")
    elif "업소" in msg["text"]:
        tmp = list(msg["text"].split())
        name = tmp[1]
        realName = findByName(name)
        if realName != False:
            bot.sendMessage(id, realName)
        else:
            bot.sendMessage(id, "없는 업소 입니다.")
    else:
        bot.sendMessage(id, infoStr)

bot.message_loop(handle)

while True:
    time.sleep(400)