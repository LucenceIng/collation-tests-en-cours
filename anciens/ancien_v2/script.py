#coding utf-8
#! /usr/bin/python3
 # error : arrive pas a importer collatex 

from collatex import *
#import pprint
import json,os
#import sys
#is_py2 = sys.version[0] == '2'
#if is_py2:
#    import Queue as queue
#else:
 #   import queue as queue

#f=open('test2.txt')
#data=json.dumps(json_data)
#json_data2=open('AF.json')
#print(type(f))

#data = json.load(f)
#print(data)
#data2 = json.load(json_data2)

#print type(data)
#pprint(data)
#ppprint(data2)

#json_collation = Collation()
#json_collation.add_witness(witness)

#collation = Collation()
#collation.add_witness(json_data)

#class Collation():

    # json_data can be a string or a file
#    def create_from_json(cls, json_data):
#       data = json.load(json_data)
#       collation = cls.create_from_dict(data)
#       return collation
#info = json.loads(js.decode("utf-8"))
#collation1 = Collation()
#filename = "test2.json"
#f = open(filename)


#collation1.create_from_json('test2.json')

#witnessSet = (inputFile[0],open('docs/' + inputFile,'rb').read()) for inputFile in os.listdir('docs')])


if __name__ == '__main__':
    # lecture des donnees JSON dans un dictionnaire
    #json_data=inputFile[0],open('docs/' + inputFile,'rb')
    #data = json.load(json_data)
    #json_data.close()
    
    
  #  json_data2=open('sortie20.json')
   # data2 = json.load(json_data2)
    #json_data2.close()
   # os.listdir('docs')
    #os.listdir('sortie')
    #for inputFile in os.listdir('docs'):
        #inputFile[0],open('docs/' + inputFile,'rb')
        #print(inputFile)
        data = json.load(inputFile)
        inputFile.close()
        outfile = open('sortie/', encoding='utf-8')
    # generation d'un objet collation a l 'aide d'un dict

        acoller = Collation.create_from_dict(data)
    #print(collate(acoller))
        graph = collate(acoller, output='xml')

        with open("out_test.xml", "w") as text_file:
            text_file.write(graph)
 #   collation2 = Collation.create_from_dict(data2)

#graph = collate(collation, output='json')
#    graph2 = collate(collation2, output='json')
    #print(graph)
    #sortie = collate(collation, output='html2')
    #permet de sauvegarder le fichier (tout format possible, on modifie en meme temps, le output cidessus)
#with open("out_test.xml", "w") as text_file:
#    text_file.write(graph)
#with open("out_test.json") as text_file:
 #   text_file.w(graph)

#with open("out_test2.json") as text_file2:
#    text_file2.w(graph2)
#collation = Collation.create_from_dict(data)

   
    
   # print(graph)
#alignment_table = collate(collation)
#print(alignment_table)

#collation.add_plain_witness("A", data)
#collation.add_plain_witness("B", data2)

#alignment_table = collate(collation)
#collate_pretokenized_json(witness.json,output='json')

