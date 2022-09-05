from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
import sys
import os
import mysql.connector


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
        driver.get('https://www.aftonbladet.se/valkompassen')
        driver.maximize_window()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section/div/div[2]/button[2]').click()

        # ----------------------------------------------
        def fraga(i):
            time.sleep(1.2)
            alt = [a for a in range(1, 5)]
            randalt = random.choice(alt)
            driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/form/div[' + str(
                i) + ']/section/fieldset/div/div[1]/label[' + str(randalt) + ']').click()

        # -----------------------------------------------
        antfraga = [a for a in range(1, 31)]
        for i in antfraga:
            fraga(i)
        # -----------------------------------------------
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/form/section/div/button').click()
        time.sleep(2)

        name_list = []
        value_list = []
        for x in range(1, 9):
            value = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div/main/section/div[2]/div/div[2]/div[' + str(x) + ']/p').text
            value = value.split("%", 1)
            value = int(value[0])
            value_list.append(value)
            name = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/div/main/section/div[2]/div/div[2]/div[' + str(x) + ']/h3').text
            name_list.append(name)

        my_dict = dict(zip(name_list, value_list))
        print(my_dict)

        V = my_dict["VÄNSTERPARTIET"]
        S = my_dict["SOCIALDEMOKRATERNA"]
        MP = my_dict["MILJÖPARTIET"]
        C = my_dict["CENTERPARTIET"]
        L = my_dict["LIBERALERNA"]
        M = my_dict["MODERATERNA"]
        KD = my_dict["KRISTDEMOKRATERNA"]
        SD = my_dict["SVERIGEDEMOKRATERNA"]

        insert = "INSERT INTO aftonbladet (V, S, MP, C, L, M, KD, SD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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