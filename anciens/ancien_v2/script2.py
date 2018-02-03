#coding: utf-8

from collatex import *
from lxml import etree
import json,re,os,itertools

def splitId(id):
    """Splits @id value like 4008a into parts, for sorting"""
    linenoRegex = re.compile('(\d+)(.*)')
    results = linenoRegex.match(id).groups()
    return (int(results[0]),results[1])

class WitnessSet:
    def __init__(self,witnessList):
        self.witnessList = witnessList
    def all_witnesses(self):
        """List of tuples consisting of siglum and contents"""
        return [Witness(witness) for witness in self.witnessList]
    def all_ids(self):
        """Sorted deduplicated list of all ids in corpus"""
        return sorted(set(itertools.chain.from_iterable([witness.XML().xpath('//l/@id') for witness in self.all_witnesses()])),key=splitId)
    def get_lines_by_id(self,id):
        """List of tuples of siglum plus <l> element from each witness that corresponds to a certain line"""
        witnesses_with_line = []
        for witness in self.all_witnesses():
            try:
                witnesses_with_line.append((witness.siglum,witness.XML().xpath('//l[@id = ' + id + ']')[0]))
            except:
                pass
        return witnesses_with_line
    def generate_json_input(self, lineId):
        """JSON input to CollateX for an <l> segment"""
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

class Line:
    """An instance of Line is a line in a witness, expressed as an <l> element"""
    addWMilestones = etree.XML("""
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output method="xml" indent="no" encoding="UTF-8" omit-xml-declaration="yes"/>
        <xsl:template match="*|@*">
            <xsl:copy>
                <xsl:apply-templates select="node() | @*"/>
            </xsl:copy>
        </xsl:template>
        <xsl:template match="/*">
            <xsl:copy>
                <xsl:apply-templates select="@*"/>
                <!-- insert a <w/> milestone before the first word -->
                <w/>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:template>
        <!-- convert <add>, <sic>, and <crease> to milestones (and leave them that way)
             CUSTOMIZE HERE: add other elements that may span multiple word tokens
        -->
        <xsl:template match="add | sic | crease ">
            <xsl:element name="{name()}">
                <xsl:attribute name="n">start</xsl:attribute>
            </xsl:element>
            <xsl:apply-templates/>
            <xsl:element name="{name()}">
                <xsl:attribute name="n">end</xsl:attribute>
            </xsl:element>
        </xsl:template>
        <xsl:template match="note"/>
        <xsl:template match="text()">
            <xsl:call-template name="whiteSpace">
                <xsl:with-param name="input" select="translate(.,'&#x0a;',' ')"/>
            </xsl:call-template>
        </xsl:template>
        <xsl:template name="whiteSpace">
            <xsl:param name="input"/>
            <xsl:choose>
                <xsl:when test="not(contains($input, ' '))">
                    <xsl:value-of select="$input"/>
                </xsl:when>
                <xsl:when test="starts-with($input,' ')">
                    <xsl:call-template name="whiteSpace">
                        <xsl:with-param name="input" select="substring($input,2)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="substring-before($input, ' ')"/>
                    <w/>
                    <xsl:call-template name="whiteSpace">
                        <xsl:with-param name="input" select="substring-after($input,' ')"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:template>
    </xsl:stylesheet>
    """)
    transformAddW = etree.XSLT(addWMilestones)
    xsltWrapW = etree.XML('''
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
        <xsl:output method="xml" indent="no" omit-xml-declaration="yes"/>
        <xsl:template match="/*">
            <xsl:copy>
                <xsl:apply-templates select="w"/>
            </xsl:copy>
        </xsl:template>
        <xsl:template match="w">
            <!-- faking <xsl:for-each-group> as well as the "<<" and except" operators -->
            <xsl:variable name="tooFar" select="following-sibling::w[1] | following-sibling::w[1]/following::node()"/>
            <w>
                <xsl:copy-of select="following-sibling::node()[count(. | $tooFar) != count($tooFar)]"/>
            </w>
        </xsl:template>
    </xsl:stylesheet>
    ''')
    transformWrapW = etree.XSLT(xsltWrapW)
    def __init__(self,line):
        self.line = line
    def tokens(self):
        return [Word(token).createToken() for token in Line.transformWrapW(Line.transformAddW(self.line)).xpath('//w')]
    

class Word:
    unwrapRegex = re.compile('<w>(.*)</w>')
    stripTagsRegex = re.compile('<.*?>')
    def __init__(self,word):
        self.word = word
    def unwrap(self):
        return Word.unwrapRegex.match(etree.tostring(self.word,encoding='unicode')).group(1)
    def normalize(self):
        return Word.stripTagsRegex.sub('',self.unwrap().lower())
    def createToken(self):
        token = {}
        token['t'] = self.unwrap()
        token['n'] = self.normalize()
        return token



#os.listdir('textes')

#witnessSet = WitnessSet([(inputFile[0],open('textes/' + inputFile,'rb').read()) for inputFile in os.listdir('textes')])

Ao = etree.parse("AF_pour_coll2.xml")
Ez = etree.parse("MF_pour_coll2.xml")
witnessSet = WitnessSet([Ao,Ez])
 
#for lineident in witnessSet:
json_input = witnessSet.generate_json_input('027')
print(json_input)

collationJSON = collate(json_input,output='json')
print(collationJSON)

collationText = collate(json_input,output='table',layout='vertical')
print(collationText)

outfile = open('out_test.json', encoding='utf-8')
    # generation d'un objet collation a l 'aide d'un dict
acoller = Collation.create_from_dict(json_input)
    #print(collate(acoller))
graph = collate(acoller, output='json')

with open("out_test.json", "w") as text_file:
    text_file.write(graph)
    
outfile2 = open('out_test.xml',  encoding='utf-8')
graph2= collate(acoller, output='xml')
with open("out_test.xml", "w") as text_file:
    text_file.write(graph2)
    
#collationJSON = collate(json_input,output='json')
#print(collationJSON)