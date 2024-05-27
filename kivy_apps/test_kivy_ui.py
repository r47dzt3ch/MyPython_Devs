from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import csv

class CSVFilterApp(App):

    def build(self):
        self.data = []
        self.filtered_data = []

        # Load the CSV data into memory
        with open('C:/Users/jeral/Documents/MyPython_Devs/kivy_apps/ddo_house_locator.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.data = list(reader)
            self.filtered_data = self.data[:]  # Copy all data initially

        layout = BoxLayout(orientation='vertical')

        self.filter_input = TextInput(hint_text="Enter filter criteria")
        self.filter_input.bind(text=self.on_filter_input)

        self.result_label = Label(text="Filtered data will be shown here")

        layout.add_widget(self.filter_input)
        layout.add_widget(self.result_label)

        return layout

    def on_filter_input(self, instance, value):
        filter_text = value.lower()
        self.filtered_data = [row for row in self.data if any(filter_text in cell.lower() for cell in row)]

        # Display the filtered data as a string
        result = '\n'.join([', '.join(row) for row in self.filtered_data])
        self.result_label.text = result

if __name__ == '__main__':
    CSVFilterApp().run()
