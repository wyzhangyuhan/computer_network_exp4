from tkinter import *
from  tkinter  import ttk 
from baidutrans import BaiduTranslate

class Translate(object):
    def __init__(self):
        self.root = Tk()
        self.root.geometry('400x190')
        self.root.title('弘牛翻译')

        comvalue = StringVar()
        self.comboxlist=ttk.Combobox(self.root,textvariable=comvalue)
        self.comboxlist["values"]=("中文","英文","日文","西班牙语")  
        self.comboxlist.current(0)  #选择第一个  
        # self.comboxlist.bind("<<ComboboxSelected>>",self.go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        self.comboxlist.pack() 
        self.comboxlist.place(relx=0.15,rely=0.03, relwidth=0.3, relheight=0.15)
        self.comboxlist.current(0)

        w1 = Label(self.root, text="源语言")
        w1.place(relx=0.03,rely=0.03, relwidth=0.1, relheight=0.15)
        w2 = Label(self.root, text="目的语言")
        w2.place(relx=0.45,rely=0.03, relwidth=0.15, relheight=0.15)

        comvalue = StringVar()
        self.comboxlist2=ttk.Combobox(self.root,textvariable=comvalue)
        self.comboxlist2["values"]=("中文","英文","日文","西班牙语")  
        self.comboxlist2.current(0)  #选择第一个  
        # self.comboxlist2.bind("<<ComboboxSelected>>",self.go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        self.comboxlist2.pack() 
        self.comboxlist2.place(relx=0.6,rely=0.03, relwidth=0.3, relheight=0.15)
        self.comboxlist2.current(0)

        #输入框
        self.inp1 = Entry(self.root,font=('华文新魏',11))
        self.inp1.place(relx=0.03,rely=0.2, relwidth=0.79, relheight=0.15)

        # ‘翻译’按钮，直接调用 run1()
        btn1 = Button(self.root,font=('华文新魏',11), text='翻译',background='#CA0316',foreground='white',activebackground='red',activeforeground='white', command=self.get_information)
        btn1.place(relx=0.82, rely=0.2, relwidth=0.15, relheight=0.15)

        # 输出文本框
        self.txt = Text(self.root,font=('华文新魏',11))
        self.txt.place(relx=0.03,rely=0.357, relwidth=0.938,relheight=0.5,)
    
    def go(self, *args):   #处理事件，*args表示可变参数  
        print(self.comboxlist.get()) #打印选中的值  

    def judge_type(self, string):
        if string == '中文':
            return 'zh'
        elif string == '英文':
            return 'en'
        elif string == '日文':
            return 'jp'
        elif string == '西班牙语':
            return 'spa'

    def get_information(self):
        self.txt.delete('0.0', END)
        str1 = self.judge_type(self.comboxlist.get())
        str2 = self.judge_type(self.comboxlist2.get())
        str3 = self.inp1.get()
        tmp_str = []
        tmp_str.append(str1)
        tmp_str.append(str2)
        tmp_str.append(str3)

        BaiduTranslate_test = BaiduTranslate(str1,str2)
        (status, Results) = BaiduTranslate_test.BdTrans(str3)#要翻译的词组
        print(Results)
        self.txt.insert(END, Results)
        return tmp_str


    
    def main(self):
        self.root.mainloop()

if __name__ == '__main__':
    tmp = Translate()
    tmp.main()
