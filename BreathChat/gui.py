from tkinter import *

from breathbot import breathBotCevap, botName

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("BreathBot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")
        
        #GUI Etiketini Belirliyoruz.
        head_label = Label(self.window, bg="#17202A", fg="#EAECEE",
                           text="Hoşgeldiniz", font="Helvetica 12", pady=10)
        head_label.place(relwidth=1)
        
        line = Label(self.window, width=450, bg="#ABB2B9")
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        #Yazıları Düzenliyoruz.
        self.text = Text(self.window, width=20, height=2, bg="#17202A", fg="#EAECEE",
                                font="Helvetica 12", padx=5, pady=5)
        self.text.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text.configure(cursor="arrow", state=DISABLED)
        
        #ScroolBar Ekliyoruz.
        scrollbar = Scrollbar(self.text)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text.yview)
        
        #Alt kısmı düzenliyoruz.
        bottomTap = Label(self.window, bg="#ABB2B9", height=80)
        bottomTap.place(relwidth=1, rely=0.825)
        
        #Mesaj Kısmını Tasarlıyoruz.
        self.mesajGiris = Entry(bottomTap, bg="#2C3E50", fg="#EAECEE", font="Helvetica 12")
        self.mesajGiris.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.mesajGiris.focus()
        self.mesajGiris.bind("<Return>", self._on_enter_pressed)
        
        #Chatbota veri gönderebilmek için Gönder butonu oluşturuyoruz.
        send_button = Button(bottomTap, text="Gönder", font= "Helvetica 12", width=20, bg="#ABB2B9",
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
    def _on_enter_pressed(self, event):
        mesaj = self.mesajGiris.get()
        self._insert_message(mesaj, "Siz")
        
    def _insert_message(self, mesaj, gonder):
        if not mesaj:
            return
        
        self.mesajGiris.delete(0, END)
        tempMesaj = f"{gonder}: {mesaj}\n\n"
        self.text.configure(state=NORMAL)
        self.text.insert(END, tempMesaj)
        self.text.configure(state=DISABLED)
        
        tempMesaj2 = f"{botName}: {breathBotCevap(mesaj)}\n\n"
        self.text.configure(state=NORMAL)
        self.text.insert(END, tempMesaj2)
        self.text.configure(state=DISABLED)
        
        self.text.see(END)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()