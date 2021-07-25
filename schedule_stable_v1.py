#libraries
import datetime as dt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import modules.distribution as dist

#functions
def check_condition():
    r_ = 2
    # if condition_1 == True:
        # r_ += 1
    if condition_2 == True:
        r_ += 1
        while courses_c.Grade.value_counts().iloc[0] > len(schedule_a.columns):
            st.markdown("""#### ***Girdiğiniz koşullara göre dağılım gerçekleştirilemiyor. Bir öğrencinin bir günde birden fazla zorunlu derse giremediği durumda gün sayısı en fazla zorunlu dersi olan sınıfın zorunlu ders sayısından küçük olmamalıdır. Lütfen tarihleri değiştirin.***""")
            exit()
    return r_

#instructions
st.markdown("""
            # Sınav Programı
            *by bozkurt toral*
              
            ### **Kullanım talimatları:**
            1. Tarihleri ve günlük süreyi belirleyin.\n
            2. Koşulları seçin.\n
            3. Sınav dosyasını yükleyin.\n
            """)

example = st.checkbox("4. Örnek Dosyayı Göster", False)
if example == True:
    st.image(Image.open("examples/example.jpg"), caption="Örnek Ders Listesi")

#inputs
st.sidebar.markdown("# Periyot Ayarları")
first_day = st.sidebar.date_input("Başlangıç tarihini giriniz.", dt.date.today())
last_day = st.sidebar.date_input("Bitiş tarihini giriniz.", dt.date.today() + dt.timedelta(days = 6))
start_time = st.sidebar.time_input("Başlangıç saatini giriniz.", dt.time(9, 00))
stop_time = st.sidebar.time_input("Bitiş saatini giriniz.", dt.time(17, 00))

st.sidebar.markdown("# Koşullar")
condition_2 = st.sidebar.checkbox("Bir öğrenci bir günde birden fazla zorunlu dersin sınavına giremez.", True)
condition_3 = st.sidebar.checkbox("Bitiş saatini aşmaya izin verme.", True)
condition_1 = st.sidebar.checkbox("Ders listesi birden çok bölümün dersini içeriyor. [HAZIRLANIYOR]", False)
condition_4 = st.sidebar.checkbox("Cumartesi günlerini dahil etme. [HAZIRLANIYOR]", False)
condition_5 = st.sidebar.checkbox("Pazar günlerini dahil etme. [HAZIRLANIYOR]", False)
                                  
st.sidebar.markdown("# Görünüm")
optiond_1 = st.sidebar.checkbox("Daraltılmış görünüm.", True)

st.markdown("### **Ders Listesi**")           
uploaded_file = st.file_uploader("", ["xlsx"], False)
try:
    file = pd.read_excel(uploaded_file).sort_values(by="Duration", ascending=False).reset_index(drop = True)
    courses_c = file[file.Mandatory == "Y"].sort_values(by="Duration", ascending=False).reset_index(drop = True)
    courses_e = file[file.Mandatory == "N"].sort_values(by="Duration", ascending=False).reset_index(drop = True) 
    process = "ongoing"
    
    #schedule_a
    period_d = []
    for d in range (0, (last_day - first_day).days+1):
        day = str(first_day + dt.timedelta(days=d)).split()[0]
        period_d.append(day)
    period_t = (dt.datetime.combine(first_day, stop_time)
                - dt.datetime.combine(first_day, start_time)).seconds/60 
    schedule_a = pd.DataFrame(columns = period_d)
    for d in schedule_a.columns:
        schedule_a.loc["Kalan Süre", d] = period_t  
    
    #schedule_b
    schedule_b = pd.DataFrame(columns = period_d)
    con_ = check_condition()
    var_ = ["Courses", "Duration"]
    for i in range (0, len(schedule_a.columns)):
        schedule_b.insert((2 * i) + 1, f"{schedule_a.columns[i]} | Duration", True) 
    if con_ > 2:
        var_.append("Grade")
        for i in range (0, len(schedule_a.columns)):
            schedule_b.insert((3*i) + 2, f"{schedule_a.columns[i]} | Grade", True)
    for i in range (0, len(schedule_a.columns)):
        schedule_b.loc["Kalan Süre", schedule_b.columns[(con_* i) + 1]] = schedule_a.iloc[0, i]        
    
    #schedule_c
    schedule_c = pd.DataFrame(columns = period_d)
    
    #distribution
    non_distributed = []
    dist.distribution(file,
                      schedule_a,
                      schedule_b,
                      courses_c,
                      var_,
                      con_,
                      condition_1,
                      condition_2,
                      condition_3,
                      non_distributed)
    dist.distribution(file,
                      schedule_a,
                      schedule_b,
                      courses_e,
                      var_,
                      con_,
                      condition_1,
                      condition_2,
                      condition_3,
                      non_distributed)
    non_distributed = pd.DataFrame(non_distributed).rename(columns = {0: "Dağıtılamayan Dersler"})

    #edit    
    for row in range (1, schedule_b.shape[0]):
        if pd.isnull(schedule_b.loc[row, :]).all(axis=0) == True:
            schedule_b.drop(index = row, inplace = True)
    for col in range (0, schedule_a.shape[1]):
        schedule_b.loc["Kalan Süre", schedule_b.columns[(con_ * col) + 1]] = schedule_a.iloc[0, col]
        if optiond_1 == True:
            if con_ == 2:
                schedule_b[schedule_b.columns[(con_ * col)]] = schedule_b[schedule_b.columns[(con_ * col)]] + ", Süre:" + schedule_b[schedule_b.columns[(con_*col) + 1]].astype(str) + " dk."
                schedule_c.loc[:, schedule_c.columns[col]] = schedule_b.loc[:, schedule_b.columns[(con_ * col)]]
            elif con_ == 3:
                schedule_b[schedule_b.columns[(con_ * col)]] = schedule_b[schedule_b.columns[(con_ * col)]] + ", Süre:" + schedule_b[schedule_b.columns[(con_*col) + 1]].astype(str) + " dk, Sınıf:" + schedule_b[schedule_b.columns[con_*col + 2]].astype(str) + "."
                schedule_c.loc[:, schedule_c.columns[col]] = schedule_b.loc[:, schedule_b.columns[(con_ * col)]]
            schedule_c.loc["Kalan Süre", schedule_c.columns[col]] = schedule_a.iloc[0, col]
        elif optiond_1 == False:
            schedule_c = schedule_b
    
    #results    
    process = "completed"
    if process == "completed":
        st.markdown("""### **Sınav Programı:**""")
        st.markdown("""*Girdiğniz tarih aralığı ve süreye göre dersler aşağıdaki gibi dağıtılmıştır.*""")
        #st.table(schedule_c)
        # download_button = st.button("Tabloyu İndirmek İçin Tıklayınız [YAKINDA]")
        st.markdown("""### **Dağıtılamayan Dersler:**""")
        if non_distributed.empty == True:
            st.markdown("""*Girdiğiniz tarih aralığı ve süreye göre bütün dersler dağıtılmıştır.* """)
        elif non_distributed.empty == False:
            st.markdown("""*Girdiğiniz tarih aralığı ve süreye göre aşağıdaki dersler dağıtılamamıştır*""")
            st.table(non_distributed) 
# =============================================================================
#         if download_button == True:
#             fname = str(dt.datetime.now())
#             fname = "".join(filter(str.isalnum, fname))
#             schedule_c.to_excel(f"schedule{fname}.xlsx")
# =============================================================================
except KeyError:
    st.markdown("""
                    *Yüklemiş olduğunuz dosyayı örnekteki gibi düzeleneyip tekrar deneyiniz.*
                """)
except AssertionError:
    st.markdown("""
                    *Hazırlamış olduğunuz ders listesini aşağıdaki alanı sürükleyiniz veya **Browse Files** butonuna dosyayı basarak seçiniz.*
                """)

 
            
            
            
            
            