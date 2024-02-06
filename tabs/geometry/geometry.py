from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QStackedLayout

from tabs.geometry.frames.default_frame import DefaultFrame
from tabs.geometry.frames.energy_network_frame import EnergyNetworkFrame
from tabs.geometry.frames.fuselage_frame import FuselageFrame
from tabs.geometry.frames.landing_gear_frame import LandingGearFrame
from tabs.geometry.frames.nacelle_frame import NacelleFrame
from tabs.geometry.frames.wings_frame import WingsFrame


class GeometryWidget(QWidget):

    def __init__(self):
        super(GeometryWidget, self).__init__()

        base_layout = QHBoxLayout()
        main_layout = QStackedLayout()
        # Define actions based on the selected index
        self.frames = [DefaultFrame, FuselageFrame, WingsFrame, NacelleFrame, LandingGearFrame, EnergyNetworkFrame]

        for frame in self.frames:
            main_layout.addWidget(frame())

        self.tree_frame = QWidget()
        # self.main_extra_frame = None  # Initialize as None

        self.tree_frame_layout = QVBoxLayout(self.tree_frame)

        # Set a background color for tree_frame
        # tree_frame_style = """
        #     background-color: navy
        # """
        # self.tree_frame.setStyleSheet(tree_frame_style)

        # Create a QComboBox and add options
        self.dropdown = QComboBox()
        options = ["Select an option", "Add Fuselage", "Add Wings", "Add Nacelles", "Add Landing Gear",
                   "Add Energy Network"]
        self.dropdown.addItems(options)

        # Style the dropdown with a colored background
        # dropdown_style = """
        #     QComboBox {
        #         background-color: coral;
        #         border: 1px solid #5A5A5A;
        #         padding: 2px;
        #     }
        #
        #     QComboBox QAbstractItemView {
        #         background-color: goldenrod;  /* You can adjust the color here */
        #         border: 1px solid #5A5A5A;
        #     }
        # """
        # self.dropdown.setStyleSheet(dropdown_style)

        self.tree_frame_layout.addWidget(self.dropdown, alignment=Qt.AlignmentFlag.AlignTop)

        # main_layout.addWidget(Color("navy"), 7)
        base_layout.addWidget(self.tree_frame, 1)
        base_layout.addLayout(main_layout, 4)

        main_layout.setSpacing(3)
        base_layout.setSpacing(3)

        main_layout.setCurrentIndex(0)

        self.setLayout(base_layout)

        # Connect the dropdown's currentIndexChanged signal to a slot
        self.dropdown.currentIndexChanged.connect(self.on_dropdown_change)

        # Initially display the DefaultFrame

    def on_dropdown_change(self, index):
        main_layout: QStackedLayout = cast(QStackedLayout, self.layout().itemAt(1))
        main_layout.setCurrentIndex(index)


def get_widget() -> QWidget:
    return GeometryWidget()
