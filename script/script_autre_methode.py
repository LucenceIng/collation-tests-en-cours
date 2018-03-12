#coding utf-8

#import des libraries
from collatex import *
import json,os


#tentative pour collationer avec astar et avec detect_transpositions pour l'instant echec

# appelle de main
if __name__ == '__main__':
        # ouverture du fichier qui colationne sur les lemmes (test petit, fichier court)
        json_data=open('./docs/002_lemmes.json')
        data = json.load(json_data)
        json_data.close()
        #appel de la fonction create_from_dict
        test = Collation.create_from_dict(data)
        print(test)
        #appel de la fonction collate avec detect_transpositions : fonctionne pas
        #graphxml = collate(test, detect_transpositions=True)
        #fonctionne pas non plus avec astar
        #graphxml = collate(test, near_match=False, debug_scores=False, astar=True)
        #ici, bien : permet une collation plus proche des mots
        graphxml = collate(test, output='svg')
       # print(graphxml)
        #tester = collate(graphxml, astar=True)
#graphxml.plt.savefig('test.pdf')
#écriture des fichiers
#with open("./sortie/002_trans.html") as text_file:
#        text_file.write(graphxml)
        
        
        #erreurs quand astar et quand detect_transpositions