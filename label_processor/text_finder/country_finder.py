from typing import Optional


_countries = [
    "united states", "canada", "china", "japan", "germany", "france", "united kingdom",
    "italy", "south korea", "india", "brazil", "australia", "russia", "mexico",
    "netherlands", "turkey", "spain", "switzerland", "saudi arabia", "argentina",
    "sweden", "indonesia", "south africa", "vietnam", "malaysia", "singapore",
    "thailand", "philippines", "new zealand", "norway", "denmark", "finland",
    "poland", "austria", "belgium", "portugal", "ireland", "greece", "hungary",
    "czech republic", "israel", "egypt", "pakistan", "bangladesh", "iran", "iraq",
    "ukraine", "kazakhstan", "chile", "colombia", "peru", "usa", "uk"
]

def find_in_words(words: list[str])-> Optional[str]:
    for word in words:
        cleaned_word = word.strip(" .,:;!?")
        if word in _countries:
            return cleaned_word
