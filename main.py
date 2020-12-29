def apparition_par_charactere(texte):
    """
    :param string:
    :return: dictionnaire d'apparition de chaque lettre dans le texte
    """
    _apc = {}
    for lettre in texte:
        if lettre in _apc:
            _apc[lettre] += 1
        else:
            _apc[lettre] = 1
    return _apc


class Arbre:

    def __init__(self, g, d,  l='', p=-1):
        self.gauche = g
        self.lettre = l
        self.droit = d
        self.poids = p
        if p == -1:
            self.calculer_poids()

    def enfant_gauche(self):
        return self.gauche

    def enfant_droit(self):
        return self.droit

    def calculer_poids(self):
        self.poids = 0
        if self.gauche is not None:
            self.poids += self.gauche.poids

        if self.droit is not None:
            self.poids += self.droit.poids

    def donne_poids(self):
        return self.poids

    def donnee(self):
        return self.lettre

    def __str__(self):
        if self is None:
            return 'None'
        return '(' + str(self.gauche) + ',' + self.lettre + ',' + str(self.poids) + ',' + str(self.droit) + ')'


def parcours_infixe(_a):
    if _a is not None:
        parcours_infixe(_a.enfant_gauche())
        print(_a.lettre(),  _a.donne_poids())
        parcours_infixe(_a.enfant_droit())


def item_minimal_dans_dict(dict_de_lettres):
    lettre = ''
    poids = 0
    for _lettre, apparition in dict_de_lettres.items():
        if apparition > poids:
            poids = apparition
            lettre = _lettre
    return lettre


def item_maximal_dans_dict(dict_de_lettres):
    lettre = ''
    poids = 0
    for _lettre, apparition in dict_de_lettres.items():
        if apparition < poids:
            poids = apparition
            lettre = _lettre
    return lettre


def supprime_et_retourne_minimal_tab_arbre(tab_arbre):
    if len(tab_arbre) == 0:
        return None

    arbre = tab_arbre.pop()
    index_arbre = len(tab_arbre)
    tab_arbre.append(arbre)
    for i in range(len(tab_arbre)):
        a = tab_arbre[i]
        if a.donne_poids() < arbre.donne_poids():
            arbre = a
            index_arbre = i
    tab_arbre.pop(index_arbre)
    return arbre, tab_arbre


def creation_tableau_arbres(dict_de_lettres):
    if len(dict_de_lettres) > 0:
        l = item_minimal_dans_dict(dict_de_lettres)

        arbre = Arbre(None, None, l, dict_de_lettres[l])

        dict_de_lettres.pop(l)

        return [arbre] + creation_tableau_arbres(dict_de_lettres)
    else:
        return []


def creation_arbre_huffman(tab_arbre):
    arbre = None

    # arbre initial
    smaller1 = tab_arbre.pop(0)
    smaller2 = tab_arbre.pop(0)
    arbre = Arbre(smaller2, smaller1)
    tab_arbre.append(arbre)

    while len(tab_arbre) > 2:
        arbre1, tab_arbre = supprime_et_retourne_minimal_tab_arbre(tab_arbre)
        arbre2, tab_arbre = supprime_et_retourne_minimal_tab_arbre(tab_arbre)
        _arbre = Arbre(arbre2, arbre1)
        tab_arbre.append(_arbre)

    fd, tab_arbre = supprime_et_retourne_minimal_tab_arbre(tab_arbre)
    fg, tab_arbre = supprime_et_retourne_minimal_tab_arbre(tab_arbre)
    return Arbre(fg, fd)


def chemin_lettre(l, arbre):
    if arbre is None:
        return -1
    # WIP


def main():
    texte = 'a'*240 + 'b'*140 + 'c'*160 + 'd'*51 + 'e'*280 + 'f'*49 + 'G'*45 + 'h'*35
    apc = apparition_par_charactere(texte)

    tab_arbres = creation_tableau_arbres(apc)

    tab_arbres.reverse()
    # for a in tab_arbres:
    #     print(a)

    arbre = creation_arbre_huffman(tab_arbres)
    print(arbre)


if __name__ == '__main__':
    main()

