#Kullanılacak olan kütüphaneler import ediliyor.
import random
import json
import pickle
import numpy as np
import nltk
from tensorflow import keras
from tensorflow import _keras_module
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from keras.models import load_model
import warnings
warnings.filterwarnings('ignore')

from snowballstemmer import stemmer
#Stemmer işlemi yani kök bulma işlemi için Türkçe stemmer import ediyoruz.
kokAl = stemmer('turkish')

tumKelimeler = []
classes = []
documents = []

ignoreNoktalama = ['?', '!', '.', ',']

with open("corpus.json", encoding="utf8") as file:
    jsonIntents = json.load(file)


#Veri ön işleme kısmıdır. Verilerin değiştirilmesi veya bırakılması kısmıdır.
#Boş listeleri, kelimeleri ve sınıfları güncellemekteyiz.
for intent in jsonIntents['intents']:
    for pattern in intent['patterns']:
        kelimeler = nltk.word_tokenize(pattern)#Büyük metin veya cümleleri kelimelere bölüyoruz.
        tumKelimeler.extend(kelimeler)
        tempIntent = intent['tag']
        documents.append((kelimeler, tempIntent))
        #classes listemize ekleme yapıyoruz.
        if tempIntent not in classes:
            classes.append(tempIntent)

#stem işlemi, kelimelerin çekimli biçimlerinin tek kelimede gruplanmasıdır.
#Yani, alıngan sözcüğü almak olur.
tumKelimeler = [kokAl.stemWord(w.lower()) for w in tumKelimeler if w not in ignoreNoktalama]
tumKelimeler = sorted(list(set(tumKelimeler)))

classes = sorted(list(set(classes)))


pickle.dump(tumKelimeler, open('tumKelimeler.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outTemp = [0] * len(classes)

for tempDoc in documents:
    canta = []
    
    kelime = tempDoc[0]
    kelime = [kokAl.stemWord(w.lower()) for w in kelime]
    
    for w in tumKelimeler:
        canta.append(1) if w in kelime else canta.append(0)
    
    outRow = list(outTemp)
    outRow[classes.index(tempDoc[1])] = 1
    training.append([canta, outRow])

random.shuffle(training)
training = np.array(training)

X_train = list(training[:, 0])
Y_train = list(training[:, 1])

#Yukarıdaki işlemler ile eğitim verilerini oluşturmuş olduk.

#Modelimizi oluşturuyoruz.
#Sequential modeli sıralı katmanlar halinde bir yapı kurmamızı sağlıyor.

model = Sequential()

#Giriş katmanı (bu giriş katmanı belgemizin uzunluğu kadardır), bir gizli katman, bir çıkış katmanı ve iki bırakma katmanı bulunur.
#Aktivasyon fonksiyonu olarak relu hız açısından avantajlıdır. Sigmoid ve hiperbolik tanjant fonksiyonlarına göre işlem gücü daha azdır.
#128 Node Sayısıdır. Girdiler tüm düğümlere gönderilir.
model.add(Dense(128, input_shape = (len(X_train[0]),), activation='relu'))
#Dropout ile seyreltme işlemi yapıyoruz.
#Yani, zayıf bilgilerin unutulması, bırakılmasıdır. Böylece öğrenim artmaktadır.
model.add(Dropout(0.5))
#64 node ile Hidden Layer belirliyoruz ve aktivasyon olarak yine relu veriyoruz.
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
#Output aktivasyon fonksiyonu olarak softmax belirliyoruz.
model.add(Dense(len(Y_train[0]), activation='softmax'))

#decay kısmındaki 1e-6 = 0.000001 anlamına gelmektedir.
#Optimizasyon fonksiyonumuzu belirliyoruz. 
sgdOptimizer = SGD(learning_rate = 0.001, decay=1e-6, momentum=0.9, nesterov=True)
#loss fonksiyonumuzu belirledik.
#metrics algoritmanın doğru ya da yanlış yaptığını anlamasını sağlayacak yöntemi belirledik.
model.compile(loss = 'categorical_crossentropy', optimizer=sgdOptimizer, metrics=['accuracy'])

X_train = np.array(X_train)
Y_train = np.array(Y_train)

ePochs = 1000

#epochs, sistemin kaç defa eğitileceğidir.
#batch_size, tek seferde ne kadar verimizin ağdan geçeceğini belirliyoruz.
#verbose, işlem sırasında ekrana ayrıntılı verilerin yazılıp yazılmamasını belirliyoruz.
temp = model.fit(X_train, Y_train, epochs=ePochs, batch_size=8, verbose=0)#Modelimiz ile öğretme işlemi gerçekleştirilmektedir.
model.save('breathbot_model.h5', temp)
print('BreathBot Öğrenme İşlemini Tamamladı.')