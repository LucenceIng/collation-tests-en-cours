from collatex import *

#test
#si on ajoute une espace après le mot, la restitue et donc devient lisible : astuce
#mais sinon, même sur ce court passage très similaire, met plusieurs mots dans un rdg même quand même mot
tokens_a =  [{
        "-xml:id": "Ao_w_000256",
        "lemme" : "cant1",
        "t": "Qant "
        },
        {
        "-xml:id": "Ao_w_000257",
        "lemme" : "venir",
        "t": "vint "
        },
        {
        "-xml:id": "Ao_w_000258",
        "lemme" : "a3+le",
        "t": "au "
        },
        {
        "-xml:id": "Ao_w_000259",
        "lemme" : "chief1",
        "t": "chief "
        },
        {
        "-xml:id": "Ao_w_000260",
        "lemme" : "de",
        "t": "de "
        },
        {
        "-xml:id": "Ao_w_000261",
        "lemme" : "dis+huit",
        "t": "dishuit "
        },
        {
        "-xml:id": "Ao_w_000262",
        "lemme" : "an",
        "t": "anz "
        }]
tokens_b = [ {
        "-xml:id": "Ez_w_000809",
        "lemme" : "cant1",
        "t": "Quant "
        },{
        "-xml:id": "Ez_w_000810",
        "lemme" : "venir",
        "t": "vint "
        },{
        "-xml:id": "Ez_w_000811",
        "lemme" : "a3+le",
        "t": "au "
        },{
        "-xml:id": "Ez_w_000812",
        "lemme" : "chief1",
        "t": "chief "
        },{
        "-xml:id": "Ez_w_000813",
        "lemme" : "de",
        "t": "de "
        },{
        "-xml:id": "Ez_w_000814",
        "lemme" : "dis+huit",
        "t": "xviii "
        },{
        "-xml:id": "Ez_w_000815",
        "lemme" : "an",
        "t": "ans "
        } ]

#ce que propose le site et qui ne marche pas :
#witness_a = { "id": "A", "tokens": tokens_a }
#print( witness_a )
#witness_b = { "id": "B", "tokens": tokens_b }
#JSON_input = { "witnesses": [ witness_a, witness_b ] }
#result = collate_pretokenized_json( JSON_input, output='table' )
#print( result )
#result= collate()

witness_a = { "id": "A", "tokens": tokens_a }
witness_b = { "id": "B", "tokens": tokens_b }
JSON_input = { "witnesses": [ witness_a, witness_b ] }
test = Collation.create_from_dict(JSON_input)
testjson = collate(test, output='xml')

with open(".sortie/test_out.xml", "w") as text_file:
        text_file.writelines(testjson)