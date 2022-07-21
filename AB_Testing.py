
#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################
# Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximum bidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testiyapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.

#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna Average Biddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç


# Değişkenler

# Impression: Reklam görüntüleme sayısı
# Click :     Görüntülenen reklama tıklama sayısı
# Purchase:   Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning :   Satın alınan ürünler sonrası elde edilen kazanç


#####################################################
# Proje Görevleri
#####################################################

#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################


# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from IPython.core.pylabtools import figsize
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.graphics.gofplots import qqplot
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


Control_Group = pd.read_excel("/Users/fadimeacikgoz/PycharmProjects/pythonProject/Measurement Problems/measurement_problems/datasets/ab_testing.xlsx", sheet_name="Control Group")
Test_Group = pd.read_excel("/Users/fadimeacikgoz/PycharmProjects/pythonProject/Measurement Problems/measurement_problems/datasets/ab_testing.xlsx", sheet_name="Test Group")
Control_Group.head()
Test_Group.head()


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(Test_Group)
check_df(Control_Group )

Control_Group.describe([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T
Test_Group.describe([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T



pd.plotting.scatter_matrix(Control_Group)
plt.show()
pd.plotting.scatter_matrix(Test_Group)
plt.show()




# 1.yol
#Control_Group.columns= [col + "_C" for col in Control_Group.columns]
#Test_Group.columns=[col + "_T" for col in Test_Group.columns]
#Control_Group.head()
#Test_Group.head()
# concat islemi yapalım
#df = pd.concat([Control_Group, Test_Group], axis=1, join='inner')
#df.head()
#df.columns.value_counts()
#############################



#2. yol
Control_Group["group"] = "control"
Test_Group["group"] = "test"
df = pd.concat([Control_Group,Test_Group], axis=0, ignore_index=True)
df.head()
for col in df.columns:
    sns.boxplot(x="group", y=col, hue="group", data=df)
    plt.show(block= True)


# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#Adım 1 : Hipotezi tanımlayınız.

# 1. Hipotezleri kur
# H0: M1 = M2
# Kontrol ve Test Grubu Purchase(Kazanç)  Ort. Arasında İst. Ol. Anl. Fark Yoktur
# H1: M1 != M2
# .... vardır.



#Ortalamalara baktım
Control_Group["Purchase"].mean()
Test_Group["Purchase"].mean()

# Görev 3:  Hipotez Testinin Gerçekleştirilmesi

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.


######### Normallik Varsayımı (H0: Normal dağılım varsayımı sağlanmaktadır.)
#test_stat, pvalue = shapiro(df["Purchase_C"])
#print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#test_stat, pvalue = shapiro(df["Purchase_T"])
#print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.5891
# HO reddedilemez. Control grubunun değerleri normal dağılım varsayımını sağlamaktadır.
#2.yol
shapiro(df.loc[df.index[0:40],"Purchase"])

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# Burada p_value > 0 tür , yani H0 Reddedilmez.

####### Varyans Homojenligi Varsayımı
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


### Görev 4:  Sonuçların Analizi
## Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

############################
# Varsayımlar sağlandıgı icin  bağımsız iki örneklem t testi (parametrik test)
############################

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"], equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
Control_Group["Purchase"].mean()
Test_Group["Purchase"].mean()
#   TT testi sonrası baktıgımızda p-value degeri 0.3493 cıktı, yani p-value > 0ldugu için h0 red edilmez
#   Kontrol ve Test Grubu Purchase(Kazanç)  Ort. Arasında İst. Ol. Anl. Fark Yoktur diyebiliriz.
#   Örneklem sayısını artırak tekrar birkez gözlemlenmesi gerekir.