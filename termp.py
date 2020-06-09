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

window = Tk()
window.geometry("1180x670")
window.title("충남 숙박업소")
window.resizable(False, False)

locList = ["검색", "천안", "공주", "아산", "서산", "논산", "당진", "금산", "부여", "서천", "청양", "홍성",\
           "예산", "태안", "보령"]
loc = ""
dataList = []
def init():
    global combobox, inputEntry, searchFrame, bookmarkFrame, \
        subFrame, subFrame2, subFrame3, subFrame4, subFrame5, subFrame6

    notebook = tkinter.ttk.Notebook(window, width=1180, height=670)
    notebook.pack()
    searchFrame = Frame(window)
    notebook.add(searchFrame, text="검색")
    bookmarkFrame = Frame(window)
    notebook.add(bookmarkFrame, text="북마크")

    subFrame = Frame(searchFrame)
    subFrame.grid(row=0, column=0)
    subFrame2 = Frame(searchFrame)
    subFrame2.grid(row=0, column=1)
    subFrame3 = Frame(searchFrame)
    subFrame3.grid(row=0, column=2)
    subFrame4 = Frame(searchFrame)
    subFrame4.grid(row=1, column=0)
    subFrame5 = Frame(searchFrame)
    subFrame5.grid(row=1, column=1)
    subFrame6 = Frame(searchFrame)
    subFrame6.grid(row=1, column=2)

    combobox = tkinter.ttk.Combobox(subFrame, values=locList, width=44)
    combobox.pack()
    combobox.set("지역 선택")

    inputEntry = Entry(subFrame2, width=44)
    inputEntry.grid(row=0, column=0)
    click = Button(subFrame2, text="찾기", command=search)
    click.grid(row=0, column=1)
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
                        dataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue, desc, i, w, k))
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
                        dataList.append((subitems[7].firstChild.nodeValue, subitems[5].firstChild.nodeValue, \
                                         tel, subitems[11].firstChild.nodeValue, desc, i, w, k))

            for e in subFrame4.grid_slaves():
                e.destroy()

            Label(subFrame4, text="\n<검색 결과>\n").grid(row=0, column=0)
            for i in range(len(dataList)):
                Button(subFrame4, text=dataList[i][0], bg="light gray", \
                       command=lambda x=i: showDetail(x)).grid(row=i+1, column=0)
    else:
        print("parsing error")
def initRenderText():
    global RenderText

    RenderText = Text(subFrame5, width=46, height=44, borderwidth=10, relief='ridge')
    RenderText.pack()
    RenderText.configure(state='disabled')

    bookmarker = Button(subFrame5, text="북마크", command=search)
    bookmarker.pack(side=RIGHT)
    gmailer = Button(subFrame5, text="G-mail", command=search)
    gmailer.pack(side=RIGHT)
def Pressed(y):
    map_osm = folium.Map(location=[y[0], y[1]], zoom_start=13)
    folium.Marker([y[0], y[1]], popup='충남숙박업소').add_to(map_osm)
    map_osm.save('osm.html')
    webbrowser.open_new('osm.html')
    mapStatus = ""
def showDetail(x):
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

    for e in subFrame3.pack_slaves():
        e.destroy()

    mapButton = Button(subFrame3, text="지도보기", command=lambda y=(dataList[x][6], dataList[x][7]): Pressed(y))
    mapButton.pack()

    for e in subFrame6.pack_slaves():
        e.destroy()

    #url="http://tour.chungnam.go.kr/Upl/kr/stay/thm_54.jpg"
    if dataList[x][5] != "-":
        url = dataList[x][5]
        #print(url)
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im)
        imLabel = Label(subFrame6, image=image, height=350, width=350)
        imLabel.pack()
    else:
        pass

init()
initRenderText()

window.mainloop()
