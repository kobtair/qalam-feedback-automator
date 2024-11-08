from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import tkinter as tk
from tkinter import simpledialog

def highlight(driver, elt, style="background: yellow; border: 3px solid red;"):
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", elt, style)

def main(username, password):
    links = []
    driver = webdriver.Firefox()
    driver.get("https://qalam.nust.edu.pk/")
    form = driver.find_element(By.TAG_NAME, "form")
    form.find_element(By.NAME, "login").send_keys(username)
    form.find_element(By.NAME, "password").send_keys(password)
    form.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, "uk-row-first"))
    )

    forms = driver.find_elements(By.CLASS_NAME, "classCards")
    for form in forms:
        formLink = form.find_element(By.TAG_NAME, "a")
        spans = form.find_elements(By.TAG_NAME, "span")
        if "Not Submitted" in spans[len(spans)-2].get_attribute("innerHTML"):
            link = formLink.get_attribute("href")
            links.append(link)
            highlight(driver, form)

    for link in links:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)

        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CLASS_NAME, "md-card-content"))
        )

        sliders = driver.find_elements(By.CLASS_NAME, "slider")
        for slider in sliders:
            highlight(driver, slider)
            slider.send_keys(Keys.RIGHT)
            time.sleep(0.6)

        comment = driver.find_element(By.TAG_NAME, "textarea")
        comment.send_keys("The Instructor was very nice")
        submit = driver.find_element(By.CLASS_NAME, "md-btn-primary")
        highlight(driver, submit)
        submit.click()
        time.sleep(0.6)

    time.sleep(0.6)
    driver.quit()

def get_credentials():
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Input", "Enter your username:")
    password = simpledialog.askstring("Input", "Enter your password:", show='*')
    return username, password

if __name__ == "__main__":
    username, password = get_credentials()
    main(username, password)
