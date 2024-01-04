from tkinter import *
from PIL import Image,ImageTk
import pickle
import sklearn
import sqlite3
import time
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from tkinter import messagebox as ms
import re

model=pickle.load(open("Anaemia.pkl","rb"))

print("*************************** APP IS RUNNING PLEASE DON'T CLOSE THIS WINDOW  ********************************")
app=Tk()
app.title("Anaemia Prediction app")
app.geometry("800x600")
app.configure(background="skyblue")
bg_image=Image.open("Anaemia.jpg")
test_img=ImageTk.PhotoImage(bg_image)

bg_image1=Image.open("stop-anemia.jpg")
test_img1=ImageTk.PhotoImage(bg_image1)

bg_image2=Image.open("search.jpeg")
test_img2=ImageTk.PhotoImage(bg_image2)

e = 'T'+datetime.datetime.now().strftime('%d%m%y')


dbase=sqlite3.connect('Patient_Details.db')
dbase.execute(f'''CREATE TABLE IF NOT EXISTS
               {e}(
               Patient_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               NAME TEXT NOT NULL,
               GENDER TEXT NOT NULL,
               HEMOGLOBIN TEXT NOT NULL,
               MCH TEXT NOT NULL,
               MCHC TEXT NOT NULL,
               MCV TEXT NOT NULL,
               PREDICTED_RESULT TEXT NOT NULL)''')


Name=StringVar()
Hemoglobin=StringVar()
MCH=StringVar()
MCHC=StringVar()
MCV=StringVar()
GENDER=IntVar()



def submit():

    GENDERval=GENDER.get()
    Nameval=Name.get()
    Hemoglobinval=Hemoglobin.get()
    MCHval=MCH.get()
    MCHCval=MCHC.get()
    MCVval=MCV.get()


    if Nameval and Hemoglobinval and MCHval and MCVval and MCHCval:

    
        if float(Hemoglobinval)<=23.0 and float(MCHval)<=30.0 and float(MCVval)<=110.0 and float(MCHCval)<=36.0:
    
            result=model.predict([[Hemoglobinval,MCHval,MCHCval,MCVval,GENDERval]])
            result_percentage=model.predict_proba([[Hemoglobinval,MCHval,MCHCval,MCVval,GENDERval]])

            if result[0]==1:
                a='Anaemia'
                anaemia="{} % may {}".format(round(max(result_percentage[0])*100,2),a)
                butt2 = Button(app, text="STOP ANAEMIA",command=createNewWindow,font=("Bahnschrift",20),bg="#d4ca19",fg="#050505")
                butt2.grid(row=8,column=2,padx=15,pady=15)
            else:
                b='Not Anaemia'
                anaemia="{} % may {}".format(round(max(result_percentage[0])*100,2),b)
                butt2 = Button(app, text="STOP ANAEMIA",command=createNewWindow,state=DISABLED,font=("Bahnschrift",20),bg="#d4ca19",fg="#050505")
                butt2.grid(row=8,column=2,padx=15,pady=15)

            ans.configure(text=anaemia)
            
            ent2.delete(first=0,last=END)
            ent3.delete(first=0,last=END)
            ent4.delete(first=0,last=END)
            ent5.delete(first=0,last=END)
            ent6.delete(first=0,last=END)
            if GENDERval==0:
                output='Female'

            else:
                output='Male'
                
            dbase.execute(f'''INSERT INTO {e} (NAME,GENDER,HEMOGLOBIN,MCH,MCHC,
                                MCV,PREDICTED_RESULT
                               )VALUES(?,?,?,?,?,?,?)''',(Nameval,output,Hemoglobinval,MCHval,MCHCval,MCVval,anaemia))
                                                                        
                                                                        

            dbase.commit()

        else:
            ms.showerror("Error", "Out of range data's")

    else:
         ms.showerror("Error", "Fill all the data's")

def createNewWindow():
    newWindow = Toplevel(app)
    newWindow.title("STOP ANAEMIA")
    newWindow.geometry("600x500")

    
    bg_lb1=Label(newWindow,image=test_img1)
    bg_lb1.place(x=0,y=0,relwidth=1,relheight=1)
    newWindow.resizable(width=False,height=False)
    

date=StringVar()
p_id=StringVar()
    
    
def createNewWindow2():
    newWindow1 = Toplevel(app)
    newWindow1.title("STOP ANAEMIA")
    newWindow1.geometry("600x270")
    newWindow1.resizable(width=False,height=False)

    bg_lb2=Label(newWindow1,image=test_img2)
    bg_lb2.place(x=0,y=0,relwidth=1,relheight=1)



    def search():
        dateval=date.get()
        p_idval=p_id.get()

    
        x = re.search("\d\d-\d\d-\d\d", dateval)

        

        if dateval and p_idval:
            if x:
                dateval=dateval.replace('-','')
                dateval='T'+dateval



                cur=dbase.cursor()
                cur.execute(f"SELECT * FROM {dateval} WHERE Patient_ID=?",(p_idval,))
                data=cur.fetchone()

              
                data_id=data[0]
                data_name=data[1]
                data_gen=data[2]
                data_hemo=data[3]
                data_mch=data[4]
                data_mchc=data[5]
                data_mcv=data[6]
                data_result=data[7]
                data=f'''
                Patient_ID:{data_id}
                Name:{data_name}
                Gender:{data_gen}
                Hemoglobin:{data_hemo}
                MCH:{data_mch}
                MCHC:{data_mchc}
                MCV :{data_mcv}
                RESULT:{data_result}'''

                ent1.delete(first=0,last=END)
                ent2.delete(first=0,last=END)
                if data:
                    ms.showinfo('Search Result',data)
            else:
                ms.showerror('Error','Please Enter Correct Format')
        else:
            ms.showerror('Error','Please enter all data')
        
        
        

    lb1=Label(newWindow1,text="Enter Recorded Date",font=("Georgia",20),bg="black",fg="white",relief=RAISED)
    lb1.grid(row=0,column=0,padx=15,pady=15)
    ent1=Entry(newWindow1,textvariable=date,font=("bold",20),bg="#b8f0a5",fg="black",relief=RAISED,width=13)
    ent1.grid(row=0,column=1,padx=15,pady=15)


    lb2=Label(newWindow1,text="Enter Patient ID",font=("Georgia",20),bg="black",fg="white",relief=RAISED)
    lb2.grid(row=1,column=0,padx=15,pady=15)
    ent2=Entry(newWindow1,textvariable=p_id,font=("bold",20),bg="#b8f0a5",fg="black",relief=RAISED,width=13)
    ent2.grid(row=1,column=1,padx=15,pady=15)


    btn4=Button(newWindow1,command=search,text="Search",font=("bold",14),bg="green",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
    btn4.grid(row=2,column=1,padx=15,pady=15)



    
def quit_app():
    print('*********************************  APP CLOSED  ************************************')
    app.destroy()


bg_lb=Label(app,image=test_img)
bg_lb.place(x=0,y=0,relwidth=1,relheight=1)

lb1=Label(app,text="Enter the GENDER_level",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb1.grid(row=0,column=0,padx=15,pady=15)
Radiobutton(app, text="Male",variable=GENDER,value=1,font=("Georgia",22),bg="#b8f0a5",fg="black").grid(row=0,column=1,padx=15,pady=15)
Radiobutton(app, text="Female",variable=GENDER,value=0,font=("Georgia",22),bg="#b8f0a5",fg="black").grid(row=0,column=2,padx=15,pady=15)



lb2=Label(app,text="Enter the Hemoglobin_level",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb2.grid(row=2,column=0,padx=15,pady=15)
ent2=Entry(app,textvariable=Hemoglobin,font=("bold",22),bg="#b8f0a5",fg="black",relief=RAISED)
ent2.grid(row=2,column=1,padx=15,pady=15)



lb3=Label(app,text="Enter the MCH_level",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb3.grid(row=3,column=0,padx=15,pady=15)
ent3=Entry(app,textvariable=MCH,font=("bold",22),bg="#b8f0a5",fg="black",relief=RAISED)
ent3.grid(row=3,column=1,padx=15,pady=15)


lb4=Label(app,text="Enter the MCHC_level",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb4.grid(row=4,column=0,padx=15,pady=15)
ent4=Entry(app,textvariable=MCHC,font=("bold",22),bg="#b8f0a5",fg="black",relief=RAISED)
ent4.grid(row=4,column=1,padx=15,pady=15)


lb5=Label(app,text="Enter the MCV_level",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb5.grid(row=5,column=0,padx=15,pady=15)
ent5=Entry(app,textvariable=MCV,font=("bold",22),bg="#b8f0a5",fg="black",relief=RAISED)
ent5.grid(row=5,column=1,padx=15,pady=15)

lb6=Label(app,text="Patient Name",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb6.grid(row=1,column=0,padx=15,pady=15)
ent6=Entry(app,textvariable=Name,font=("bold",22),bg="#b8f0a5",fg="black",relief=RAISED)
ent6.grid(row=1,column=1,padx=15,pady=15)




lb8=Label(app,text="Predicted ",font=("Georgia",28),bg="black",fg="white",relief=RAISED)
lb8.grid(row=8,column=0,padx=15,pady=15)
ans=Label(app,font=("bold",26),width=25,bg="#e1e687",fg="red", relief=RAISED)
ans.grid(row=8,column=1,padx=15,pady=15)



btn1=Button(app,command=submit,text="submit",font=("bold",18),bg="green",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
btn1.grid(row=7,column=1,padx=15,pady=15)

btn3=Button(app,command=createNewWindow2,text="Quick Search",font=("bold",18),bg="green",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
btn3.grid(row=7,column=2,padx=15,pady=15)

btn4=Button(app,command=quit_app,text="Quit",font=("bold",18),bg="green",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
btn4.grid(row=9,column=2,padx=15,pady=15)

app.mainloop()




