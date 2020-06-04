from tkinter import *
from tkinter import font
import tkinter.ttk
import http.client
from xml.dom.minidom import parse, parseString
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO

window = Tk()
window.geometry("1280x720")
window.title("충남 숙박업소")

locList = ["검색", "천안", "공주", "보령", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성",\
           "예산", "태안"]
loc = ""
dataList = []

def init():
    global combobox, inputEntry, searchFrame, bookmarkFrame, subFrame, subFrame2, subFrame3

    notebook = tkinter.ttk.Notebook(window, width=1280, height=720)
    notebook.pack()
    searchFrame = Frame(window)
    notebook.add(searchFrame, text="검색")
    bookmarkFrame = Frame(window)
    notebook.add(bookmarkFrame, text="북마크")

    combobox = tkinter.ttk.Combobox(searchFrame, values=locList, width=36)
    combobox.grid(row=0, column=0)
    combobox.set("지역 선택")

    inputEntry = Entry(searchFrame, width=52)
    inputEntry.grid(row=0, column=1)
    click = Button(searchFrame, text="찾기", command=search)
    click.grid(row=0, column=1, sticky=E)

    subFrame = Frame(searchFrame)
    subFrame.grid(row=1, column=0)

    subFrame2 = Frame(searchFrame)
    subFrame2.grid(row=1, column=1)
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
                        dataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue, subitems[21].firstChild.nodeValue, \
                                         subitems[23].firstChild.nodeValue))
                    else:
                        if inputEntry.get() is not None and inputEntry.get() in subitems[7].firstChild.nodeValue:
                            pass
                        else:
                            continue
                        if subitems[17].firstChild is not None:
                            tel = subitems[17].firstChild.nodeValue
                        else:
                            tel = "-"
                        dataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue, subitems[21].firstChild.nodeValue, \
                                         subitems[23].firstChild.nodeValue))
            for e in subFrame.grid_slaves():
                e.destroy()
            Label(subFrame, text="\n<검색 결과>\n").grid(row=1, column=0)
            for i in range(len(dataList)):
                Button(subFrame, text=dataList[i][0], bg="light gray", \
                       command=lambda x=i: showDetail(x)).grid(row=i+2, column=0)
    else:
        print("parsing error")
def showDetail(x):
    RenderText2.configure(state='normal')
    RenderText2.delete(0.0, END)
    RenderText2.insert(INSERT, "※업소 이름: ")
    RenderText2.insert(INSERT, dataList[x][0])
    RenderText2.insert(INSERT, "\n\n")
    RenderText2.insert(INSERT, "※업소 분류: ")
    RenderText2.insert(INSERT, dataList[x][1])
    RenderText2.insert(INSERT, "\n\n")
    RenderText2.insert(INSERT, "※전화번호: ")
    RenderText2.insert(INSERT, dataList[x][2])
    RenderText2.insert(INSERT, "\n\n")
    RenderText2.insert(INSERT, "※주소: ")
    RenderText2.insert(INSERT, dataList[x][3])
    RenderText2.insert(INSERT, "\n\n")
    RenderText2.insert(INSERT, "※설명: \n\n")
    RenderText2.insert(INSERT, dataList[x][4])
    RenderText2.configure(state='disabled')
    
    url = dataList[x][5]
    print(url)
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    label = Label(searchFrame, image=image, width=413, height=275)
    label.place(x=800, y=55)
    """
    p = Image.open(dataList[x][5])
    img = ImageTk.PhotoImage(p)
    label = Label(searchFrame, image=img, width=413, height=275)
    label.place(x=800, y=55)
    """
def initRenderText():
    global RenderText2
    RenderText2 = Text(subFrame2, width=49, height=44, borderwidth=10, relief='ridge')
    RenderText2.pack()
    RenderText2.configure(state='disabled')

    bookmarker = Button(subFrame2, text="북마크", command=search)
    bookmarker.pack(side=RIGHT)
    gmailer = Button(subFrame2, text="G-mail", command=search)
    gmailer.pack(side=RIGHT)

init()
initRenderText()

window.mainloop()
