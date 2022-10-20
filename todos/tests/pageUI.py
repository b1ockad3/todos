from selenium.webdriver.common.by import By

#This file contains the CSS Locators of http://127.0.0.1:8000/

category_dropdown = (By.CLASS_NAME, "dropdown")
category_input = (By.CSS_SELECTOR, ".ui.input>input")
category_submit_button = (By.CSS_SELECTOR, ".ui.form>button")
last_item_in_dropdown_locator = (By.CSS_SELECTOR,".dropdown .menu.transition>:last-child")
selected_category_header = (By.CSS_SELECTOR,"div>div>div.ui.divided.padded.grid>div>h2")
category_delete_button = (By.CSS_SELECTOR,'div>div>div.ui.divided.padded.grid>div>button')

task_table = (By.CSS_SELECTOR, ".ui.violet.table")
task_add_button = (By.CSS_SELECTOR, "div>div>table>tbody>tr>td:nth-child(1)>button")
task_title_input = (By.CSS_SELECTOR, "div>div>table>tbody>tr>td:nth-child(2)>form>div:nth-child(1)>div>input[type=text]")
task_description_input = (By.CSS_SELECTOR, "div>div>table>tbody>tr>td:nth-child(2)>form>div:nth-child(2)>div>input[type=text]")
task_date_input = (By.CSS_SELECTOR, "div>div>table>tbody>tr>td:nth-child(2)>form>div.DayPickerInput>input")

task_table_title = (By.CSS_SELECTOR,"div>div>table>tbody>tr:nth-child(1)>td:nth-child(1)>b")
task_table_description = (By.CSS_SELECTOR,"div>div>table>tbody>tr:nth-child(1)>td:nth-child(2)")
task_table_date = (By.CSS_SELECTOR,"div>div>table>tbody>tr:nth-child(1)>td:nth-child(3)")
task_done_button = (By.CSS_SELECTOR, "div>div>table>tbody>tr:nth-child(1)>td:nth-child(4)>button:nth-child(1)")
task_edit_button = (By.CSS_SELECTOR, "div>div>table>tbody>tr:nth-child(1)>td:nth-child(4)>button:nth-child(2)")