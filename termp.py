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

window = Tk()
window.geometry("1552x670+0+0")
window.title("충남 관광지 숙박업소")
window.resizable(False, False)

locList = ["검색", "천안", "공주", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성",\
           "예산", "태안", "보령"]
loc = ""
dataList = []
dataX = []
bookmarkDataList = []
buttonList = []
idxX = 0
def init():
    global combobox, inputEntry, searchFrame, bookmarkFrame, noPhotoLabel,\
        subFrame, subFrame2, subFrame4, subFrame5, textFrame, imageFrame

    notebook = tkinter.ttk.Notebook(window, width=1080, height=670)
    notebook.pack()
    searchFrame = Frame(window)
    notebook.add(searchFrame, text="검색")
    bookmarkFrame = Frame(window)
    notebook.add(bookmarkFrame, text="북마크")

    textFrame = Frame(searchFrame)
    textFrame.pack(side=LEFT)
    imageFrame = Frame(searchFrame)
    imageFrame.pack(side=LEFT)

    subFrame = Frame(textFrame)
    subFrame.grid(row=0, column=0)
    subFrame2 = Frame(textFrame)
    subFrame2.grid(row=0, column=1)
    subFrame4 = Frame(textFrame)
    subFrame4.grid(row=1, column=0)
    subFrame5 = Frame(textFrame)
    subFrame5.grid(row=1, column=1)

    combobox = tkinter.ttk.Combobox(subFrame, values=locList, width=44)
    combobox.pack()
    combobox.set("지역 선택")

    inputEntry = Entry(subFrame2, width=44)
    inputEntry.grid(row=0, column=0)

    click = Button(subFrame2, text="찾기", command=search)
    click.grid(row=0, column=1)

    noPhotoLabel = Label(imageFrame, text="")
    noPhotoLabel.grid(row=0, column=0)
def search():
    global loc, locList, dataList

    loc = combobox.get()

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
                        if inputEntry.get() is not None and inputEntry.get() in subitems[7].firstChild.nodeValue:
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

            for e in subFrame4.grid_slaves():
                e.destroy()
            buttonList.clear()

            Label(subFrame4, text="\n<검색 결과>\n").grid(row=0, column=0)
            for i in range(len(dataList)):
                button = Button(subFrame4, text=dataList[i][0], bg="light gray", \
                       command=lambda x=i: showDetail(x))
                button.grid(row=i+1, column=0)
                buttonList.append(button)
    else:
        print("parsing error")
def initRenderText():
    global RenderText

    RenderText = Text(subFrame5, width=46, height=44, borderwidth=10, relief='ridge')
    RenderText.pack()
    RenderText.configure(state='disabled')

    bookmarker = Button(subFrame5, text="북마크", command=setBookmark)
    bookmarker.pack(side=RIGHT)
    gmailer = Button(subFrame5, text="G-mail", command=sendGMail)
    gmailer.pack(side=RIGHT)
    mapper = Button(subFrame5, text="지도보기", command=Pressed)
    mapper.pack(side=RIGHT)
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
    tmp = "※업소 이름: "+dataX[0]+"\n\n"+"※업소 분류: "+dataX[1]+"\n\n"+"※전화번호: "+dataX[2]+"\n\n"\
          +"※주소: "+dataX[3]+"\n\n"+"※설명: \n\n"+dataX[4]+"\n\n"+"※사진: "+dataX[5]+"\n\n"
    msg = MIMEText(tmp)
    msg["Subject"] = "숙박업소 검색 결과입니다."
    s.sendmail("jojunhyeon414@gmail.com", "bbb2632@naver.com", msg.as_string())
    s.quit()
def setBookmark():
    tkinter.messagebox.showinfo("북마크 완료!", "북마크 완료!")
    bookmarkDataList.append(dataX)
    buttonList[idxX]["bg"] = "yellow"
def showImage(x):
    for e in imageFrame.grid_slaves():
        e.destroy()
    try:
        raw_data = urllib.request.urlopen(dataList[x][5]).read()
        im = Image.open(BytesIO(raw_data))
        imag = ImageTk.PhotoImage(im)
        imageLabel = Label(imageFrame, image=imag, height=404, width=404)
        imageLabel.image = imag
        imageLabel.grid(row=1, column=0)
    except:
        noPhotoLabel.configure(text="사진을 제공하지 않는 숙박업소입니다.")
def showDetail(x):
    global dataX, idxX

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    RenderText.insert(INSERT, "※업소 이름: ")
    RenderText.insert(INSERT, dataList[x][0])
    RenderText.insert(INSERT, "\n\n")
    RenderText.insert(INSERT, "※업소 분류: ")
    RenderText.insert(INSERT, dataList[x][1])
    RenderText.insert(INSERT, "\n\n")
    RenderText.insert(INSERT, "※전화번호: ")
    RenderText.insert(INSERT, dataList[x][2])
    RenderText.insert(INSERT, "\n\n")
    RenderText.insert(INSERT, "※주소: ")
    RenderText.insert(INSERT, dataList[x][3])
    RenderText.insert(INSERT, "\n\n")
    RenderText.insert(INSERT, "※설명: \n\n")
    RenderText.insert(INSERT, dataList[x][4])
    if dataList[x][6] == "-" or dataList[x][7] == "-":
        RenderText.insert(INSERT, "\n\n")
        RenderText.insert(INSERT, "@ 지도는 제공되지 않습니다.")
    RenderText.configure(state='disabled')

    showImage(x)

    idxX = x

    dataX = dataList[x]

init()
initRenderText()

window.mainloop()
