from typing import Optional


_manufacturers = [
    # Hãng máy tính và laptop
    "apple", "dell", "hp", "lenovo", "asus", "acer", "microsoft",
    "msi", "razer", "huawei", "gigabyte", "toshiba", "sony", "samsung",
    "lg", "xiaomi", "alienware", "panasonic", "vaio", "nvidia", 
    
    # Hãng sản xuất chuột và bàn phím
    "logitech", "razer", "steelseries", "corsair", "cooler master", "hyperx", "asus rog",
    "redragon", "zowie", "glorious", "gigabyte", "fuhlen",
    
    # Đồ điện tử khác
    "sennheiser", "bose", "sony", "jbl", "anker", "beats", "philips",
    "plantronics", "vizio", "yamaha", "samsung", "sharp", "lg", "panasonic",
    "vivo", "oneplus", "oppo", "realme", "google", "nokia", "htc", "epson", "brother",
]

def find_in_words(words: list[str])-> Optional[str]:
    for word in words:
        cleaned_word = word.strip(" .,:;!?")
        if word in _manufacturers:
            return cleaned_word