
from typing import List, Dict, Any

class BrowserUtils:

    def __init__(self,driver):
        self.driver = driver

    def getPageTitle(self):
        return self.driver.title


    def print_css_properties(self, element, properties: List[str] = None, label_map: Dict[str, str] = None) -> None:
        """
        Print CSS properties for a WebElement.
        - element: selenium WebElement
        - properties: list of CSS property names (defaults to background-color, color, font-size)
        - label_map: optional dict to map property names to custom labels for printing
        """
        if properties is None:
            properties = ["background-color", "color", "font-size"]
        for prop in properties:
            label = label_map.get(prop) if label_map and prop in label_map else prop.replace("-", " ").title()
            try:
                value = element.value_of_css_property(prop)
            except Exception:
                value = None
            print(label, value)

