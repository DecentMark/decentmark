from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://localhost:8000")
driver.find_element_by_id("id_username").send_keys("student")
driver.find_element_by_id ("id_password").send_keys("university123")
driver.find_element_by_xpath("//input[2]").click()

unit_name = "unit 123"
driver.find_element_by_link_text(unit_name).click()
driver.find_element_by_link_text("View Assignments").click()

ass_name = "assignment 123"

driver.find_element_by_link_text(ass_name).click()
driver.find_element_by_link_text("Make a submission").click()
solution = "solution 123"
driver.find_element_by_id("id_solution").send_keys(solution)
driver.find_element_by_xpath("//button").click()

