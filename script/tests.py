#coding utf-8
#test pour comprendre comment fonctionne le parser de XML

from lxml import etree
#on parse
doc = etree.parse('./docs/AF_travail.xml')

#on obtient la racine du doc
root = doc.getroot()

# les éléments enfants : impression de l'élément (balise) --> text et teiHeader
for child in root:
    print(child.tag)

#récupérer les éléments spécifiques du mot : utiliser .iter à partir de root, qui contient la racine du doc
#besoin de spécifier le namespace car pas du XML simple mais TEI
for mot in root.iter('{http://www.tei-c.org/ns/1.0}w'):
    print(mot.text)
    #print(mot.attrib)
    attribut = mot.attrib
    print(attribut)
