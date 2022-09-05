import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
import sys
import os
import mysql.connector

#Lägg till heartrandom
# ------------------------------------------------------------------------

def restart():
    print("argv: ", sys.argv)
    print("sys.executable: ", sys.executable)
    print("Restart now!")
    os.execv(sys.executable, ['python'] + sys.argv)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Ask me at malte.meuller@gmail.com",
        database="valkompasser",
    )
    my_cursor = db.cursor()


    def funk(f):
        driver = webdriver.Chrome()
        driver.get('https://valkompass.tt.se/v1/index.html?customerId=Foretagarna')
        time.sleep(1)
        driver.maximize_window()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[1]/main/div/div/section/div/button').click()
        time.sleep(1)

        heart = [a for a in range(2, 32)]  # random number
        randheart = random.choices(heart, k=3)
        print('Random hearts:', randheart)
        time.sleep(2)

        # ----------------------------------------------
        def fraga(i):
            if (i in randheart):
                time.sleep(1)
                xpa = '//*[@id="root"]/div/div[1]/div/div/div['+str(i)+']/div/section/div/main/div/section/div/div'
                driver.find_element(By.XPATH, xpa).click()
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/button').click()

            time.sleep(1)
            alt = [a for a in range(1, 5)]
            randalt = random.choice(alt)
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div['+str(i)+']/div/section/div/div/section[1]/div/div/div[2]/div['+str(randalt)+']').click()

        # -----------------------------------------------
        antfraga = [a for a in range(2, 32)]
        for i in antfraga:
            fraga(i)
        # -----------------------------------------------
        time.sleep(3)

        name_list = []
        value_list = []

        for x in range(1, 9):
            value = driver.find_element(By.XPATH, '//*[@id="root"]/div/section[1]/section/section[2]/div/section/div[1]/div['+str(x)+']/span').text
            value = value.split("%", 1)
            value = int(value[0])
            value_list.append(value)
        print(value_list)

        name = driver.find_element(By.XPATH, '//*[@id="root"]/div/section[1]/section/section[2]/div/section').text
        name = name.split()
        print(name)

        for x in range(8,16):
            name2 = name[x]
            print(name2)
            name_list.append(name2)
        print(name_list)

        my_dict = dict(zip(name_list, value_list))
        print(my_dict)

        V = my_dict["V"]
        S = my_dict["S"]
        MP = my_dict["MP"]
        C = my_dict["C"]
        L = my_dict["L"]
        M = my_dict["M"]
        KD = my_dict["KD"]
        SD = my_dict["SD"]

        insert = "INSERT INTO företagarna (V, S, MP, C, L, M, KD, SD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (V, S, MP, C, L, M, KD, SD)
        my_cursor.execute(insert, values)
        db.commit()

        driver.close()
    #------------------------------------

    iterations = [f for f in range(1, 10000)]
    for f in iterations:
        funk(f)
     #----------------------------------
except:
    restart()