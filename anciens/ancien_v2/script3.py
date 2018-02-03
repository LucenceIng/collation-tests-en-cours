#coding utf-8

from collatex import *
from lxml import etree
import json,re

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
    def siglum(self):
        return str(etree.XML(self.line).xpath('/p/@source')[0])
    def tokens(self):
        return [Word(token).createToken() for token in Line.transformWrapW(Line.transformAddW(etree.XML(self.line))).xpath('//w')]

class Word:
    unwrapRegex = re.compile('<w>(.*)</w>')
    stripTagsRegex = re.compile('<.*?>')
    def __init__(self,word):
        self.word = word
    def unwrap(self):
        return self.word.text
        #
        #Word.unwrapRegex.match(etree.tostring(self.word,encoding='unicode')).group(1)
    def normalize(self):
        return Word.stripTagsRegex.sub('',self.unwrap().lower())
    def createToken(self):
        token = {}
        token['t'] = self.unwrap()
        token['n'] = self.normalize()
        return token
    
#Ao = etree.parse("AF_pour_coll.xml")
#Ez = etree.parse("MF_pour_coll.xml")



A = """<p n="001" source="Ao">
   <w xml:id="Ao_w_000047">Or</w>
   <w xml:id="Ao_w_000048">dit</w>
   <w xml:id="Ao_w_000049">li</w>
   <w xml:id="Ao_w_000050">contes</w>
   <w xml:id="Ao_w_000051">que</w>
   <w xml:id="Ao_w_000052">tant</w>
   <w xml:id="Ao_w_000053">a</w>
   <w xml:id="Ao_w_000054">esté</w>
   <w xml:id="Ao_w_000056">en</w>
   <w xml:id="Ao_w_000057">la</w>
   <w xml:id="Ao_w_000058">garde</w>
   <w xml:id="Ao_w_000059">a</w>
   <w xml:id="Ao_w_000060">la</w>
   <w xml:id="Ao_w_000064">que</w>
   <w xml:id="Ao_w_000065">bien</w>
   <w xml:id="Ao_w_000066">est</w>
   <w xml:id="Ao_w_000067">en</w>
   <w xml:id="Ao_w_000068">l</w>
   <w xml:id="Ao_w_000069">aage</w>
   <w xml:id="Ao_w_000070">de</w>
   <w xml:id="Ao_w_000071">dishuit</w>
   <w xml:id="Ao_w_000072">anz</w>
   <w xml:id="Ao_w_000073">Si</w>
   <w xml:id="Ao_w_000074">est</w>
   <w xml:id="Ao_w_000075">tant</w>
   <w xml:id="Ao_w_000076">biax</w>
   <w xml:id="Ao_w_000077">vallez</w>
   <w xml:id="Ao_w_000078">que</w>
   <w xml:id="Ao_w_000079">por</w>
   <w xml:id="Ao_w_000080">neiant</w>
   <w xml:id="Ao_w_000081">queïst</w>
   <w xml:id="Ao_w_000082">l</w>
   <w xml:id="Ao_w_000083">an</w>
   <w xml:id="Ao_w_000084">nul</w>
   <w xml:id="Ao_w_000085">plus</w>
   <w xml:id="Ao_w_000086">bel</w>
   <w xml:id="Ao_w_000087">en</w>
   <w xml:id="Ao_w_000088">tot</w>
   <w xml:id="Ao_w_000089">lo</w>
   <w xml:id="Ao_w_000090">monde</w>
   <w xml:id="Ao_w_000091">et</w>
   <w xml:id="Ao_w_000092">tant</w>
   <w xml:id="Ao_w_000093">sages</w>
   <w xml:id="Ao_w_000094">que</w>
   <w xml:id="Ao_w_000095">nule</w>
   <w xml:id="Ao_w_000096">chose</w>
   <w xml:id="Ao_w_000097">ne</w>
   <w xml:id="Ao_w_000098">estoit</w>
   <w xml:id="Ao_w_000099">dont</w>
   <w xml:id="Ao_w_000100">l</w>
   <w xml:id="Ao_w_000101">an</w>
   <w xml:id="Ao_w_000102">lo</w>
   <w xml:id="Ao_w_000103">poïst</w>
   <w xml:id="Ao_w_000104">a</w>
   <w xml:id="Ao_w_000105">droit</w>
   <w xml:id="Ao_w_000106">ne</w>
   <w xml:id="Ao_w_000107">blasmer</w>
   <w xml:id="Ao_w_000108">ne</w>
   <w xml:id="Ao_w_000109">reprandre</w>
   <w xml:id="Ao_w_000110">en</w>
   <w xml:id="Ao_w_000111">nule</w>
   <w xml:id="Ao_w_000112">ovre</w>
   <w xml:id="Ao_w_000113">que</w>
   <w xml:id="Ao_w_000114">il</w>
   <w xml:id="Ao_w_000115">feïst</w>
   <w xml:id="Ao_w_000116">Qant</w>
   <w xml:id="Ao_w_000117">il</w>
   <w xml:id="Ao_w_000118">fut</w>
   <w xml:id="Ao_w_000119">an</w>
   <w xml:id="Ao_w_000120">aage</w>
   <w xml:id="Ao_w_000121">de</w>
   <w xml:id="Ao_w_000122">dishuit</w>
   <w xml:id="Ao_w_000123">anz</w>
   <w xml:id="Ao_w_000124">si</w>
   <w xml:id="Ao_w_000125">fu</w>
   <w xml:id="Ao_w_000126">a</w>
   <w xml:id="Ao_w_000127">mervoilles</w>
   <w xml:id="Ao_w_000128">granz</w>
   <w xml:id="Ao_w_000129">et</w>
   <w xml:id="Ao_w_000130">corssuz</w>
   <w xml:id="Ao_w_000131">et</w>
   <w xml:id="Ao_w_000132">la</w>
   <w xml:id="Ao_w_000133">dame</w>
   <w xml:id="Ao_w_000134">qui</w>
   <w xml:id="Ao_w_000135">lo</w>
   <w xml:id="Ao_w_000136">norrissoit</w>
   <w xml:id="Ao_w_000137">voit</w>
   <w xml:id="Ao_w_000138">bien</w>
   <w xml:id="Ao_w_000139">que</w>
   <w xml:id="Ao_w_000140">bien</w>
   <w xml:id="Ao_w_000141">est</w>
   <w xml:id="Ao_w_000142">des</w>
   <w xml:id="Ao_w_000143">ores</w>
   <w xml:id="Ao_w_000144">mais</w>
   <w xml:id="Ao_w_000145">tans</w>
   <w xml:id="Ao_w_000146">et</w>
   <w xml:id="Ao_w_000147">raisons</w>
   <w xml:id="Ao_w_000148">qu</w>
   <w xml:id="Ao_w_000149">il</w>
   <w xml:id="Ao_w_000150">reçoive</w>
   <w xml:id="Ao_w_000151">l</w>
   <w xml:id="Ao_w_000152">ordre</w>
   <w xml:id="Ao_w_000153">de</w>
   <w xml:id="Ao_w_000154">chevalerie</w>
   <w xml:id="Ao_w_000155">et</w>
   <w xml:id="Ao_w_000156">se</w>
   <w xml:id="Ao_w_000157">ele</w>
   <w xml:id="Ao_w_000158">plus</w>
   <w xml:id="Ao_w_000159">li</w>
   <w xml:id="Ao_w_000160">delaoit</w>
   <w xml:id="Ao_w_000161">ce</w>
   <w xml:id="Ao_w_000162">seroit</w>
   <w xml:id="Ao_w_000163">pechiez</w>
   <w xml:id="Ao_w_000164">et</w>
   <w xml:id="Ao_w_000165">dolors</w>
   <w xml:id="Ao_w_000166">car</w>
   <w xml:id="Ao_w_000167">bien</w>
   <w xml:id="Ao_w_000168">savoit</w>
   <w xml:id="Ao_w_000169">par</w>
   <w xml:id="Ao_w_000170">sa</w>
   <w xml:id="Ao_w_000171">sort</w>
   <w xml:id="Ao_w_000172">que</w>
   <w xml:id="Ao_w_000173">maintes</w>
   <w xml:id="Ao_w_000174">foiz</w>
   <w xml:id="Ao_w_000175">avoit</w>
   <w xml:id="Ao_w_000176">gitee</w>
   <w xml:id="Ao_w_000177">qu</w>
   <w xml:id="Ao_w_000178">il</w>
   <w xml:id="Ao_w_000179">vandroit</w>
   <w xml:id="Ao_w_000180">encor</w>
   <w xml:id="Ao_w_000181">a</w>
   <w xml:id="Ao_w_000182">mout</w>
   <w xml:id="Ao_w_000183">grant</w>
   <w xml:id="Ao_w_000184">chose</w>
   <w xml:id="Ao_w_000185">Et</w>
   <w xml:id="Ao_w_000186">se</w>
   <w xml:id="Ao_w_000187">ele</w>
   <w xml:id="Ao_w_000188">lo</w>
   <w xml:id="Ao_w_000189">poïst</w>
   <w xml:id="Ao_w_000190">encores</w>
   <w xml:id="Ao_w_000191">delaier</w>
   <w xml:id="Ao_w_000192">de</w>
   <w xml:id="Ao_w_000193">prendre</w>
   <w xml:id="Ao_w_000194">chevalerie</w>
   <w xml:id="Ao_w_000195">ele</w>
   <w xml:id="Ao_w_000196">lo</w>
   <w xml:id="Ao_w_000197">feïst</w>
   <w xml:id="Ao_w_000198">mout</w>
   <w xml:id="Ao_w_000199">volentiers</w>
   <w xml:id="Ao_w_000200">car</w>
   <w xml:id="Ao_w_000201">a</w>
   <w xml:id="Ao_w_000202">mout</w>
   <w xml:id="Ao_w_000203">grant</w>
   <w xml:id="Ao_w_000204">paines</w>
   <w xml:id="Ao_w_000205">se</w>
   <w xml:id="Ao_w_000206">porra</w>
   <w xml:id="Ao_w_000207">consirrer</w>
   <w xml:id="Ao_w_000208">de</w>
   <w xml:id="Ao_w_000209">lui</w>
   <w xml:id="Ao_w_000210">car</w>
   <w xml:id="Ao_w_000211">totes</w>
   <w xml:id="Ao_w_000212">amors</w>
   <w xml:id="Ao_w_000213">de</w>
   <w xml:id="Ao_w_000214">pitié</w>
   <w xml:id="Ao_w_000215">et</w>
   <w xml:id="Ao_w_000216">de</w>
   <w xml:id="Ao_w_000217">norreture</w>
   <w xml:id="Ao_w_000218">i</w>
   <w xml:id="Ao_w_000219">avoit</w>
   <w xml:id="Ao_w_000220">mises</w>
   <w xml:id="Ao_w_000221">mais</w>
   <w xml:id="Ao_w_000222">se</w>
   <w xml:id="Ao_w_000223">ele</w>
   <w xml:id="Ao_w_000224">outre</w>
   <w xml:id="Ao_w_000225">son</w>
   <w xml:id="Ao_w_000226">droit</w>
   <w xml:id="Ao_w_000227">aage</w>
   <w xml:id="Ao_w_000228">lo</w>
   <w xml:id="Ao_w_000229">detenoit</w>
   <w xml:id="Ao_w_000230">d</w>
   <w xml:id="Ao_w_000231">estre</w>
   <w xml:id="Ao_w_000232">chevaliers</w>
   <w xml:id="Ao_w_000233">et</w>
   <w xml:id="Ao_w_000234">destornoit</w>
   <w xml:id="Ao_w_000235">ele</w>
   <w xml:id="Ao_w_000236">feroit</w>
   <w xml:id="Ao_w_000237">pechié</w>
   <w xml:id="Ao_w_000238">mortel</w>
   <w xml:id="Ao_w_000239">si</w>
   <w xml:id="Ao_w_000240">grant</w>
   <w xml:id="Ao_w_000241">comme</w>
   <w xml:id="Ao_w_000242">de</w>
   <w xml:id="Ao_w_000243">traïson</w>
   <w xml:id="Ao_w_000244">car</w>
   <w xml:id="Ao_w_000245">ele</w>
   <w xml:id="Ao_w_000246">li</w>
   <w xml:id="Ao_w_000247">toudroit</w>
   <w xml:id="Ao_w_000248">ce</w>
   <w xml:id="Ao_w_000249">a</w>
   <w xml:id="Ao_w_000250">quoi</w>
   <w xml:id="Ao_w_000251">il</w>
   <w xml:id="Ao_w_000252">ne</w>
   <w xml:id="Ao_w_000253">porroit</w>
   <w xml:id="Ao_w_000254">recovrer</w>
   <w xml:id="Ao_w_000255">legierement</w>
</p>"""
B = """<p n="001" source="Ez">
   <w xml:id="Ez_w_000732">Cant</w>
   <w xml:id="Ez_w_000733">a</w>
   <w xml:id="Ez_w_000734">este</w>
   <w xml:id="Ez_w_000736">en</w>
   <w xml:id="Ez_w_000737">la</w>
   <w xml:id="Ez_w_000738">garde</w>
   <w xml:id="Ez_w_000739">de</w>
   <w xml:id="Ez_w_000740">la</w>
   <w xml:id="Ez_w_000744">qu</w>
   <w xml:id="Ez_w_000745">il</w>
   <w xml:id="Ez_w_000746">est</w>
   <w xml:id="Ez_w_000747">en</w>
   <w xml:id="Ez_w_000748">l</w>
   <w xml:id="Ez_w_000749">aage</w>
   <w xml:id="Ez_w_000750">de</w>
   <w xml:id="Ez_w_000751">xviii</w>
   <w xml:id="Ez_w_000752">ans</w>
   <w xml:id="Ez_w_000753">et</w>
   <w xml:id="Ez_w_000754">estoit</w>
   <w xml:id="Ez_w_000755">tant</w>
   <w xml:id="Ez_w_000756">beau</w>
   <w xml:id="Ez_w_000757">que</w>
   <w xml:id="Ez_w_000758">de</w>
   <w xml:id="Ez_w_000759">son</w>
   <w xml:id="Ez_w_000760">aage</w>
   <w xml:id="Ez_w_000761">n</w>
   <w xml:id="Ez_w_000762">avoit</w>
   <w xml:id="Ez_w_000763">son</w>
   <w xml:id="Ez_w_000764">pareil</w>
   <w xml:id="Ez_w_000765">en</w>
   <w xml:id="Ez_w_000766">tout</w>
   <w xml:id="Ez_w_000767">le</w>
   <w xml:id="Ez_w_000768">monde</w>
   <w xml:id="Ez_w_000769">et</w>
   <w xml:id="Ez_w_000770">tant</w>
   <w xml:id="Ez_w_000771">saige</w>
   <w xml:id="Ez_w_000772">que</w>
   <w xml:id="Ez_w_000773">merveilles</w>
   <w xml:id="Ez_w_000774">La</w>
   <w xml:id="Ez_w_000775">dame</w>
   <w xml:id="Ez_w_000776">voit</w>
   <w xml:id="Ez_w_000777">bien</w>
   <w xml:id="Ez_w_000778">que</w>
   <w xml:id="Ez_w_000779">desormais</w>
   <w xml:id="Ez_w_000780">il</w>
   <w xml:id="Ez_w_000781">estoit</w>
   <w xml:id="Ez_w_000782">temps</w>
   <w xml:id="Ez_w_000783">qu</w>
   <w xml:id="Ez_w_000784">il</w>
   <w xml:id="Ez_w_000785">receust</w>
   <w xml:id="Ez_w_000786">lordre</w>
   <w xml:id="Ez_w_000787">de</w>
   <w xml:id="Ez_w_000788">chevalerie</w>
   <w xml:id="Ez_w_000789">et</w>
   <w xml:id="Ez_w_000790">que</w>
   <w xml:id="Ez_w_000791">se</w>
   <w xml:id="Ez_w_000792">plus</w>
   <w xml:id="Ez_w_000793">l</w>
   <w xml:id="Ez_w_000794">en</w>
   <w xml:id="Ez_w_000795">destournoit</w>
   <w xml:id="Ez_w_000796">ce</w>
   <w xml:id="Ez_w_000797">seroit</w>
   <w xml:id="Ez_w_000798">pechie</w>
   <w xml:id="Ez_w_000799">car</w>
   <w xml:id="Ez_w_000800">bien</w>
   <w xml:id="Ez_w_000801">savoit</w>
   <w xml:id="Ez_w_000802">qu</w>
   <w xml:id="Ez_w_000803">il</w>
   <w xml:id="Ez_w_000804">viendroit</w>
   <w xml:id="Ez_w_000805">encores</w>
   <w xml:id="Ez_w_000806">a</w>
   <w xml:id="Ez_w_000807">grant</w>
   <w xml:id="Ez_w_000808">chose</w>
</p>"""


witnessSet = WitnessSet([A,B])


#witnessSet = WitnessSet([Ao,Ez])

json_input = witnessSet.generate_json_input("2")
print(json_input)

#outfile = open('out_test.xml', encoding='utf-8')
    # generation d'un objet collation a l 'aide d'un dict

acoller = Collation.create_from_dict(json_input)
    #print(collate(acoller))
graph = collate(acoller, output='xml')

with open("out_test.xml", "w") as text_file:
    text_file.write(graph)


#collationText = collate_pretokenized_json(json_input,output='table',layout='vertical')
#print(collationText)
#collationJSON = collate_pretokenized_json(json_input,output='json')
#print(collationJSON)