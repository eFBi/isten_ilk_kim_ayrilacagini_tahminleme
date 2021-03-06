# -*- coding: utf-8 -*-
"""
# İşten İlk Kimlerin Ayrılacağını Tahminleme

## Giriş

Veri setimizde:
* Çalışan memnuniyet oranı, (satisfaction_level) (0-1 aralığında)
* Son değerlendirme (last_evaluation) (0-1 aralığında)
* Proje sayısı (number_project)
* Ortalama aylık çalışma süresi (average_monthly_hours)
* Şirkette geçirilen yıl (time_spent_company)
* İş kazası geçirilip geçirilmediği (work_accident)*
* Son 5 yılda promosyon alıp almadığı (promotion_last_5_years)
* Departman(sales)
* Maaş (salary) - (low, medium or high)
* Çalışanın işten ayrılıp ayrılmadığı (left)

Şeklinde tanımlanmış attribute lar bulunmaktadır. Çalışanın işten ayrılıp ayrılmadığı (left) bilgisi
etiket değeri olarak alınacak ve eğitim veri seti kullanılarak, test veri seti içerisinde yer alan
çalışanların işten ayrılıp ayrılmadığı tahmin edilecektir.
Bu veri seti üzerinde Karar Ağaçları ve Yapay Sinir Ağları kullanarak farklı modeller geliştirip bu
modellere ait eğitim, validasyon ve test veri seti üzerindeki model başarımlarını karşılaştırmanız
beklenmektedir

## Veri Seri ve Kütüphaneleri Yükleme
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn

data = pd.read_csv('HR.csv')

data

data.describe()

data.info()

data.corr()['left'].sort_values()

plt.figure(figsize=(15,4),dpi=100)
plt.subplot(1,2,1)
sbn.distplot(data['satisfaction_level'])
plt.subplot(1,2,2)
sbn.distplot(data['Work_accident'])

plt.figure(figsize=(15,4),dpi=100)
plt.subplot(1,2,1)
sbn.distplot(data['time_spend_company'])
plt.subplot(1,2,2)
sbn.distplot(data['average_montly_hours'])

#plt.figure(figsize=(20,5),dpi=100)
sbn.catplot(x="salary", y="left", data=data, hue="sales", kind="bar",height=7)
plt.title('sales ve salary özelliklerinin değerlerine göre left')
plt.show()

sbn.countplot(x='left',data=data)

plt.figure(figsize=(12,5),dpi=100)
plt.title('sales özelliğine değerlerine göre left')
sbn.countplot(x='sales', data=data, hue='left')
plt.show()

plt.figure(figsize=(7,4),dpi=100)
plt.title('salary özelliğine değerlerine göre left')
sbn.countplot(x='salary', data=data, hue='left')
plt.show()

plt.figure(figsize=(18,4),dpi=100)
plt.subplot(1,4,1)
sbn.boxplot(x = data.satisfaction_level, color = 'red')
plt.subplot(1,4,2)
sbn.boxplot(x = data.time_spend_company, color = 'blue')
plt.subplot(1,4,3)
sbn.boxplot(x = data.average_montly_hours, color = 'green')
plt.subplot(1,4,4)
sbn.boxplot(x = data.number_project, color = 'yellow')
plt.show()

len(data)*0.01  # Veri setinden en fazla 150 örnek silebilirsin.

data[data['time_spend_company']>8]

# Sonuçlar tutarsız olursa outlier ları çıkarabilirsin.
#data = data[data['ejection_fraction']<70]

"""## Veriyi test ve train olarak ayarlama"""

from sklearn.model_selection import train_test_split

# Y = wX + b

# Y -> Label (Çıktı)
y = data["left"].values

# X -> Feature,Attribute (Özellik)
x = data[['satisfaction_level','time_spend_company','average_montly_hours','number_project','last_evaluation']].values

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.33,random_state=10)

print(x_train.shape,x_test.shape,y_train.shape,x_test.shape)

"""## Veriyi Normalize Etme"""

from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping

scaler = StandardScaler()

scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

"""## ANN Yöntemiyle Model Oluşturma"""

import tensorflow as tsf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.callbacks import EarlyStopping

np.random.seed(0)

model = Sequential()



""" Accuracy = %0.965
model.add(Dense(units = 7, activation = 'relu'))
model.add(Dense(units = 7, activation = 'relu'))
model.add(Dense(units = 7, activation = 'relu'))
"""

model.add(Dense(units = 1, activation = 'sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics = ['accuracy'])

"""### Modeli Eğitme"""

early_stopping = EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=25)

model.fit(x=x_train,y=y_train,epochs=500,validation_data=(x_test,y_test),verbose=1,callbacks=[early_stopping])

model_loss = pd.DataFrame(model.history.history)

figure = model_loss.plot()
figure.set_title('Eğitim ve Test, Doğrulukları ve Hataları')
plt.show()

tahminlerimiz = model.predict_classes(x_test)

model.evaluate(x_train,y_train)

"""### Modeli değerlendirme"""

from sklearn.metrics import classification_report , confusion_matrix, accuracy_score

print(classification_report(y_test,tahminlerimiz))

print(confusion_matrix(y_test,tahminlerimiz))

acc_ann = accuracy_score(y_test,tahminlerimiz)
print('Accuracy = ', acc_ann)

"""### Model ile Tahmin"""

satisfaction_level	last_evaluation	number_project	average_montly_hours	time_spend_company	Work_accident	left	promotion_last_5years
    0.40	            0.57	        2	            151	                    3	                0	            1	    0
    0.49	            0.60	        3	            214	                    2	                0	            0	    0
    0.90	            0.55	        3	            259	                    10	                1	            0	    1

yeni_ornek_ozellikleri = [[0.9,10,260,3,0.55]]

yeni_ornek_ozellikleri = scaler.transform(yeni_ornek_ozellikleri)

model.predict(yeni_ornek_ozellikleri)

"""## Karar Ağacı Yöntemi ile Model Oluşturma

###  Optimum max_leaf_nodes sayısını bulma
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
list1 = []
for leaves in range(2,10):
    classifier = DecisionTreeClassifier(max_leaf_nodes = leaves, random_state=0, criterion='entropy')
    classifier.fit(x_train, y_train)
    y_tahmin = classifier.predict(x_test)
    list1.append(accuracy_score(y_test,y_tahmin))
#print(mylist)
plt.plot(list(range(2,10)), list1)
plt.show()

"""### Eğitim setinde Karar Ağacı Sınıflandırıcısının eğitimi"""

classifier = DecisionTreeClassifier(max_leaf_nodes = 3, random_state=0, criterion='entropy')
classifier.fit(x_train, y_train)

"""### Test seti sonuçlarının tahmin edilmesi"""

y_tahmin = classifier.predict(x_test)
print(y_pred)

"""### Karışıklık matrisinin yapılması ve doğruluk puanının hesaplanması"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_tahmin)
print(cm)

acc_dt = accuracy_score(y_test,y_tahmin)
print('Accuracy = ', acc_dt)

"""## Modellerin Karşılaştırılması"""

modeller = ['ANN','Decision Tree']
accuracy_list = [acc_ann*100,acc_dt*100]
accuracy_list

plt.figure(figsize=(8,3),dpi=100)
sbn.barplot(x=accuracy_list,y=modeller,palette='Blues')
plt.xlabel("Accuracy")
plt.ylabel("Modeller")
plt.title('Modellerin Doğruluk Karşılaştırılması')
plt.show()

