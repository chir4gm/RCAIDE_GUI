import json
from typing import Type

import RCAIDE
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QStackedLayout, QTreeWidget, QTreeWidgetItem

from tabs.geometry.frames import *


class GeometryWidget(QWidget):
    def __init__(self):
        """Create a widget for entering vehicle geometry."""
        super(GeometryWidget, self).__init__()

        # Define actions based on the selected index
        self.frames: list[Type[GeometryFrame]] = [VehicleFrame, FuselageFrame, WingsFrame, NacelleFrame,
                                                  LandingGearFrame, EnergyNetworkFrame]
        self.tabs = ["Fuselages", "Wings", "Nacelles",
                     "Landing Gear", "Energy Networks"]
        
        options = ["Vehicle Attributes", "Add Fuselage", "Add Wings", "Add Nacelles", "Add Landing Gear",
                   "Add Energy Network"]
        
        self.data = []
        self.vehicle = RCAIDE.Vehicle()

        for _ in range(len(self.tabs)):
            self.data.append([])

        base_layout = QHBoxLayout()
        self.main_layout = QStackedLayout()
        self.tree_frame_layout = QVBoxLayout()

        for index, frame in enumerate(self.frames):
            frame_widget = frame()
            frame_widget.set_save_function(self.save_data)
            frame_widget.set_tab_index(index)
            self.main_layout.addWidget(frame_widget)  # type: ignore
        
        self.dropdown = QComboBox()
        self.dropdown.addItems(options)
        self.dropdown.currentIndexChanged.connect(self.on_dropdown_change)
        self.tree_frame_layout.addWidget(self.dropdown)

        # Create a QComboBox and add options
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Vehicle Components"])
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        
        vehicle_item = QTreeWidgetItem(["Vehicle"])
        self.tree.addTopLevelItem(vehicle_item)
        self.tree_frame_layout.addWidget(self.tree)

        # main_layout.addWidget(Color("navy"), 7)
        base_layout.addLayout(self.tree_frame_layout, 1)
        base_layout.addLayout(self.main_layout, 4)

        self.main_layout.setSpacing(3)
        base_layout.setSpacing(3)

        # Initially display the DefaultFrame
        self.main_layout.setCurrentIndex(0)
        self.setLayout(base_layout)

    def on_dropdown_change(self, index):
        """Change the index of the main layout based on the selected index of the dropdown.

        Args:
            index: The index of the selected item in the dropdown.
        """
        layout = self.layout()
        if layout:
            self.main_layout.setCurrentIndex(index)

    def on_tree_item_clicked(self, item, _col):
        """Change the index of the main layout based on the selected item in the tree.

        Args:
            item: The selected item in the tree.
            _col: The column index of the selected item. (Not used)

        """        
        # get item depth
        depth = 0
        while item.parent():
            item = item.parent()
            depth += 1


        if depth == 0:
            self.main_layout.setCurrentIndex(0)
            return
        if depth == 1:
            top_item = item.parent()
            tab_index = self.tree.indexFromItem(top_item).row()
            assert top_item is not None
            
            index = top_item.indexOfChild(item)
            frame = self.main_layout.widget(tab_index + 1)
            assert isinstance(frame, GeometryFrame)
            
            frame.load_data(self.data[tab_index][index], index)
            self.main_layout.setCurrentIndex(tab_index + 1)
        

    def save_data(self, tab_index, vehicle_component=None, index=0, data=None, new=False):
        """Save the entered data in a frame to the list.

        Args:
            tab_index: The index of the tab.
            index: The index of the vehicle element in the list. (Within its type, eg fuselage #0, #1, etc.)
            vehicle_component: The vehicle component to be appended to the vehicle.
            data: The data to be saved.
            new: A flag to indicate if the data is of a new element.
        """
        print("Saving data:", data)
        if data is None:
            return

        if new:
            self.data[tab_index].append(data)
            child = QTreeWidgetItem([data["name"]])
            item = self.tree.topLevelItem(tab_index)
            assert item is not None
            item.addChild(child)
            index = item.indexOfChild(child)
        else:
            self.data[tab_index][index] = data
            top_item = self.tree.topLevelItem(tab_index)
            assert top_item is not None

            child = top_item.child(index)
            assert child is not None
            child.setText(0, data["name"])

        with open("data/geometry.json", "w") as f:
            f.write(json.dumps(self.data, indent=4))

        if vehicle_component:
            # Check if it is an energy network being added
            if tab_index == 4:
                self.vehicle.append_energy_network(vehicle_component)
            else:
                self.vehicle.append_component(vehicle_component)

        return index
    
    def get_vehicle(self):
        return self.vehicle
    
    def get_data(self):
        return self.data


def get_widget() -> QWidget:
    """Return the geometry widget.

    Returns:
        The geometry widget.
    """
    return GeometryWidget()
