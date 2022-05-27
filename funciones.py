from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Credentials
mail = "dev@frogmi.com"
password = "Dfr0g2K21"

# Subfunciones
def chrome_start():  
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome("chromedriver",options=options)

    print("[+]  Chrome driver started")
    return driver

def wait_to_load(driver, name):
    WebDriverWait(driver=driver, timeout=10).until(lambda x: x.execute_script("return document.readyState === 'complete'"))
    errors = driver.find_elements(By.CLASS_NAME, "flash-error")
    error_message = "Incorrect username or password."
    for e in errors:
        print(e.text)
    if any(error_message in e.text for e in errors):
        print("[!]  "+ name +" failed")
    else:
        print("[+]  "+ name +" successful load")

def click_from_list(list,name):
    for element in list:
        #print(element.text)
        if(element.text == name):
            element.click()
            print("[->] "+ name +" clicked")
            return
    print("[!]  "+ name +" not found")

# Funciones de accion

def login_dev(driver):
    driver.get("https://neo.frogmi.com/login")
    driver.maximize_window()

    driver.find_element(By.ID,"identification").send_keys(mail)
    driver.find_element(By.ID,"password").send_keys(password)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Sign in')]").click()

    wait_to_load(driver,"Login")
    driver.implicitly_wait(2)
    return driver

def click_on_mainHeader(driver, name):
    shortWait = WebDriverWait(driver,10)
    try:
        shortWait.until(EC.visibility_of_element_located((By.CLASS_NAME,"main-header")))
        print("[->] Header menu found")
    except:
        print("[!] Header menu not found")
        return

    buttons = driver.find_elements(By.XPATH,"//*[@class = 'main-nav pull-left']/li")

    click_from_list(buttons,name)
    wait_to_load(driver,name)

def click_on_dashboardSidebar(driver, name):
    shortWait = WebDriverWait(driver,10)
    try:
        shortWait.until(EC.visibility_of_element_located((By.CLASS_NAME,"context-nav-container")))
        print("[->] Sidebar menu found")
    except:
        print("[!]  Sidebar menu not found")
        return

    buttons = driver.find_elements(By.XPATH,"//*[@class = 'sidebar-nav']/li")
    click_from_list(buttons,name)
    wait_to_load(driver,name)

def return_to_dashboard(driver):
    shortWait = WebDriverWait(driver,10)
    try:
        shortWait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.logo.pull-left")))
        driver.find_element(By.CSS_SELECTOR,"h1.logo.pull-left").click()
        print("[->] Return to dashboard")
    except:
        print("[!]  Logo not found")
        return

def dashboard_info(driver):
    shortWait = WebDriverWait(driver,10)
    try:
        shortWait.until(EC.visibility_of_element_located((By.XPATH,"//*[@class = 'dashboard-content']")))
    except:
        print("[!] Dashboard info not found")

    dashboard = driver.find_elements(By.XPATH,"//*[@class = 'dashboard-content']/div/div")
    
    for element in dashboard:
        print("-"+ element.text +"-")

def change_date_range(driver,range):
    shortWait = WebDriverWait(driver,10)
    try:
        shortWait.until(EC.visibility_of_element_located((By.XPATH,"//*[@class = 'row title-and-filter']")))
    except:
        print("[!] Title & Filter not found")
        return

    dateRange = driver.find_element(By.CSS_SELECTOR,"div.reportrange.pull-right")
    dateRange.click()

    try:
        driver.find_element(By.XPATH,"//*[contains(text(), '"+range+"')]").click()
        print("[->] Range changed to: "+ range)
    except:
        print("[!] Could't click: "+ range)
    

if __name__ == '__main__':
    chromeWindow = chrome_start()

    login_dev(chromeWindow)
    change_date_range(chromeWindow,"Último Mes")

    #chromeWindow.close()
    print("\n---- End of test ----")