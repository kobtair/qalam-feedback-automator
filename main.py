from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

username= "YOUR_USERNAME_HERE"
password = "YOUR_PASSWORD_HERE"

def highlight(driver, elt, style="background: yellow; border: 3px solid red;"):
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", elt, style)


def main():
    links = []
    driver = webdriver.Edge()
    driver.get("https://qalam.nust.edu.pk/")
    form = driver.find_element(By.TAG_NAME, "form")
    form.find_element(By.NAME,"login").send_keys(username)
    form.find_element(By.NAME,"password").send_keys(password)
    form.find_element(By.TAG_NAME,"button").click()
    WebDriverWait(driver, 120 ).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "uk-row-first")
                )
            )
    forms = driver.find_elements(By.CLASS_NAME, "classCards")
    for form in forms:
        formLink = form .find_element(By.TAG_NAME, "a")
        spans = form.find_elements(By.TAG_NAME, "span")
        if "Not Submitted" in spans[len(spans)-2].get_attribute("innerHTML"):
            link = formLink.get_attribute("href")
            links.append(link)
            highlight(driver, form)
    for link in links:
        driver.get(link)
        WebDriverWait(driver, 120 ).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "md-card-content")
                )
            )
        sliders = driver.find_elements(By.CLASS_NAME, "slider")
        for slider in sliders:
            highlight(driver, slider)
            slider.send_keys(Keys.RIGHT)
        comment = driver.find_element(By.TAG_NAME, "textarea")
        comment.send_keys("The Instructor was very nice")
        submit = driver.find_element(By.CLASS_NAME, "md-btn-primary")
        highlight(driver, submit)
        submit.click()
        time.sleep(5)

    time.sleep(5)
    driver.quit()


main()