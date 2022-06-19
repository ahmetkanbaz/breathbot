import random
import json
import pickle
import numpy as np

import nltk

from keras.models import load_model

from snowballstemmer import stemmer

#Stemmer işlemi yani kök bulma işlemi için Türkçe stemmer import ediyoruz.
kokAl = stemmer('turkish')

#Chatbotumuzun adını belirliyoruz.
botName = 'BreathBot'

#Corpusumuzun olduğu json dosyasını açıyoruz.
with open("corpus.json", encoding="utf8") as file:
    jsonIntents = json.load(file)

tumKelimeler = pickle.load(open('tumKelimeler.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('breathbot_model.h5')


#Cümleyi veya kullanıcının girdisini temizlemek için gerekli fonksiyonu yazıyoruz.
def cumleTemizle(cumle):
    #Cümlede bulunan kelimeleri ayırıyoruz.
    cumleKelimeler = nltk.word_tokenize(cumle)
    #Kelimelerin kökleri alınarak küçük harflere dönüştürülüyor.
    cumleKelimeler = [kokAl.stemWord(w.lower()) for w in cumleKelimeler]
    return cumleKelimeler



def cantaKelime(cumle, kelimeler):
    #Fonksiyona alınan veri 'cumleTemizle' fonksiyonuna gönderilerek kelimere ayrılması ve küçük harf olması sağlandı.
    cumleKelime = cumleTemizle(cumle)
    canta = [0] * len(kelimeler)
    for w in cumleKelime:
        for i, w2 in enumerate(kelimeler):
            if w2 == w:
                canta[i] = 1
    return np.array(canta)


def sinifTahmini(cumle, model):
    tempBag = cantaKelime(cumle, tumKelimeler)#Tahmin datasını alıyoruz.
    res = model.predict(np.array([tempBag]))[0]#Tahmin haritasını modelimize gönderiyoruz.
    error = 0.25
    sonuc = [[i, r] for i, r in enumerate(res) if r > error]
    
    sonuc.sort(key=lambda x: x[1], reverse=True)
    listSonuc = []
    for r in sonuc:
        listSonuc.append({'intent': classes[r[0]], 'probability': str(r[1])})#Olasılık ve intent değişkene atanıyor.
    return listSonuc


def sonucAl(listIntents, tempIntent):
    etiket = listIntents[0]['intent']
    tempListIntents = tempIntent['intents']
    for i in tempListIntents:
        if i['tag'] == etiket:
            sonuc = random.choice(i['responses'])
            break
    return sonuc

def breathBotCevap(text):
    tempInt = sinifTahmini(text, model)
    tempProbability = tempInt[0]['probability']
    if float(tempProbability) > 0.70: #Doğruluk oranı yani benzerlik oranı %70'in üstünde ise json dosyasından veri alır.
        res = sonucAl(tempInt, jsonIntents)
    else:#%70'in altında ise kullanıcıyı anlamadığını belirtir.
        res = 'Ne demek istediğinizi anlayamadım. Lütfen tekrar eder misiniz?'
    return res

def breathBotChat():
    while True:
        inputUsers = input('Siz: ')
        if inputUsers.lower() == 'quit':
            print(f'{botName}: Çıkış yapılıyor...')
            break
        
        if inputUsers.lower() == '' or inputUsers.lower() == '*':
            print('İfadenizi kontrol ederek lütfen tekrar deneyiniz.')
        
        else:
            print(f'{botName}: {breathBotCevap(inputUsers)}')

#breathBotChat()