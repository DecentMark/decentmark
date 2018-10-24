from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://localhost:8000")
driver.find_element_by_id("id_username").send_keys("marker")
driver.find_element_by_id ("id_password").send_keys("university123")
driver.find_element_by_xpath("//input[2]").click()

unit_name = "unit 123"
driver.find_element_by_link_text(unit_name).click()

driver.find_element_by_link_text("View Assignments").click()

ass_name = "assignment 123"
driver.find_element_by_link_text(ass_name).click()

driver.find_element_by_link_text("View Submissions").click()
driver.find_element_by_link_text("student").click()

driver.find_element_by_link_text("Mark this submission").click()
feedback = "feedback"
mark = 6
driver.find_element_by_id("id_mark").clear()
driver.find_element_by_id("id_mark").send_keys(mark)
driver.find_element_by_id("id_feedback").send_keys(feedback)
driver.find_element_by_xpath("//button").click()


