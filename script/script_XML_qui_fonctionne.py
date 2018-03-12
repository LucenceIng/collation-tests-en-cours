# coding utf-8

from collatex import *
from lxml import etree
import json,re,os,itertools

#fonctionne : de notre xml vers json avec prise en compte des éléments
# fonctionne de l'xml vers l'xml
#modifications du core_functions.py du code Collatex pour dessiner notre sortie, avec des mots et les id de chaque mot + un type 'novariance' quand ne bouge pas
#réussite pour concaténer toutes les sorties isolées en un document, avec récupération de l'id du p
# pb : code un peu sale ?
# pb : l'XSLT inutile

#définition de la classe witnessSet
class WitnessSet:
    def __init__(self,witnessList):
        self.witnessList = witnessList
    def all_witnesses(self):
        """List of tuples consisting of siglum and contents"""
        return [Witness(witness) for witness in self.witnessList]
    def all_ids(self):
        """Sorted deduplicated list of all ids in corpus"""
        return sorted(set(itertools.chain.from_iterable([witness.XML().xpath('//p/@n') for witness in self.all_witnesses()])))
    def get_lines_by_id(self,id):
        """List of tuples of siglum plus <p> element from each witness that corresponds to a certain line"""
        witnesses_with_line = []
        for witness in self.all_witnesses():
            try:
                witnesses_with_line.append((witness.siglum,witness.XML().xpath('//p[@n = ' + id + ']')[0]))
            except:
                pass
        return witnesses_with_line
    def generate_json_input(self, lineId):
        json_input = {}
        witnesses = []
        for witness in self.get_lines_by_id(lineId):
            currentWitness = {}
            currentWitness['id'] = witness[0]
            currentWitness['tokens'] = Line(witness[1]).tokens()
            witnesses.append(currentWitness)
        json_input['witnesses'] = witnesses
        return json_input

class Witness:
    """Each witness in the witness set is an instance of class Witness"""
    def __init__(self,witness):
        self.witness = witness
        self.siglum = self.witness[0]
        self.contents = self.witness[1]
    def XML(self):
        return etree.XML(self.contents)

#comment ne pas passer par une XSLT ? 
class Line:
    xsltWrapW = etree.XML('''
   <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="p">
    <xsl:element name="l">
    <xsl:attribute name="n">
    <xsl:value-of select="@n"/>
    </xsl:attribute>
    <xsl:apply-templates/>
    </xsl:element>
    </xsl:template>
    <xsl:template match="w">
        <!--<!-\- faking <xsl:for-each-group> as well as the "<<" and except" operators -\->
        <xsl:variable name="tooFar" select="following-sibling::w[1] | following-sibling::w[1]/following::node()"/>
        <w>
            <xsl:copy-of select="following-sibling::node()[count(. | $tooFar) != count($tooFar)]"/>
        </w>-->
        <xsl:element name="w">
            <xsl:attribute name="xml:id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
    ''')
    transformWrapW = etree.XSLT(xsltWrapW)
    def __init__(self,line):
        self.line = line
    def tokens(self):
        #fonctionne ?
        return [Word(token).createToken() for token in Line.transformWrapW(self.line).xpath('//w')]
        #return  [Word(token).createToken() for token in Line.xpath('//w')] 
        #print (Word(token).createToken() for token in Line.transformWrapW(self.line).xpath('//w'))
               

class Word:
    #code original :
    #unwrapRegex = re.compile('<w>(.*)</w>')
    stripTagsRegex = re.compile('<.*?>')
    def __init__(self,word):
        self.word = word
    def unwrap(self):
        return self.word.text
        #code de base
        #return Word.unwrapRegex.match(etree.tostring(self.word,encoding='unicode')).group(1)
    def attrib(self):
        return self.word.get('{http://www.w3.org/XML/1998/namespace}id')
    def normalize(self):
        return Word.stripTagsRegex.sub('',self.unwrap().lower())
    def createToken(self):
        token = {}
        token['t'] = self.unwrap()
        token['n'] = self.normalize()
        token['i'] = self.attrib()
        return token

os.listdir('./docs/coll')

witnessSet = WitnessSet([(inputFile[0],open('./docs/coll/' + inputFile,'rb').read()) for inputFile in os.listdir('./docs/coll')])

#vérification que tout se passe bien !
print(witnessSet.all_ids())


#tests pour la modification du code Collatex
#graph = collate(json_input, output='xml')
#with open("TEST_3.xml", "w") as text_file:
 #   text_file.write(graph)
#graph2 = collate(json_input, output='tei')
#with open("test_tei_3.xml", "w") as text_file:
#    text_file.write(graph2)


#création d'une variable pour opérer sur chaque ensemble en une fois
repet = witnessSet.all_ids()   
#ouverture du document destiné à accueillir tous les paragrpahes collationnés
#outfile = open('./sortie/XML_test_tout.xml', encoding='utf-8')
outfile = open('./sortie/XML_test_tout.xml', encoding='utf-8')
#création d'une liste vide pour y mettre tous les paragraphes
v = []

#boucle sur chaque paragraphe
for i in repet:
    json_input = witnessSet.generate_json_input(i)
    graph = collate(json_input, output='xml')
    #test avec NEAR graph = collate(json_input, output='xml', near_match=True, segmentation=False)
#on met le résultat de la collation d'un ensemble, ayant pour racine l'élément <p> avec le numéro qui nous permet de l'identifier
    doc = "<p n='" + i +"'>" + graph + "</p>"
#on remplit la liste au fur et à mesure
    v.append(doc)    
#lorsque la liste est complète, on la transforme en string
ensemble = str(v)

#on crée un objet dans lequel on place notre liste, à l'intérieur d'une balise racine <text>
val = "<text>" + ''.join(v) + "</text>"

#on écrit le résultat (une simple chaîne de caractères) dans notre document XML
with open("./sortie/XML_test_tout.xml", "w") as text_file:
    text_file.write(val)

#anciennement : boucle qui crée chaque document, dans un doc JSON et dans un doc XML :
#for i in repet:
 #   json_input = witnessSet.generate_json_input(i)
  #  print(json_input)
    #collationText = collate(json_input,output='table',layout='vertical')
    #print(collationText)
   # acoll = collate(json_input,output='json')
    #with open("./sortie/XML_test%s.json" % i, "w") as text_file:
    #    text_file.write(acoll)
    #graph = collate(json_input, output='xml')
    #with open("./sortie/XML_test%s.xml" % i, "w") as text_file:
   #     text_file.write(graph)


