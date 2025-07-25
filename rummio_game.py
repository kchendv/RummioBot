from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait

class RummioGame():
    def __init__(self):
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Optional: Start with a maximized window
        options.add_argument("--log-level=3")  # Supress deprecated endpoints
        # Create WebDriver (Make sure chromedriver is in your PATH or specify the full path)
        self.driver = webdriver.Chrome(service=Service(), options=options)

        file_path = os.path.abspath("rumm.io.html")
        file_url = f"file://{file_path}"
        # Load the page
        self.driver.get(file_url)


        # The browser stays open

    def get_state(self):
        # Get all cell-top divs inside the main 5x5 grid (not tutorial or win-grid)
        grid_cells = self.driver.find_elements(By.XPATH, '//div[@class="grid"]//div[@class="row"]//div//div')
        # Extract the class name (e.g., c0, c1...) and parse the numeric value
        values = []
        for cell in grid_cells:
            class_attr = cell.get_attribute("class")
            match = class_attr.split(" ")
            values.append(int(match[-1][1:]))

        input_cell = self.driver.find_elements(By.XPATH, '//div[@id="next"]//div')
        class_attr = input_cell[0].get_attribute("class")
        match = class_attr.split(" ")
        values.append(int(match[-1][1:]))
        one_hot_values = np.eye(12, dtype=np.int32)[[(v if v < 12 else 0) for v in values]].flatten()
        return one_hot_values, not(0 in values)
    
    def do_click(self, index):
        grid_cells = self.driver.find_elements(By.XPATH, '//div[@class="grid"]//div[@class="row"]//div//div')
        grid_cells[index].click()

    def reset(self):
        reset_button = self.driver.find_element(By.XPATH, '//div[text()="restart"]')
        reset_button.click()

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure driver is destroyed
        self.driver.quit()