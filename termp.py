from tkinter import *
import tkinter.ttk
import http.client
from xml.dom.minidom import parse, parseString
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
import folium
import webbrowser
import smtplib
from email.mime.text import MIMEText
import tkinter.messagebox
import tkinter.font

window = Tk()
window.geometry("1080x670+0+0")
window.title("충남 관광지 숙박업소")
window.resizable(False, False)

myFont = tkinter.font.Font(family="맑은 고딕", size=20, slant="italic")

locList = ["검색", "천안", "공주", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성", "예산", "태안", \
           "보령"]
loc = ""
dataList = []
dataX = []
bookmarkDataList = []
dataY = []
buttonList = []
idxX = 0
def init():
    global searchFrame, textFrameS, imageFrameS, subFrameS, subFrameS2, subFrameS3, subFrameS4, comboboxS, inputEntryS, \
           bookmarkFrame, textFrameB, imageFrameB, subFrameB, subFrameB2, subFrameB3, subFrameB4

    notebook = tkinter.ttk.Notebook(window, width=1080, height=670)
    notebook.pack()

    searchFrame = Frame(window)
    notebook.add(searchFrame, text="검색")
    bookmarkFrame = Frame(window)
    notebook.add(bookmarkFrame, text="북마크")

    textFrameS = Frame(searchFrame)
    textFrameS.pack(side=LEFT)
    imageFrameS = Frame(searchFrame)
    imageFrameS.pack(side=LEFT)

    subFrameS = Frame(textFrameS)
    subFrameS.grid(row=0, column=0)
    subFrameS2 = Frame(textFrameS)
    subFrameS2.grid(row=0, column=1)
    subFrameS3 = Frame(textFrameS)
    subFrameS3.grid(row=1, column=0)
    subFrameS4 = Frame(textFrameS)
    subFrameS4.grid(row=1, column=1)

    comboboxS = tkinter.ttk.Combobox(subFrameS, values=locList, width=44)
    comboboxS.pack()
    comboboxS.set("지역 선택")

    inputEntryS = Entry(subFrameS2, width=44)
    inputEntryS.grid(row=0, column=0)

    Button(subFrameS2, text="찾기", command=search).grid(row=0, column=1)

    ##########################################################################################

    textFrameB = Frame(bookmarkFrame)
    textFrameB.pack(side=LEFT)
    imageFrameB = Frame(bookmarkFrame)
    imageFrameB.pack(side=LEFT)

    subFrameB = Frame(textFrameB)
    subFrameB.grid(row=0, column=0)
    subFrameB2 = Frame(textFrameB)
    subFrameB2.grid(row=0, column=1)
    subFrameB3 = Frame(textFrameB)
    subFrameB3.grid(row=1, column=0)
    subFrameB4 = Frame(textFrameB)
    subFrameB4.grid(row=1, column=1)

    Label(subFrameB, text="북마크 목록", width=45).pack()
    Label(subFrameB2, text="    ", width=45).pack()

    """
    logoImg = ImageTk.PhotoImage(file="logo.gif")
    logoLabelS = Label(imageFrameS, image=logoImg, height=300, width=390)
    logoLabelS.image = logoImg
    logoLabelS.grid(row=0, column=0)
    """
def search():
    bookmarkerS["state"] = "disabled"
    gmailerS["state"] = "disabled"
    mapperS["state"] = "disabled"

    global loc, locList, dataList

    loc = comboboxS.get()

    conn = http.client.HTTPConnection("tour.chungnam.go.kr")
    conn.request("GET", "/_prog/openapi/?func=stay&start=0&end=150")
    req = conn.getresponse()
    dataList.clear()
    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("normal error")
        else:
            parseData = parseString(BooksDoc)
            item_info = parseData.childNodes
            row = item_info[0].childNodes
            for item in row:  # row = <item>
                if item.nodeName == "item":
                    subitems = item.childNodes
                    if loc != "검색":
                        if subitems[3].firstChild.nodeValue == loc:
                            pass
                        else:
                            continue
                        if subitems[17].firstChild is not None:
                            tel = subitems[17].firstChild.nodeValue
                        else:
                            tel = "-"
                        if subitems[21].firstChild is not None:
                            desc = subitems[21].firstChild.nodeValue
                        else:
                            desc = "-"
                        if subitems[13].firstChild is not None and subitems[15].firstChild is not None:
                            w, k = subitems[13].firstChild.nodeValue, subitems[15].firstChild.nodeValue
                        else:
                            w, k = "-", "-"
                        if subitems[23].firstChild is not None:
                            i = subitems[23].firstChild.nodeValue
                        else:
                            i = "-"
                        dataList.append([subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue, desc, i, w, k])
                    else:
                        if inputEntryS.get() is not None and inputEntryS.get() in subitems[7].firstChild.nodeValue:
                            pass
                        else:
                            continue
                        if subitems[17].firstChild is not None:
                            tel = subitems[17].firstChild.nodeValue
                        else:
                            tel = "-"
                        if subitems[21].firstChild is not None:
                            desc = subitems[21].firstChild.nodeValue
                        else:
                            desc = "-"
                        if subitems[13].firstChild is not None and subitems[15].firstChild is not None:
                            w, k = subitems[13].firstChild.nodeValue, subitems[15].firstChild.nodeValue
                        else:
                            w, k = "-", "-"
                        if subitems[23].firstChild is not None:
                            i = subitems[23].firstChild.nodeValue
                        else:
                            i = "-"
                        dataList.append([subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue, desc, i, w, k])

            for e in subFrameS3.grid_slaves():
                e.destroy()
            buttonList.clear()

            Label(subFrameS3, text="\n<검색 결과>\n").grid(row=0, column=0)
            for i in range(len(dataList)):
                button = Button(subFrameS3, text=dataList[i][0], bg="light gray", \
                                command=lambda x=i: showDetail(x))
                for j in range(len(bookmarkDataList)):
                    if dataList[i][0] in bookmarkDataList[j][0]:
                        button["bg"] = "yellow"
                button.grid(row=i+1, column=0)
                buttonList.append(button)
    else:
        print("parsing error")
def initRenderText():
    global RenderTextS, RenderTextB, bookmarkerS, gmailerS, mapperS, bookmarkerB, gmailerB, mapperB

    RenderTextS = Text(subFrameS4, width=46, height=44, borderwidth=10, relief='ridge')
    RenderTextS.pack()
    RenderTextS.configure(state='disabled')

    bookmarkerS = Button(subFrameS4, text="북마크 설정", command=addBookmark)
    bookmarkerS.pack(side=RIGHT)

    gmailerS = Button(subFrameS4, text="G-mail", command=sendGMail)
    gmailerS.pack(side=RIGHT)

    mapperS = Button(subFrameS4, text="지도보기", command=Pressed)
    mapperS.pack(side=RIGHT)

    RenderTextB = Text(subFrameB4, width=46, height=44, borderwidth=10, relief='ridge')
    RenderTextB.pack()
    RenderTextB.configure(state='disabled')

    bookmarkerB = Button(subFrameB4, text="북마크 해제", command=deleteBookmark)
    bookmarkerB.pack(side=RIGHT)

    gmailerB = Button(subFrameB4, text="G-mail", command=sendGMail2)
    gmailerB.pack(side=RIGHT)

    mapperB = Button(subFrameB4, text="지도보기", command=Pressed2)
    mapperB.pack(side=RIGHT)

    bookmarkerS["state"] = "disabled"
    gmailerS["state"] = "disabled"
    mapperS["state"] = "disabled"
    bookmarkerB["state"] = "disabled"
    gmailerB["state"] = "disabled"
    mapperB["state"] = "disabled"
def Pressed2():
    map_osm = folium.Map(location=[dataY[6], dataY[7]], zoom_start=13)
    folium.Marker([dataY[6], dataY[7]], popup=dataY[0]).add_to(map_osm)
    map_osm.save("osm.html")
    webbrowser.open_new("osm.html")
def sendGMail2():
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("jojunhyeon414@gmail.com", "hdqpoawlyzvuitij")
    tmp = "※업소 이름: " + dataY[0] + "\n\n" + "※업소 분류: " + dataY[1] + "\n\n" + "※전화번호: " + dataY[2] + "\n\n" \
          + "※주소: " + dataY[3] + "\n\n" + "※설명: \n\n" + dataY[4] + "\n\n" + "※사진: " + dataY[5] + "\n\n"
    msg = MIMEText(tmp)
    msg["Subject"] = "숙박업소 검색 결과입니다."
    s.sendmail("jojunhyeon414@gmail.com", "bbb2632@naver.com", msg.as_string())
    s.quit()
def Pressed():
    map_osm = folium.Map(location=[dataX[6], dataX[7]], zoom_start=13)
    folium.Marker([dataX[6], dataX[7]], popup=dataX[0]).add_to(map_osm)
    map_osm.save("osm.html")
    webbrowser.open_new("osm.html")
    mapStatus = ""
def sendGMail():
    #tkinter.messagebox.showinfo("메일발송 완료!", "메일발송 완료!")
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("jojunhyeon414@gmail.com", "hdqpoawlyzvuitij")
    tmp = "※업소 이름: "+dataX[0]+"\n\n"+"※업소 분류: "+dataX[1]+"\n\n"+"※전화번호: "+dataX[2]+"\n\n" \
          +"※주소: "+dataX[3]+"\n\n"+"※설명: \n\n"+dataX[4]+"\n\n"+"※사진: "+dataX[5]+"\n\n"
    msg = MIMEText(tmp)
    msg["Subject"] = "숙박업소 검색 결과입니다."
    s.sendmail("jojunhyeon414@gmail.com", "bbb2632@naver.com", msg.as_string())
    s.quit()
def setBookmark():
    for e in subFrameB3.grid_slaves():
        e.destroy()

    for i in range(len(bookmarkDataList)):
        Button(subFrameB3, text=bookmarkDataList[i][0], bg="yellow", command=lambda x=i: showDetail2(x)).grid(row=i, column=0)
def saveBookmark():
    file = open("bookmark.txt", "w")
    for i in range(len(bookmarkDataList)):
        s = "★".join(bookmarkDataList[i])
        file.write(s)
        file.write("\n♩\n")
    file.close()
def loadBookmark():
    file = open("bookmark.txt", "r")
    s = file.readlines()
    ss = ""
    for e in s:
        if e == "♩\n" or e == "\n♩\n" or e == "\n♩" or e == "♩":
            bookmarkDataList.append(list(ss.split("★")))
            ss = ""
            continue
        ss += e
    file.close()
def deleteBookmark():
    for e in bookmarkDataList:
        if e[0] == dataY[0]:
            bookmarkDataList.remove(dataY)
            break
    tkinter.messagebox.showinfo("북마크 해제!", "북마크 해제!")
    setBookmark()
    saveBookmark()
def addBookmark():
    tkinter.messagebox.showinfo("북마크 완료!", "북마크 완료!")
    buttonList[idxX]["bg"] = "yellow"
    bookmarkDataList.append(dataX)
    saveBookmark()
    setBookmark()
def showDetail2(x):
    global dataY

    bookmarkerB["state"] = "normal"
    gmailerB["state"] = "normal"
    mapperB["state"] = "normal"

    RenderTextB.configure(state='normal')
    RenderTextB.delete(0.0, END)
    RenderTextB.insert(INSERT, "※업소 이름: ")
    RenderTextB.insert(INSERT, bookmarkDataList[x][0])
    RenderTextB.insert(INSERT, "\n\n")
    RenderTextB.insert(INSERT, "※업소 분류: ")
    RenderTextB.insert(INSERT, bookmarkDataList[x][1])
    RenderTextB.insert(INSERT, "\n\n")
    RenderTextB.insert(INSERT, "※전화번호: ")
    RenderTextB.insert(INSERT, bookmarkDataList[x][2])
    RenderTextB.insert(INSERT, "\n\n")
    RenderTextB.insert(INSERT, "※주소: ")
    RenderTextB.insert(INSERT, bookmarkDataList[x][3])
    RenderTextB.insert(INSERT, "\n\n")
    RenderTextB.insert(INSERT, "※설명: \n\n")
    RenderTextB.insert(INSERT, bookmarkDataList[x][4])
    if bookmarkDataList[x][6] == "-" or bookmarkDataList[x][7] == "-":
        RenderTextB.insert(INSERT, "\n\n")
        RenderTextB.insert(INSERT, "@ 지도는 제공되지 않습니다.")
    RenderTextS.configure(state='disabled')

    for e in imageFrameB.grid_slaves():
        e.destroy()

    try:
        raw_data = urllib.request.urlopen(bookmarkDataList[x][5]).read()
        im = Image.open(BytesIO(raw_data))
        imag = ImageTk.PhotoImage(im)
        imageLabel = Label(imageFrameB, image=imag, height=413, width=410)
        imageLabel.image = imag
        imageLabel.grid(row=1, column=0)
    except:
        pass
    dataY = bookmarkDataList[x]
def showImage(x):
    for e in imageFrameS.grid_slaves():
        e.destroy()

    try:
        raw_data = urllib.request.urlopen(dataList[x][5]).read()
        im = Image.open(BytesIO(raw_data))
        imag = ImageTk.PhotoImage(im)
        imageLabel = Label(imageFrameS, image=imag, height=404, width=404)
        imageLabel.image = imag
        imageLabel.grid(row=1, column=0)
    except:
        pass
def showDetail(x):
    global dataX, idxX

    bookmarkerS["state"] = "normal"
    gmailerS["state"] = "normal"
    mapperS["state"] = "normal"

    RenderTextS.configure(state='normal')
    RenderTextS.delete(0.0, END)
    RenderTextS.insert(INSERT, "※업소 이름: ")
    RenderTextS.insert(INSERT, dataList[x][0])
    RenderTextS.insert(INSERT, "\n\n")
    RenderTextS.insert(INSERT, "※업소 분류: ")
    RenderTextS.insert(INSERT, dataList[x][1])
    RenderTextS.insert(INSERT, "\n\n")
    RenderTextS.insert(INSERT, "※전화번호: ")
    RenderTextS.insert(INSERT, dataList[x][2])
    RenderTextS.insert(INSERT, "\n\n")
    RenderTextS.insert(INSERT, "※주소: ")
    RenderTextS.insert(INSERT, dataList[x][3])
    RenderTextS.insert(INSERT, "\n\n")
    RenderTextS.insert(INSERT, "※설명: \n\n")
    RenderTextS.insert(INSERT, dataList[x][4])
    if dataList[x][6] == "-" or dataList[x][7] == "-":
        RenderTextS.insert(INSERT, "\n\n")
        RenderTextS.insert(INSERT, "@ 지도는 제공되지 않습니다.")
    RenderTextS.configure(state='disabled')

    showImage(x)

    idxX = x
    #색칠하려고

    dataX = dataList[x]

init()
loadBookmark()
setBookmark()
initRenderText()

window.mainloop()
