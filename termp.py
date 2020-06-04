from tkinter import *
from tkinter import font
import tkinter.messagebox
window = Tk()
window.geometry("400x600+750+200")
DataList = []
loc = ""
locList = ["검색", "천안", "공주", "보령", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성",\
           "예산", "태안"]
def InitTopText():
    TempFont = font.Font(window, size=20, weight='bold', family='Consolas')
    MainText = Label(window, font=TempFont, text="[충남 숙박업소 검색]")
    MainText.place(x=20)
def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(window)
    ListBoxScrollbar.place(x=150, y=50)
    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(window, font=TempFont, activestyle='none', width=10, height=1,
                            borderwidth=12, relief='ridge', yscrollcommand=ListBoxScrollbar.set)
    SearchListBox.insert(0, "검색")
    SearchListBox.insert(1, "천안")
    SearchListBox.insert(2, "공주")
    SearchListBox.insert(3, "보령")
    SearchListBox.insert(4, "아산")
    SearchListBox.insert(5, "서산")
    SearchListBox.insert(6, "논산")
    SearchListBox.insert(7, "당진")
    SearchListBox.insert(8, "금산")
    SearchListBox.insert(9, "부여")
    SearchListBox.insert(10, "서천")
    SearchListBox.insert(11, "청양")
    SearchListBox.insert(12, "홍성")
    SearchListBox.insert(13, "예산")
    SearchListBox.insert(14, "태안")
    SearchListBox.place(x=10, y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)
def InitInputLabel():
    global InputLabel
    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    InputLabel = Entry(window, font=TempFont, width=26, borderwidth=12, relief='ridge')
    InputLabel.place(x=10, y=105)
def InitSearchButton():
    TempFont = font.Font(window, size=12, weight='bold', family='Consolas')
    SearchButton = Button(window, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.place(x=330, y=110)
def SearchButtonAction():
    global SearchListBox, locList, loc
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = SearchListBox.curselection()[0]
    loc = locList[iSearchIndex]
    Search()
    RenderText.configure(state='disabled')
def Search():
    import urllib
    import http.client
    from xml.dom.minidom import parse, parseString
    from io import BytesIO
    import urllib.request
    from PIL import Image, ImageTk
    conn = http.client.HTTPConnection("tour.chungnam.go.kr")
    conn.request("GET", "/_prog/openapi/?func=stay&start=0&end=150")
    req = conn.getresponse()
    global DataList, loc
    DataList.clear()
    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("normal error")
        else:
            parseData = parseString(BooksDoc)
            item_info = parseData.childNodes
            row = item_info[0].childNodes
            for item in row:              #row = <item>
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
                        DataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue))
                    else:
                        if InputLabel.get() in subitems[7].firstChild.nodeValue:
                            pass
                        else:
                            continue
                        if subitems[17].firstChild is not None:
                            tel = subitems[17].firstChild.nodeValue
                        else:
                            tel = "-"
                        DataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue))
            for i in range(len(DataList)):
                RenderText.insert(INSERT, "[")
                RenderText.insert(INSERT, i + 1)
                RenderText.insert(INSERT, "] ")
                RenderText.insert(INSERT, "시설명: ")
                RenderText.insert(INSERT, DataList[i][0])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "업소 분류: ")
                RenderText.insert(INSERT, DataList[i][1])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "전화번호: ")
                RenderText.insert(INSERT, DataList[i][2])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "주소: ")
                RenderText.insert(INSERT, DataList[i][3])
                RenderText.insert(INSERT, "\n\n")
    else:
        print("parsing error")
def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(window)
    RenderTextScrollbar.place(x=375, y=200)
    TempFont = font.Font(window, size=10, family='Consolas')
    RenderText = Text(window, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')
InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
window.mainloop()
