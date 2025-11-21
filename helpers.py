import json

def load_data():

    with open("patients_data.json", "r") as file:
        data = json.load(file)
    return data

data=load_data()
print(type(data))