from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from todos.tests import pageUI

class TodoPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def test_ui(self):
        """
        Ensure we use the ui as intended
        """
        
        #Check that category elements are visible then create a new category
        self.driver.get("http://127.0.0.1:8000/")
        self.assertTrue(self.driver.find_element(*pageUI.category_dropdown).is_displayed, "dropdown is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.category_input).is_displayed, "Category input field is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.category_submit_button).is_displayed, "Category submit button is missing from UI")
        self.driver.find_element(*pageUI.category_input).send_keys("MyNewCategory")
        self.driver.find_element(*pageUI.category_submit_button).click()
        sleep(1) # wait for endpoint to finish
        self.driver.find_element(*pageUI.category_dropdown).click()
        last_item_in_dropdown = self.driver.find_element(*pageUI.last_item_in_dropdown_locator).text
        self.assertEqual("MyNewCategory", last_item_in_dropdown, f"Got {last_item_in_dropdown} as last item in dropdown instead of 'MyNewCategory'" ) 
        self.driver.find_element(*pageUI.last_item_in_dropdown_locator).click()
        sleep(1) # wait for endpoint to finish
        
        #Check that heading contains the selected Category and task table is visible
        self.assertEqual("MyNewCategory", self.driver.find_element(*pageUI.selected_category_header).text )
        self.assertTrue(self.driver.find_element(*pageUI.category_delete_button).is_displayed,"Trash icon is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.task_table).is_displayed, "Task table is missing from UI" )
        
        #Check that add task elements are displayed then add a new task. Check new task's elements are displayed properly
        self.assertTrue(self.driver.find_element(*pageUI.task_add_button).is_displayed, "add task button is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.task_title_input).is_displayed, "title input is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.task_description_input).is_displayed, "description input is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.task_date_input).is_displayed, "date input is missing from UI")
        self.driver.find_element(*pageUI.task_title_input).send_keys("MyNewTitle")
        self.driver.find_element(*pageUI.task_description_input).send_keys("MyNewDesc")
        
        # clear() function doesn't work with values attribute so i have to clear the field manually
        self.driver.find_element(*pageUI.task_date_input).click()
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(self.driver.find_element(*pageUI.task_date_input),1,1)
        for _ in str(self.driver.find_element(*pageUI.task_date_input).get_attribute("value")):
            actions.send_keys(Keys.LEFT)
        actions.key_down(Keys.SHIFT)
        for _ in str(self.driver.find_element(*pageUI.task_date_input).get_attribute("value")):
            actions.send_keys(Keys.RIGHT)
        actions.key_up(Keys.SHIFT)
        actions.perform()
        self.driver.find_element(*pageUI.task_date_input).send_keys("2022-11-01")
        self.driver.find_element(*pageUI.task_add_button).click()
        sleep(1) # wait for endpoint to finish
        self.assertEqual("MyNewTitle", self.driver.find_element(*pageUI.task_table_title).text,"newly added title mismatch")
        self.assertEqual("MyNewDesc", self.driver.find_element(*pageUI.task_table_description).text,"newly added description mismatch")
        self.assertEqual("2022-11-01", self.driver.find_element(*pageUI.task_table_date).text,"newly added date mismatch")
        self.assertTrue(self.driver.find_element(*pageUI.task_done_button).is_displayed, "task done button is missing from UI")
        self.assertTrue(self.driver.find_element(*pageUI.task_edit_button).is_displayed, "task edit button is missing from UI")

        #Delete the category then check that category is no longer in the dropdown list
        self.driver.find_element(*pageUI.category_delete_button).click()
        sleep(1) # wait for endpoint to finish
        last_item_in_dropdown = self.driver.find_element(*pageUI.last_item_in_dropdown_locator).text
        self.assertNotEqual("MyNewCategory", last_item_in_dropdown, f"'MyNewCategory' was not removed from the category dropdown list" )

    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()