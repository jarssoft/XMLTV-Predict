import descparser

descs=[
    'Kausi 1. Jakso 21/26. Bing on kolmevuotias pikkuinen pupu, joka ystäviensä avustamana oppii joka päivä jotain uutta ja selviytyy taaperoille tutuista elämän haasteista. Lastenohjelma. (7\') Ohjelman tekstitys teksti-tv:n sivulla 333.',
    'Böjligare rygg och rörligare axlar i Gympastunden på tisdagarna.',
    'Kausi 4. Jakso 17/40. Kleingarten. Nicole on viettänyt lapsuutensa Saksassa ja haluaa pihaansa siirtolapuutarhapalstan eli kleingartenin. Puutarhaan tulee erilaisia kukkia ja vihannespenkki, mutta pihan keskipisteenä on',
    'Kausi 9. Jakso 3/29. Eri maailmoista. Entinen Miss Wales Imogen Thomas etsii herrasmiestä, joka osaa hemmotella naistaan. Adrenaliiniaddikti, rocktähti ja itsevarma karibialainen yrittävät vuorollaan tehdä häneen vaikutuksen'
    ]

for desc1 in descs:

    descobj1=descparser.Desc(desc1)

    for i in range(1,10):
        if descobj1.hasJakso() and not descobj1.isLastJakso():
            descobj1.addJakso()    
        print(descobj1.str())

