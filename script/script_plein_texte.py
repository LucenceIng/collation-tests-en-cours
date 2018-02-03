
from collatex import *

#tests sur plein texte pour voir résultats : même résultats, même quand très peu de texte
collation = Collation()
#A = "Qant vint au chief de dishuit anz un po aprés la Pentecoste si fu alez en bois si ot trové un si grant cerf"
#B = "Quant vint au chief de xviii ans ung peu apres la penthecouste il ala au boys et trouva ung si grant cerf"

C = "Qant vint au chief de dishuit "
D = "Quant vint au chief de xviii ans"

#collation.add_plain_witness("Ao", A)
#collation.add_plain_witness("Ez", B)
collation.add_plain_witness("Ao2",C)
collation.add_plain_witness("Ez2",D)

#coller = collate(collation, output='xml')
coller2 = collate(collation, output='xml')

#with open("./sortie/002_texte.xml", "w") as text_file:
#        text_file.writelines(coller)
        
with open("./sortie/002_texte2.xml", "w") as text_file:
        text_file.writelines(coller2)

collationText = collate(collation,output='table')
print(collationText)