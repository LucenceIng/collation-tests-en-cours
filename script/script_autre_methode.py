#coding utf-8

#import des libraries
from collatex import *
import json,os

#tentative pour collationer avec astar pour l'instant echec

# appelle de main
if __name__ == '__main__':
        # ouverture du fichier qui colationne sur les lemmes
        json_data=open('./docs/002_lemmes.json')
        data = json.load(json_data)
        json_data.close()
        #appel de la fonction create_from_dict
        acoller = Collation.create_from_dict(data)
        
        #ne marche pas ici
       # colle = collate(acoller, output='table')
        #appel de la fonction collate avec astar
        graphxml = collate(acoller, output='table', astar=True)
        #collate()
        #graphxml = collate(acoller, output='xml')

#écriture des fichiers
with open("./sortie/002_astar.xml", "w") as text_file:
        text_file.writelines(graphxml)