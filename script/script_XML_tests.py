# coding utf-8

from collatex import *
from lxml import etree
import json,re,os,itertools



#on obtient la racine du doc
#root = doc.getroot()

#for mot in root.iter('{http://www.tei-c.org/ns/1.0}w'):
#    attribut = mot.attrib


#def splitId(id):
 #   """Splits @id value like 4008a into parts, for sorting"""
  #  linenoRegex = re.compile('(\d+)(.*)')
   # results = linenoRegex.match(id).groups()
    #return (int(results[0]),results[1])


class WitnessSet:
    def __init__(self,witnessList):
        self.witnessList = witnessList
    def all_witnesses(self):
        """List of tuples consisting of siglum and contents"""
        return [Witness(witness) for witness in self.witnessList]
    def all_ids(self):
        """Sorted deduplicated list of all ids in corpus"""
        return sorted(set(itertools.chain.from_iterable([witness.XML().xpath('//l/@n') for witness in self.all_witnesses()])))
    def get_lines_by_id(self,id):
        """List of tuples of siglum plus <l> element from each witness that corresponds to a certain line"""
        witnesses_with_line = []
        for witness in self.all_witnesses():
            try:
                witnesses_with_line.append((witness.siglum,witness.XML().xpath('//l[@n = ' + id + ']')[0]))
            except:
            #   print('erreur')
                pass
               #witnesses_with_line.append((witness.siglum,witness.XML().xpath('//l[@n = ' + id + ']')[0]))
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
   # XML = etree.XML(line)
    def __init__(self,line):
        self.line = line
       # self.contents=self.line
    #def XML(self):
     #   return etree.XML(self.contents)
    #pb ici
    def tokens(self):
        return [Word(token).createToken() for token in self.line().xpath('//w')]
 #   def attr(self):
  #      return [Word(token).createToken() for token in self.par.xpath('//w/@xml:id')]
    
class Word:
    unwrapRegex = re.compile('<w>(.*)</w>')
    stripTagsRegex = re.compile('<.*?>')
   # att = Par.xpath('//w/@xml:id')
    def __init__(self,word):
        self.word = word
    def unwrap(self):
        return Word.unwrapRegex.match(etree.tostring(self.word,encoding='unicode')).group(1)
    def normalize(self):
        return Word.stripTagsRegex.sub('',self.unwrap().lower())
  #  def attribute(self):
   #     return etree.tostring(self.word.xpath('@xml:id'),encoding='unicode').group(1)
    def createToken(self):
        token = {}
        token['t'] = self.unwrap()
        token['n'] = self.normalize()
    #    token['a'] = self.attribute()
        return token
#on parse


os.listdir('./docs/coll')

#coller = collate(collation, output='xml')
#A = open('./docs/coll/A.xml', 'rb')
#Ao = A.read()
#AA = Collation.add_witness("AA",Ao)

#B = open('./docs/coll/Ez.xml', 'rb')
#Ez = B.read()
#BB = Collation.add_witness(Ez)

#witnessSet=WitnessSet([AA])

witnessSet = WitnessSet([(inputFile[0],open('./docs/coll/' + inputFile,'rb').read()) for inputFile in os.listdir('./docs/coll')])



#print(witnessSet)
#récupère bien les witnesses et les id
print(witnessSet.all_witnesses())
print(witnessSet.all_ids())



test = witnessSet.generate_json_input('027')
print(test)
#json_input = witnessSet.generate_json_input('1')
#print(json_input)
#collationText = collate(json_input,output='table',layout='vertical')
#print(collationText)

#outfile = open('./sortie/XML_test.json', encoding='utf-8')
    # generation d'un objet collation a l 'aide d'un dict
#acoller = Collation.create_from_dict(test)
#print(acoller)
#graph = collate(acoller, output='json')
#collationJSON = collate(json_input,output='json')
#print(collationJSON)
#graph = collate(acoller, output='json')

#with open("./sortie/XML_test.json", "w") as text_file:
#    text_file.write(graph)



