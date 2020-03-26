'''
@Author: YuleZhang
@Description: 一个新闻分析展示页面
@Date: 2020-03-16 21:32:49
'''
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd

root = Tk()
root.geometry("700x700")#定义总布局大小
root.resizable(width=False, height=False)#界面大小不可调整
root.title('通信行业新闻分析系统')
#图片部分框架
lbPic=LabelFrame(root, width=537, height=412)
lbPic.grid(row=0,column=0)
#显示部分框架
sendfm = Frame(root, width = 700, height=40)
sendfm.grid(row=1,column=0)
#新闻记录表表头
lbhead = LabelFrame(root, width = 700, height = 50, padx=50)
lbhead.grid(row=2,column=0)
#新闻记录表数据
lbdata = Frame(root, width = 700, height = 160, padx=50)
lbdata.grid(row=3,column=0)

i = 0
def tableRead():
    # 选择并读取文件
    file_path = filedialog.askopenfilename(filetypes = [('CSV', 'csv')])
    if(file_path):
        info=pd.read_csv(file_path,encoding = 'gbk')
        for j,data in info.iterrows():
            addRow(data)
            # 受窗体大小限制，仅显示十条记录
            if j > 10:
                break

def addRow(info):
    # 每次在窗体中添加一条新闻记录
    global i
    hand_content = str(info['content']).replace('\u3000','').strip()
    Label(lbdata, text=info['title'][:12]).place(x=-50,y=20*i)
    Label(lbdata, text=hand_content[:20]).place(x=120,y=20*i)
    Label(lbdata, text=info['date']).place(x=380,y=20*i)
    Label(lbdata, text=info['source']).place(x=520,y=20*i)
    i = i + 1

if __name__ == "__main__":
    img = Image.open('img/sample.png')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    imglabel = Label(lbPic, image=photo)
    imglabel.place(x=0,y=0)
    #加载按钮
    btn = Button(sendfm,text="加载",command=tableRead,width=15)
    btn.place(x=320,y=5)
    Label(lbhead, text="标题").place(x=0,y=12)
    Label(lbhead, text="内容").place(x=200,y=12)
    Label(lbhead, text="日期").place(x=380,y=12)
    Label(lbhead, text="来源").place(x=500,y=12)
    # Label(lbhead, text="链接").place(x=500,y=12)
    mainloop()
