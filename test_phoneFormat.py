import phoneFormat

nmbrsMob = [('0465 45 26 12', '+32 465 45 26 12'), ('0478 80 21 12', '+32 478 80 21 12'),
            ('0489 80 21 12', '+32 489 80 21 12'), ('475 80 21 12', '+32 475 80 21 12')]

nmbrsLong = [('089 16 95 45', '+32 89 16 95 45'), ('080 73 15 14', '+32 80 73 15 14'),
             ('010 58 44 65', '+32 10 58 44 65')]

nmbrsShort = [('02 784 55 96', '+32 2 784 55 96'), ('03 813 98 11', '+32 3 813 98 11'),
              ('04 588 91 98', '+32 4 588 91 98'), ('09 152 83 90', '+32 9 152 83 90')]

nmbrsLongLenght = ['089 716 95 45', '080 3 15 14']

nmbrsShortLenght = ['096 284 55 96', '03 13 98 11']

nmbrsFormatting = [('0465/45-26-12', '+32 465 45 26 12'), ('0032 478;80;21;12', '+32 478 80 21 12')]

nmbrsDangerous = ['070  165 745', '077  15724 247365', '078 861 734', '0800 21 796', '0907 32 654']


def test_nbrsMob():
    for i, nmbr in enumerate(nmbrsMob):
        assert phoneFormat.belgium(nmbr[0]) == nmbr[1]

def test_nmbrsLong():
    for i, nmbr in enumerate(nmbrsLong):
        assert phoneFormat.belgium(nmbr[0]) == nmbr[1]

def test_nmbrsShort():
    for i, nmbr in enumerate(nmbrsShort):
        assert phoneFormat.belgium(nmbr[0]) == nmbr[1]

def test_nmbrsLongLenght():
    for nmbr in nmbrsLongLenght:
        assert phoneFormat.belgium(nmbr) == 'error'

def test_nmbrsShortLenght():
    for nmbr in nmbrsShortLenght:
        assert phoneFormat.belgium(nmbr) == 'error'

def test_nmbrsFormatting():
    for i, nmbr in enumerate(nmbrsFormatting):
        assert phoneFormat.belgium(nmbr[0]) == nmbr[1]

def test_nmbrsDangerous():
    for nmbr in nmbrsDangerous:
        assert phoneFormat.belgium(nmbr) == 'error'




'''
Random numbers:
80 21 12
79 65 42
61 59 81
78 24 53
16 95 45
73 15 14
58 44 65
84 55 96
13 98 11
88 91 98
52 83 90
36 66 54
62 51 69
32 86 90
30 96 72
'''
