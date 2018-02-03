#coding utf-8

#import des libraries
from collatex import *
import json,os

#normalement, redonne bien les données en entrée : voir la sortie json qui a les ids
#là aussi : https://github.com/interedition/collatex/blob/master/collatex-pythonport/tests/test_tokenized_json.py

# appelle de main
if __name__ == '__main__':
        #ouverture du fichier json contenant le texte
        json_data=open('./docs/sortie002.json')
        data = json.load(json_data)
        json_data.close()
        #appel de la fonction create_from_dict
        acoller = Collation.create_from_dict(data)
        #appel de la fonction collate
        graph = collate(acoller, output='json')
        graphxml = collate(acoller, output='xml')
        graphtei = collate(acoller, output='tei')
#properties_filter pour affiner le match

#écriture des fichiers
with open("./sortie/out_json_002.json", "w") as text_file:
        text_file.writelines(graph)

with open("./sortie/out_json_002.xml", "w") as text_file:
        text_file.writelines(graphxml)

with open("./sortie/out_json_002_tei.xml", "w") as text_file:
        text_file.writelines(graphtei)
#la différence entre xml et tei : xml met tout dans les app vs tei qui n'y met pas les éléments identiques
        
#sortie d'une table dans le terminal
collationText = collate(acoller,output='table')
print(collationText)
