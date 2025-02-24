
import re
import nltk

from typing import Optional
from pyzbar.pyzbar import decode
from PIL import Image
from nltk.corpus import words

# Download english words
# nltk.download('words', download_dir='nltk_data')
nltk.data.path.append('nltk_data')

_serial_number_keys = [
    "s/n",
    "sn:",
    "serial no",
    "serial:",
    "serialno",
    "serial number",
    "serialnumber",
    "s-n",
    "s.n",
    "sn",
    "ser. no",
    "ser.no",
    "ser no",
    "serno",
    "serial #",
    "serial#",
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
_serial_minimum_length = 5

def find_in_text(text: str, next_text: Optional[str])-> Optional[str]:
    keys = _keys_in_text(text)
    if len(keys) == 0:
        return None
    print(f"[Key] {keys}")
    for key in keys:
        serial_number = _find_in_text_has_key(text, key)
        if serial_number is not None:
            return serial_number
        if next_text is None:
            return None
        if len(_keys_in_text(next_text)) > 0:
            return None
        
        serial_number = _get_valid_serial_number(next_text)
        if serial_number is not None:
            return serial_number
    return None

def find_in_image(image_path: str)-> Optional[str]:
    img = Image.open(image_path)

    decoded_objects = decode(img)
    print(decoded_objects)
    if len(decoded_objects) == 0:
        return None

    try:
        text = str(decoded_objects[0].data.decode('utf-8')).lower()
        if text.startswith("http"):
            return None
        return text

    except:
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
        if _is_english(serial_number):
            return None
        if len(serial_number) >= _serial_minimum_length:  
            return serial_number
    
    return None

def _is_english(text):
    return text in words.words()
    

    
