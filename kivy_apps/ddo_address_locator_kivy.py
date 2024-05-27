from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

KV = '''
<Content>
    name_result: name_result
    address_result: address_result
    location_result: location_result
    GridLayout:
        cols: 1
        MDLabel:
            id: name_result
            text: ""
        MDLabel:
            id: address_result
            text: ""
        MDLabel:
            id: location_result
            text: ""

BoxLayout:
    orientation: "vertical"

    MDToolbar:
        title: "DDO Address Locator"
        md_bg_color: 0, 0.5019607843137255, 0, 1
        elevation: 10

    MDTextField:
        id: search_input
        hint_text: "Enter name"
        helper_text: "You can search by name"
        helper_text_mode: "on_focus"

    MDRaisedButton:
        text: "Search"
        on_press: app.search_address()
'''

class AddressLocatorApp(App):
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def search_address(self):
        search_query = self.root.ids.search_input.text

        if not search_query:
            self.show_error_dialog("Please enter a name to search.")
            return

        # Use Selenium to search for the address on Google Maps
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        driver = webdriver.Edge(options=options)

        # Load the CSV file
        with open('ddo_house_locator.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                # Check if the search query matches the name in the CSV row
                if search_query.lower() in row[13].lower():
                    driver.get('https://www.google.com/maps')
                    time.sleep(5)
                    search_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
                    search_box.send_keys(row[8])
                    driver.find_element(By.ID, 'searchbox-searchbutton').click()
                    split_barangayandcity = row[3].split(",")
                    name_text = "{} {} {}".format(row[13], row[14], row[15])
                    address_text = "Address found:\nPurok {}\nBarangay {}\nCity of {}\n Province of {}".format(
                        row[4], split_barangayandcity[0], split_barangayandcity[1], "Davao De Oro")
                    location_text = "Latitude: {}\nLongitude: {}".format(row[9], row[10])

                    self.show_result_dialog(name_text, address_text, location_text)
                    return

            # If no match is found, display an error message
            self.show_error_dialog("No address found for the given name.")

    def show_result_dialog(self, name_text, address_text, location_text):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address Found",
                type="custom",
                content_cls=Content(name_text=name_text, address_text=address_text, location_text=location_text),
                buttons=[MDRaisedButton(text="Close", on_release=self.close_dialog)]
            )
        self.dialog.open()

    def show_error_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDRaisedButton(text="Close", on_release=self.close_dialog)]
            )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None


class Content(BoxLayout):
    name_result = ObjectProperty()
    address_result = ObjectProperty()
    location_result = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_result.text = kwargs.get("name_text", "")
        self.address_result.text = kwargs.get("address_text", "")
        self.location_result.text = kwargs.get("location_text", "")


if __name__ == '__main__':
    AddressLocatorApp().run()
