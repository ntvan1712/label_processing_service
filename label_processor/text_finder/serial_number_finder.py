
import re
from typing import Optional


_serial_number_keys = [
    "s/n",
    "sn",
    "serial no",
    "serial number",
    "s-n",
    "s.n",
    "ser. no",
    "ser no",
    "serial #",
    "ser#",
    "sr. no",
    "sr no",
    "s/n#",
    "serialnum",
    "serial code",
    "s/n code",
    "sn#",
    "serial id",
    "s/n id"
]

_serial_number_pattern = re.compile(r'[a-zA-Z0-9\-\/]+')
_serial_minimum_length = 1

def find_in_text(text: str, next_text: Optional[str])-> Optional[str]:
    keys = _keys_in_text(text)
    if len(keys) == 0:
        return None
    print(f"[Key] {keys}")
    for key in keys:
        serial_number = _find_in_text_has_key(text, key)
        if serial_number is not None:
            return serial_number
        
        if len(_keys_in_text(next_text)) > 0:
            return None
        
        serial_number = _get_valid_serial_number(next_text)
        if serial_number is not None:
            return serial_number
    return None

# if text has key, return key, else, return None
def _keys_in_text(text: str)-> list[str]:
    keys = []
    for key in _serial_number_keys:
        if key in text:
            keys.append(key)  
    
    return keys


def _find_in_text_has_key(text: str, key: str) -> Optional[str]:
    after_key_text = text.split(key, 1)[-1].strip(" :.,-_|")
    print(f"[after_key_text] {after_key_text}")
    if after_key_text is None or after_key_text == "":
        print('after key text none')
        return None
    return _get_valid_serial_number(after_key_text)

def _get_valid_serial_number(text: str) -> Optional[str]:
    match = _serial_number_pattern.search(text)
    print(f"[match] {match}")
    
    if match:
        serial_number = match.group(0)
        if len(serial_number) >= _serial_minimum_length:  
            return serial_number
    
    return None
