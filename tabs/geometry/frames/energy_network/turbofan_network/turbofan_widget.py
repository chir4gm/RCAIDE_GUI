from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QTabWidget

from tabs.geometry.frames.energy_network.energy_network_widget import EnergyNetworkWidget
from tabs.geometry.frames.energy_network.turbofan_network.fuelline_widget import FuelLineWidget
from widgets.data_entry_widget import DataEntryWidget

# TODO: Implement an EnergyNetworkWidget class to standardize the structure of the widgets

class TurbofanWidget(QWidget, EnergyNetworkWidget):
    def __init__(self):
        super(TurbofanWidget, self).__init__()

        self.save_function = None
        self.data_entry_widget: DataEntryWidget | None = None

        self.fuellines_layout = QVBoxLayout()  # Define main_layout here
        self.fuellines_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_layout = QHBoxLayout()

        layout = self.create_scroll_layout()

        add_section_button = QPushButton("Add Fuel Line Section", self)
        add_section_button.setMaximumWidth(200)

        add_section_button.clicked.connect(self.add_fuelline_section)
        header_layout.addWidget(add_section_button)

        layout.addLayout(header_layout)

        name_layout = QHBoxLayout()

        layout.addLayout(name_layout)

        # Add line above buttons
        line_bar = QFrame()
        line_bar.setFrameShape(QFrame.Shape.HLine)
        line_bar.setFrameShadow(QFrame.Shadow.Sunken)
        line_bar.setStyleSheet("background-color: light grey;")

        layout.addWidget(line_bar)
        layout.addLayout(self.fuellines_layout)
        
        update_selector_button = QPushButton("Update Fuel Tank Selector")
        update_selector_button.clicked.connect(self.update_fuel_selector)
        layout.addWidget(update_selector_button)
        
        fuel_tank_selector = QTabWidget()
        fuel_tank_selector.setTabPosition(QTabWidget.TabPosition.North)
        # fuel_tank_selector.addTab(QLabel("Tab 1"), "Fuel Tank 1")
        # fuel_tank_selector.addTab(QLabel("Tab 2"), "Fuel Tank 2")

        layout.addWidget(fuel_tank_selector)

    def add_fuelline_section(self):
        self.fuellines_layout.addWidget(
            FuelLineWidget(self.fuellines_layout.count(), self.on_delete_button_pressed))
    
    def update_fuel_selector(self):
        data, lines = self.get_data_values()
        
    
    def load_data_values(self, data):
        # Clear the layout
        for i in reversed(range(self.fuellines_layout.count())):
            widget_item = self.fuellines_layout.itemAt(i)
            assert widget_item is not None
            widget = widget_item.widget()
            assert widget is not None
            
            self.fuellines_layout.removeWidget(widget)
            widget.deleteLater()
        
        for index, section in enumerate(data):
            self.fuellines_layout.addWidget(
                FuelLineWidget(index, self.on_delete_button_pressed, section))

    def get_data_values(self):
        # Collect data from fuel line widgets
        data = []
        lines = []
        for index in range(self.fuellines_layout.count()):
            item = self.fuellines_layout.itemAt(index)
            assert item is not None
            widget = item.widget()
            assert widget is not None and isinstance(widget, FuelLineWidget)
            fuelline_data, line = widget.get_data_values()
            data.append(fuelline_data)
            lines.append(line)

        return data, lines

    def on_delete_button_pressed(self, index):
        widget_item = self.fuellines_layout.itemAt(index)
        if widget_item is not None:
            widget = widget_item.widget()
            self.fuellines_layout.removeWidget(widget)
            self.fuellines_layout.update()
            print("Deleted Fuel Line at Index:", index)

            for i in range(index, self.fuellines_layout.count()):
                widget_item = self.fuellines_layout.itemAt(i)
                assert widget_item is not None
                widget = widget_item.widget()
                assert widget is not None and isinstance(widget, FuelLineWidget)
                
                widget.index = i
                print("Updated Index:", i)

    def create_scroll_layout(self):
        # Create a widget to contain the layout
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)  # Set the main layout inside the scroll content

        # Set the main layout of the widget
        self.setLayout(layout)
        return layout
