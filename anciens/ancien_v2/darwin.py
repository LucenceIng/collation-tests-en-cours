
import json
from collatex import collate, Collation

if __name__ == '__main__':
    # lecture des donnees JSON dans un dictionnaire
    json_data=open('darwin.json')
    data = json.load(json_data)
    json_data.close()

    # generation d'un objet collation a l 'aide d'un dict
    collation = Collation.create_from_dict(data)

    print(collate(collation))
