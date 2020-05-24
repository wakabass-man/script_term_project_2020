from tkinter import *

window = Tk()
window.title("전라남도 숙박 업소")
window.geometry("600x360")

frame0 = Frame(window)
frame0.grid(row=0, column=0)
Button(frame0, text="검색").pack(side="left")
Button(frame0, text="북마크").pack(side="left")
Label(frame0, width=40).pack(side="left")

frame1 = Frame(window)
frame1.grid(row=1, column=0)
Label(frame1, text="    시").pack(side="left")
locEntry = Entry(frame1, width=8)
locEntry.pack(side="left")
Label(frame1, text="    이름").pack(side="left")
searchEntry = Entry(frame1, width=25)
searchEntry.pack(side="left")
Button(frame1, text="찾기").pack(side="left")

frame2 = Frame(window)
frame2.grid(row=2, column=0)
frame3 = Frame(window)
frame3.grid(row=2, column=1)

Label(frame2).grid(row=0, column=0)
for i in range(10):
    Button(frame2, text="숙박업소"+str(i)).grid(row=i+1, column=0)
    Button(frame2, text="★").grid(row=i+1, column=1)

Label(frame3, text="숙박업소 사진").pack()
Label(frame3, text="숙박업소 이름").pack()
Label(frame3, text="분류(호텔/펜션/민박)").pack()
Label(frame3, text="숙박업소 전화번호").pack()
Label(frame3, text="숙박업소 위치").pack()
Label(frame3, text="숙박업소 지도").pack()
Button(frame3, text="Gmail").pack()

window.mainloop()