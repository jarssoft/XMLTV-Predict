import descparser

descs=[
    'Kausi 1. Jakso 21/26. Bing on kolmevuotias pikkuinen pupu, joka ystäviensä avustamana oppii joka päivä jotain uutta ja selviytyy taaperoille tutuista elämän haasteista. Lastenohjelma. (7\') Ohjelman tekstitys teksti-tv:n sivulla 333.',
    'Böjligare rygg och rörligare axlar i Gympastunden på tisdagarna.',
    'Kausi 4. Jakso 17/40. Kleingarten. Nicole on viettänyt lapsuutensa Saksassa ja haluaa pihaansa siirtolapuutarhapalstan eli kleingartenin. Puutarhaan tulee erilaisia kukkia ja vihannespenkki, mutta pihan keskipisteenä on',
    'Kausi 9. Jakso 3/29. Eri maailmoista. Entinen Miss Wales Imogen Thomas etsii herrasmiestä, joka osaa hemmotella naistaan. Adrenaliiniaddikti, rocktähti ja itsevarma karibialainen yrittävät vuorollaan tehdä häneen vaikutuksen',
    'UUSI KAUSI. Kausi 4. Jakso 15/40. Rakkaudesta luontoon. Luonnonsuojelusta kiinnostuneen perheen rehottava etupiha on muodonmuutoksen tarpeessa.',
    'Kausi 2, 2/8 Arjen symbolit. Millaisia viestejä arkisten tuotemerkkien, äänien ja symbolien taakse kätkeytyy? Merkkien saloja jäljittävät toimittaja Ella Kanninen ja symbolitutkija Liisa Väisänen.',
    'Kausi 26. Jakso 18. Äiti kyylä. Bart val',
    'Osa 3229: Taalasmaa impotenssiin kaksi.',
    'Kausi 9, 7/17. Poliisin hämmentävät sala',
    'Kausi 8. Osa 4.'
    ]

for desc1 in descs:

    descobj1=descparser.Desc(desc1)

    #for i in range(1,10):
    #    if descobj1.hasJakso() and not descobj1.isLastJakso():
    #        descobj1.addJakso()    
    #    print(descobj1.str())
    #    print(hash(descobj1))
    print(desc1)
    print(descparser.deschash(desc1))

