import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
import sys
import os
import mysql.connector
#------------------------------------------------------------------------
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
    chromedriver_autoinstaller.install()

    def func(f):

        driver = webdriver.Chrome()
        driver.get('https://valkompass.svt.se/2022/riksdag/fraga/vinstutdelning-for-friskolor-ska-forbjudas')
        time.sleep(1)
        driver.maximize_window()
        time.sleep(1)


        def fraga(i):
            print('fråga:', i)
            alt = [1, 2, 4, 5]
            randalt = random.choice(alt)
            print('random choice:', randalt)

            title = driver.find_element(By.XPATH, '//h1').text
            title = title.lower()
            title = title.replace(" ", "-")
            title = title.replace("ö", "o")
            title = title.replace("ä", "a")
            title = title.replace("å", "a")
            title = title.replace("---", "-")
            title = title.replace("--", "-")
            print(title)
            time.sleep(1)

            driver.find_element(By.XPATH, '//*[@id="' + str(title) + '"]/div[1]/div/div[2]/div/div[1]/div/div/div[' + str(
                randalt) + ']/button').click()
            time.sleep(1)


        # -------------------------------------------

        antfraga = list(range(1, 31))

        for i in antfraga:
            fraga(i)

        # ---------------------------------------

        altflerval = list(range(1, 6))

        randfleralt = random.choice(altflerval)
        driver.find_element(By.XPATH,
                            '//*[@id="hur-oppet-ska-sverige-vara-for-att-ta-emot-asylsokande"]/div[1]/div/div[2]/div/div[1]/div/fieldset/div[' + str(
                                randfleralt) + ']').click()
        time.sleep(1)

        randfleralt = random.choice(altflerval)
        driver.find_element(By.XPATH,
                            '//*[@id="hur-mycket-ska-polisen-fa-anvanda-hemlig-avlyssning-och-overvakning-utan-brottsmisstanke"]/div[1]/div/div[2]/div/div[1]/div/fieldset/div[' + str(
                                randfleralt) + ']').click()
        time.sleep(1)

        randfleralt = random.choice(altflerval)
        driver.find_element(By.XPATH,
                            '//*[@id="hur-mycket-ska-hoginkomsttagare-betala-i-skatt"]/div[1]/div/div[2]/div/div[1]/div/fieldset/div[' + str(
                                randfleralt) + ']').click()
        time.sleep(1)

        randfleralt = random.choice(altflerval)
        driver.find_element(By.XPATH,
                            '//*[@id="hur-mycket-av-skogen-i-sverige-ska-skyddas"]/div[1]/div/div[2]/div/div[1]/div/fieldset/div[' + str(
                                randfleralt) + ']').click()

        time.sleep(1)
        fler = list(range(1, 10))
        randfler = random.sample(fler, k=3)
        print(randfler)
        driver.execute_script("window.scrollTo(0, 400)")
        time.sleep(1)
        for i in randfler:
            driver.find_element(By.XPATH,
                                '//*[@id="vilka-av-foljande-omraden-ska-prioriteras-av-staten"]/div[1]/div/div[2]/div/div[1]/div/fieldset/label[' + str(
                                    i) + ']/span').click()
            time.sleep(1)

        time.sleep(1)
        driver.find_element(By.XPATH,
                            '//*[@id="vilka-av-foljande-omraden-ska-prioriteras-av-staten"]/div[1]/div/div[2]/div/div[2]/a').click()

        time.sleep(1)
        fler2 = list(range(1, 35))
        randfler2 = random.sample(fler2, k=5)
        print(randfler2)
        time.sleep(1)
        for i in randfler2:
            element = driver.find_element(By.XPATH,
                                          '//*[@id="root"]/div[2]/main/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/label[' + str(
                                              i) + ']/span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            time.sleep(1)

        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/main/div/div/div/div[2]/div/div/div[2]/div/div[2]/a').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/main/div/div/div/div[2]/div/div[2]/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/main/div/div/div/div[2]/div/div[1]/div/div[2]/div').click()


        parties = []
        values = []
        part = list(range(2, 10))

        for i in part:
            text = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/main/div/div/div/div[2]/div/div[1]/div/div['+str(i)+']/div').text
            print(text)
            text = str(text)
            text = text.split()
            print(text)
            for j in text:
                if j.isalpha:
                    parties.append(j)


        for i in parties:
            if len(i)>3:
                parties.remove(i)

        print(parties)
        lista = (0,1,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-3,-2,-1)

        namn= (0,-14,-12,-10,-8,-6,-4,-2)
        varde= (1,-13,-11,-9,-7,-5,-3,-1)

        name=[]
        value=[]
        for i in namn:
            name.append(parties[i])

        for i in varde:
            value.append(parties[i])

        value_ny = []
        for i in value:
            x = i
            x = x.split("%", 1)
            x = int(x[0])
            value_ny.append(x)


        my_dict = dict(zip(name, value_ny))

        V = my_dict["V"]
        S = my_dict["S"]
        MP = my_dict["MP"]
        C = my_dict["C"]
        L = my_dict["L"]
        M = my_dict["M"]
        KD = my_dict["KD"]
        SD = my_dict["SD"]

        insert = "INSERT INTO SVT (V, S, MP, C, L, M, KD, SD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (V, S, MP, C, L, M, KD, SD)
        my_cursor.execute(insert, values)
        db.commit()

        time.sleep(2)

        driver.close()
#--------------------------------
    iterations = [f for f in range(1, 10000)]
    for f in iterations:
        func(f)

except:
    restart()