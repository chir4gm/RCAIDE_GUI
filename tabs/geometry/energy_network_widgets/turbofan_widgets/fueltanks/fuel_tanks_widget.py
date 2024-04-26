import os
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from utilities import Units
from widgets.data_entry_widget import DataEntryWidget
from utilities import show_popup, Units
from tabs.geometry.frames.geometry_frame import GeometryFrame
from widgets.unit_picker_widget import UnitPickerWidget

class FuelTankWidget(QWidget, GeometryFrame):
    def __init__(self, index, on_delete, data_values=None):
        super(FuelTankWidget, self).__init__()

        self.data_values = {}
        self.index = index
        self.on_delete = on_delete

        main_section_layout = QVBoxLayout()

        data_units_labels = [
            ("Fuel Tank Origin", Units.Length),
            ("Fuel", Units.Unitless),
            ("Mass", Units.Mass),
            ("Fuel Origin", Units.Length),
            ("Center of Gravity", Units.Length),
            ("Internal Volume", Units.Volume),
        ]

        self.name_layout = QHBoxLayout()
        self.section_name_edit = QLineEdit(self)
        self.name_layout.addWidget(QLabel("Fuel Tank Name: "))
        self.name_layout.addWidget(self.section_name_edit)
        main_section_layout.addLayout(self.name_layout)

        self.data_entry_widget = DataEntryWidget(data_units_labels)
        main_section_layout.addWidget(self.data_entry_widget)

        delete_button = QPushButton("Delete Fuel Tank Segment", self)
        delete_button.clicked.connect(self.delete_button_pressed)

        main_section_layout.addWidget(delete_button)

        self.setLayout(main_section_layout)

        if data_values:
            self.load_data_values(data_values)

    def load_data_values(self, section_data):
        self.data_entry_widget.load_data(section_data)
        self.section_name_edit.setText(section_data["segment name"])

    def delete_button_pressed(self):
        print("Delete button pressed")

        if self.on_delete is None:
            print("on_delete is None")
            return

        self.on_delete(self.index)

    def get_data_values(self):
        title = self.section_name_edit.text()
        data_values = self.data_entry_widget.get_values()
        data_values["segment name"] = title

        return data_values
