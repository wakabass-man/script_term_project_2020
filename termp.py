from tkinter import *
from tkinter import font
import tkinter.ttk
window = Tk()
window.geometry("1600x800")
window.title("충남 숙박업소")

locList = ["검색", "천안", "공주", "보령", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성",\
           "예산", "태안"]
loc = ""
dataList = []
def init():
    global combobox, inputEntry, frame1, frame2
    notebook = tkinter.ttk.Notebook(window, width=1600, height=900)
    notebook.pack()

    frame1 = Frame(window)
    notebook.add(frame1, text="검색")

    frame2 = Frame(window)
    notebook.add(frame2, text="북마크")

    combobox = tkinter.ttk.Combobox(frame1, values=locList)
    combobox.grid(row=0, column=0)
    combobox.set("지역 선택")

    inputEntry = Entry(frame1)
    inputEntry.grid(row=0, column=1)

    click = Button(frame1, text="찾기", command=search)
    click.grid(row=0, column=2)
def search():
    global loc, locList, dataList
    loc = combobox.get()
    import http.client
    from xml.dom.minidom import parse, parseString
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
                                         tel, subitems[11].firstChild.nodeValue))
                    else:
                        if inputEntry.get() in subitems[7].firstChild.nodeValue:
                            pass
                        else:
                            continue
                        if subitems[17].firstChild is not None:
                            tel = subitems[17].firstChild.nodeValue
                        else:
                            tel = "-"
                        dataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue))
            for i in range(len(dataList)):
                Button(frame1, text=dataList[i][0], command=lambda x=i: showDetail(x)).grid(row=i+1, column=0)
    else:
        print("parsing error")
def showDetail(x):
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    RenderText.insert(INSERT, "업소명: ")
    RenderText.insert(INSERT, dataList[x][0])
    RenderText.insert(INSERT, "\n")
    RenderText.insert(INSERT, "업소 분류: ")
    RenderText.insert(INSERT, dataList[x][1])
    RenderText.insert(INSERT, "\n")
    RenderText.insert(INSERT, "전화번호: ")
    RenderText.insert(INSERT, dataList[x][2])
    RenderText.insert(INSERT, "\n")
    RenderText.insert(INSERT, "주소: ")
    RenderText.insert(INSERT, dataList[x][3])
    RenderText.insert(INSERT, "\n")
    RenderText.configure(state='disabled')
def initRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(frame1)
    RenderTextScrollbar.place(x=375, y=200)
    TempFont = font.Font(window, size=10, family='Consolas')
    RenderText = Text(frame1, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.place(x=700, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderText.configure(state='normal')
    print(type(RenderText))

init()
initRenderText()

window.mainloop()
