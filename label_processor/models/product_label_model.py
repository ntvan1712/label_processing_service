import json
from typing import Optional

class ProductLabelModel:
    def __init__(
            self, 
            serial_number: str,
            manufacturer: Optional[str], 
            country_of_origin: Optional[str], 
            all_words: list[str]
        ):
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.made_in = country_of_origin
        self.all_words = all_words

    def to_json(self) -> str:
        return json.dumps({
            "serial_number": self.serial_number,
            "manufacturer": self.manufacturer,
            "made_in": self.made_in,
            "all_words": self.all_words
        }, ensure_ascii=False, indent=4)