from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

def scrap_web(wait_time=10):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.worldometers.info/gdp/gdp-by-country/')

    table = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, '//table[@id="example2"]'))
    )
    headers = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    df = pd.DataFrame(columns=[header.text.strip().replace('\n', ' ') for header in headers[1:6]])
    body = table.find_element(By.TAG_NAME, 'tbody')

    for trow in body.find_elements(By.TAG_NAME, 'tr')[:5]:
        row = []
        for td in trow.find_elements(By.TAG_NAME, 'td')[1:6]:
            row.append(td.text)
        df.loc[len(df)] = row
    driver.quit()
    return df

def enter_to_notebook(df, filename='output.txt'):
    df_str = df_convert_to_str(df)
    print(df_str)
    notepad = Application(backend='uia').start('notepad.exe')
    notepad = Application(backend='uia').connect(title='Untitled - Notepad', timeout=5)
    window = notepad.UntitledNotepad

    window.type_keys(df_str, with_spaces=True, with_newlines=True, pause=0.1)
    send_keys('^+S', pause=0.5)
    send_keys(filename, pause=0.2)
    send_keys('{ENTER}')
    send_keys('^W')


def df_convert_to_str(df, separator='||'):
    separator = " " + separator + " "
    df_str = separator.join(df.columns) + '\n'
    for index, row in df.iterrows():
        df_str += separator.join(str(x).replace('%','') for x in row) + '\n'
    return df_str


enter_to_notebook(scrap_web())
