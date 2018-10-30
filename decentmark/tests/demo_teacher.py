from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os 

driver = webdriver.Firefox()
driver.get("http://localhost:8000")
driver.find_element_by_id("id_username").send_keys("himanshu")
driver.find_element_by_id ("id_password").send_keys("himanshu")
driver.find_element_by_xpath("//input[2]").click()

driver.find_element_by_link_text("Create new unit").click()
unit_name = "unit 123"
start_date = "2018-10-09"
end_date = "2018-10-10"
description = "description"
driver.find_element_by_id("id_name").send_keys(unit_name)
driver.find_element_by_id("id_start").send_keys(start_date)
driver.find_element_by_id("id_end").send_keys(end_date)
driver.find_element_by_id("id_description").send_keys(description)
driver.find_element_by_xpath("//button").click()


driver.find_element_by_link_text(unit_name).click()
driver.find_element_by_link_text("View Assignments").click()
driver.find_element_by_link_text("Create new assignment").click()
ass_name = "assignment 123"
start_date = "2018-10-09"
end_date = "2018-10-10"
description = "description"
attempts = "3"
total = "10"
test = "testing"
solution = "solution"
template = "template here"
driver.find_element_by_id("id_name").send_keys(ass_name)
driver.find_element_by_id("id_start").send_keys(start_date)
driver.find_element_by_id("id_end").send_keys(end_date)
driver.find_element_by_id("id_description").send_keys(description)
# driver.find_element_by_id("id_attempts").clear()
driver.find_element_by_id("id_total").clear()
# driver.find_element_by_id("id_attempts").send_keys(attempts)
driver.find_element_by_id("id_total").send_keys(total)
driver.find_element_by_id("id_test").send_keys(test)
driver.find_element_by_id("id_solution").send_keys(solution)
driver.find_element_by_id("id_template").send_keys(template)
driver.find_element_by_xpath("//button").click()
driver.find_element_by_link_text("Return to Assignment List").click()
driver.find_element_by_link_text("Unit Home").click()
driver.find_element_by_link_text("Invite a User").click()
driver.find_element_by_id("id_users").send_keys(os.getcwd()+"/marker")
driver.find_element_by_id("id_mark").click()
driver.find_element_by_xpath("//button").click()


