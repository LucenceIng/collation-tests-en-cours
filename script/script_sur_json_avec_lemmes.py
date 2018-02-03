#coding utf-8

#import des libraries
from collatex import *
import json,os


# appelle de main
if __name__ == '__main__':
        #ouverture du fichier json contenant le texte : avec lemmes
        json_data=open('./docs/002_avec_lemme.json')
        data = json.load(json_data)
        json_data.close()
        # ouverture du fichier qui colationne sur les lemmes
        json_data2=open('./docs/002_lemmes.json')
        data2 = json.load(json_data2)
        json_data2.close()
        #ouverture du fichier qui ne contient que les lemmes : même résultats que avec tout en collationant sur les lemmes
        json_data3=open('./docs/002_QUE_lemmes.json')
        data3 = json.load(json_data3)
        json_data3.close()
        #appel de la fonction create_from_dict sur les trois versions
        acoller = Collation.create_from_dict(data)
        acoller2 = Collation.create_from_dict(data2)
        acoller3 = Collation.create_from_dict(data3)
        
        #test avec create_from_json : meme resultat
        json_datatest=open('./docs/002_lemmes.json')
        test = Collation.create_from_json(json_datatest)
        testjson = collate(test, output='json')
        testgraph = collate(test, output='xml')
        with open("./sortie/test.xml", "w") as text_file:
                text_file.writelines(testgraph)
        with open("./sortie/test.json", "w") as text_file:
                text_file.writelines(testjson)
        # fin du test 
        
        #appel de la fonction collate
        graph = collate(acoller, output='json')
        graphxml = collate(acoller, output='xml')
        graph2 = collate(acoller2, output='json')
        graphxml2 = collate(acoller2, output='xml')
        graphtei2 = collate(acoller2, output='tei')
        graph3 = collate(acoller3, output='xml')
#properties_filter pour affiner le match

#écriture des fichiers
with open("./sortie/out_json_002_lemme.json", "w") as text_file:
        text_file.writelines(graph)

with open("./sortie/out_json_002_lemme.xml", "w") as text_file:
        text_file.writelines(graphxml)

#les deux fichiers qui collationnent sur les lemmes
with open("./sortie/out_002_lemmes.json", "w") as text_file:
        text_file.writelines(graph2)

with open("./sortie/out_002_lemmes.xml", "w") as text_file:
        text_file.writelines(graphxml2)       
#on écrit le fichier TEI pour les lemmes
with open("./sortie/out_002_lemmes_tei.xml", "w") as text_file:
        text_file.writelines(graphtei2)
      
#on écrit le fichier qui ne collationne que les lemmes
with open("./sortie/002_QUE_lemmes.xml", "w") as text_file:
        text_file.writelines(graph3) 


#sortie d'une table dans le terminal
collationText = collate(acoller,output='table')
print(collationText)
collation2 = collate(acoller2, output='table')
print(collation2)
