#Flutter uygulaması ile iletişim kurabilmek için gerekli kütüphaneler import ediliyor.
from flask import Flask, jsonify, request
import json

#breathbot.py sayfasında bulunan breathBotCevap fonksiyonunu tanımlıyoruz.
#Chatbotun vereceği cevabı bu fonksiyon ile alıyoruz.
from breathbot import breathBotCevap

#Yeni bir atama için boş bir değişken tanımlıyoruz.
response = ''

#Flask ile uygulama örneği oluşturuyoruz.
app = Flask(__name__)

#Gönderimizi  ve flutter uygulamamızdan veri almak için rota oluşturuyoruz.
@app.route('/chat', methods = ['GET', 'POST'])


def chatRoute():
    
    #Genel yanıt değişkeni alıyoruz.
    global response

    #Flutter uygulamasının isteğini kontrol ediyoruz.
    #Yani veri gönderme veya veri alma istekleri kontrol edilmektedir.
    if(request.method == 'POST'):
        #Verileri değişkene atıyoruz
        tempRequest = request.data
        #Değişkene atılan verilerin dönüşümü yapılmaktadır.
        tempRequest = json.loads(tempRequest.decode('utf-8'))
        #Dönüşüm verisi içeriği değişkene atanıyor.
        chat = tempRequest['chat']
        #Burada flutter uygulamasından gelen verinin boş olup olmadığı kontrol edilmektedir.
        if chat == '':
            response = 'Mesaj içeriğiniz boş olamaz. Lütfen içeriğinizi kontrol ederek tekrar deneyiniz.'
        else:
            #Chatbotun verdiği cevap değişkene atanmaktadır.
            response = f'{breathBotCevap(chat)}'
        return " "
    else:
        #Flutter uygulamamıza veriyi gönderiyoruz.
        return jsonify({'chat' : response})

if __name__ == "__main__":
    app.run(debug=True)

