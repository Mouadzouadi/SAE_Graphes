from requetes import *



def test_collaborateurs_communs():
    data = txt_json("data/data_2.txt")
    G = json_vers_nx("data/data.json") 
    assert collaborateurs_communs("Harrison Ford","Sean Young") == {"Rutger Hauer",
            "Edward James Olmos",
            "M. Emmet Walsh",
            "Daryl Hannah",
            "William Sanderson",
            "Brion James",
            "Joe Turkel",
            "Joanna Cassidy",
            "James Hong",
            "Morgan Paull",
            "Hy Pyke",
            "Ridley Scott",
            "Michael Deeley",
            "The Ladd Company",
            "Shaw Brothers",
            "Blade Runner Partnership",
            "Warner Bros."}


def test_est_proche():


    G2 = json_vers_nx("data/data.json")
    assert est_proche(G2, "John Cazale", "Harrison Ford", k=1) == True
    
    assert est_proche(G2, "John Cazale", "Harrison Ford", k=2) == True
    

    assert est_proche(G2, "Anna Lizaran", "Harrison Ford", k=1) == False

def test_distance():
    txt_json("data/data_2.txt")
    G2 = json_vers_nx("data/data.json")
    assert distance(G2,"Harrison Ford","Sean Young") == 1
    assert distance_naive(G2,"Harrison Ford","Sean Young") == 1
    assert distance_pre_calcul(pre_calcul(G2),"Harrison Ford","Sean Young") == 1


def test_centralite():

    data2 = txt_json("data/data_2.txt")
    G2 = json_vers_nx("data/data.json")
    assert centralite(G2, "Bruce Campbell") == 1
    assert centralite_pre_calcul(G2, "Bruce Campbell") == 1
    assert centralite(G2, "Al Pacino") == None
    """

def test_centre_holywood():

    data2 = txt_json("data/data_100.txt")
    G2 = json_vers_nx("data/data.json")
    assert centre_holywood(G2) == "Al Pacino"

def test_eloignement_max():

    data2 = txt_json("data/data_100.txt")
    G2 = json_vers_nx("data/data.json")
    assert eloignement_max(G2) == 3

def test_centralite_groupe():   
    data2 = txt_json("data/data_100.txt")
    G2 = json_vers_nx("data/data.json")
    assert centralite_groupe(G2, {"Al Pacino", "Michael J. Pollard","Charles Durning","Dick Van Dyke","Frank Campanella",}) == "Al Pacino" or "Charles Durning"


    """



