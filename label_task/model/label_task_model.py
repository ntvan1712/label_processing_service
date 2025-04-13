class LabelTaskModel:
    def __init__(self, json_data):
        self.id = json_data.get("id")
        self.path = json_data.get("path")
