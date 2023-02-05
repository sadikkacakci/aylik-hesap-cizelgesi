from tkinter import *
import pandas as pd
from datetime import datetime
from tkinter import messagebox
from tkinter.messagebox import askyesno

def initializeRoot():
    root = Tk()
    root.title("Aylık Hesap")
    root.geometry("300x300")
    return root

class Hesap:
    def __init__(self):
        self.root = initializeRoot()
        self.entries = []

    def run(self):
        kira_label = Label(self.root, text='Kira', font=('calibre', 10, 'bold'))
        kira_entry = Entry(self.root, width=20, fg="black", bg="white",borderwidth=2, font=("Arial", 10))
        self.entries.append(kira_entry)

        elektrik_label = Label(self.root, text='Elektrik', font=('calibre', 10, 'bold'))
        elektrik_entry = Entry(self.root, width=20, fg="black",bg="white", borderwidth=2, font=("Arial", 10))
        self.entries.append(elektrik_entry)

        su_label = Label(self.root, text='Su', font=('calibre', 10, 'bold'))
        su_entry = Entry(self.root, width=20, fg="black", bg="white",borderwidth=2, font=("Arial", 10))
        self.entries.append(su_entry)

        internet_label = Label(self.root, text='İnternet', font=('calibre', 10, 'bold'))
        internet_entry = Entry(self.root, width=20, fg="black",bg="white", borderwidth=2, font=("Arial", 10))
        self.entries.append(internet_entry)

        clear_button = Button(self.root, text="Temizle", height=2, width=10,fg="black", bg="white", font=("Arial", 10), command=lambda : self.clearEntries())

        push_button = Button(self.root, text="Kaydet", height=2, width=10,fg="black", bg="white", font=("Arial", 10), command=lambda : self.pushFile())

        kira_label.grid(row=0, column=0)
        kira_entry.grid(row=0, column=1)

        elektrik_label.grid(row=1, column=0)
        elektrik_entry.grid(row=1, column=1)

        su_label.grid(row=2, column=0)
        su_entry.grid(row=2, column=1)

        internet_label.grid(row=3, column=0)
        internet_entry.grid(row=3, column=1)
        
        clear_button.place(relx=0.2, rely=0.4)
        push_button.place(relx=0.5, rely=0.4)

        self.root.mainloop()

    def clearEntries(self):
        for entry in self.entries:
            entry.delete(0,"end")
    
    def getTime(self):
        current_time = datetime.now()
        month = current_time.month
        if(current_time.month < 10):
            month = "0" + str(current_time.month)
        date = str(month) + "/" + str(current_time.year)
        return date

    def pushFile(self):
        self.checkExcelFile()
        if(self.checkEntries()):
            entry_values = []
            date = self.getTime()
            if(self.checkDates(date)):
                entry_values.append([date])
                for entry in self.entries:
                    entry_values.append([entry.get()])
                df = pd.read_excel("cizelge.xlsx")
                entries_df = pd.DataFrame(data =entry_values)
                entries_df = entries_df.transpose()
                entries_df.columns = ["tarih","kira","elektrik","su","internet"]
                df = df.append(entries_df)
                try:
                    df.to_excel("cizelge.xlsx",index=None)
                    messagebox.showinfo("Başarılı",'Veri başarıyla kaydedildi.')
                    self.clearEntries()
                except:
                    messagebox.showwarning("Hata",'Veri kaydedilemedi.')
    
    def overWrite(self,number):
        answer = askyesno(title="Doğrulama",message="Bu tarihe ait kayıtlı bir veri var, üstüne yazmak ister misiniz?")
        if(answer):
            df = pd.read_excel("cizelge.xlsx")
            temp_list = []
            temp_list.append(self.getTime())
            for entry in self.entries:
                temp_list.append(entry.get())
            try:
                df.iloc[number] = temp_list
                df.to_excel("cizelge.xlsx",index=None)
                messagebox.showinfo("Başarılı",'Veri başarıyla üstüne yazıldı.')
                self.clearEntries()
            except:
                messagebox.showwarning("Hata",'Veri kaydedilemedi.')

    def checkDates(self,date):
        df = pd.read_excel("cizelge.xlsx")
        if(len(df) == 0):
            return True
        for number in range(df.shape[0]):
            savedDate = df.iloc[number]["tarih"]
            if (str(date) == str(savedDate)):
                self.overWrite(number)
                return False
        return True

    def checkEntries(self):
        for entry in self.entries:
            if(len(entry.get()) == 0):
                messagebox.showwarning(title="Hata",message="Boş alan bırakmayınız.")
                return False
            try:
                int(entry.get())
            except Exception:
                messagebox.showwarning(title="Hata",message="Sadece sayısal değer giriniz.")
                return False
        return True

    def checkExcelFile(self):
        import os 
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file=="cizelge.xlsx":
                return True
        df = pd.DataFrame()
        df.to_excel(cwd + "/cizelge.xlsx",index=None)
        print(f"cizelge.xlsx dosyası {cwd} yolunda oluşturuldu.")

hesap = Hesap()
hesap.run()