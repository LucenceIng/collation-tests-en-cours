# coding utf-8

from collatex import *
from lxml import etree
import json,re,os,itertools

#fonctionne : de xml vers xml, avec prise en compte des ids, collation sur les lemmes et sortie complète
# ajout 12/02/2018 pour compléter l'apparat, avec des rdg vides
#XLST inutile


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
            <xsl:if test="@lemma">
            <xsl:attribute name="lemma">
                <xsl:value-of select="@lemma"/>
            </xsl:attribute>
            </xsl:if>
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
    ''')
    transformWrapW = etree.XSLT(xsltWrapW)
    def __init__(self,line):
        self.line = line
    def tokens(self):
        return [Word(token).createToken() for token in Line.transformWrapW(self.line).xpath('//w')]
               

class Word:
    #unwrapRegex = re.compile('<w>(.*)</w>')
    #stripTagsRegex = re.compile('<.*?>')
    def __init__(self,word):
        self.word = word
    def unwrap(self):
        return self.word.text
        #code de base
        #return Word.unwrapRegex.match(etree.tostring(self.word,encoding='unicode')).group(1)
    def attribut(self):
        return self.word.get('{http://www.w3.org/XML/1998/namespace}id')
    def lemma(self):
        return self.word.get('lemma')
    #on enlève normalize : la collation s'effectue ici, donc on place la valeur du lemme à l'intérieur de ce normalize
    #def normalize(self):
     #   return Word.stripTagsRegex.sub('',self.unwrap().lower())
    def createToken(self):
        token = {}
        token['t'] = self.unwrap()
        token['n'] = self.lemma()
        token['i'] = self.attribut()
        return token


os.listdir('./docs/coll_002')

witnessSet = WitnessSet([(inputFile[0],open('./docs/coll_002/' + inputFile,'rb').read()) for inputFile in os.listdir('./docs/coll_002')])


print(witnessSet.all_ids())
print(witnessSet.witnessList)

json_input = witnessSet.generate_json_input('002')
print(json_input)

graph = collate(json_input, output='xml')
with open("./sortie/xml_002_complete.xml", "w") as text_file:
    text_file.write(graph)





