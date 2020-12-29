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
        self.calculer_lettres()

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

    def calculer_lettres(self):
        if self.enfant_gauche() is not None:
            self.lettre += self.enfant_gauche().donnee()
        if self.enfant_droit() is not None:
            self.lettre += self.enfant_droit().donnee()

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
    return lettre, poids


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
        l, p = item_minimal_dans_dict(dict_de_lettres)

        arbre = Arbre(None, None, l, dict_de_lettres[l])

        dict_de_lettres.pop(l)

        t = [arbre] + creation_tableau_arbres(dict_de_lettres)
        dict_de_lettres[l] = p
        return t
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
    if arbre is not None:
        # WIP
        chemin = ''
        if arbre.enfant_gauche() is not None and l in arbre.enfant_gauche().donnee():
            chemin_suivant = chemin_lettre(l, arbre.enfant_gauche())
            chemin += '0'
            if chemin_suivant is not None:
                chemin += chemin_suivant
        elif arbre.enfant_droit() is not None and l in arbre.enfant_droit().donnee():
            chemin_suivant = chemin_lettre(l, arbre.enfant_droit())
            chemin += '1'
            if chemin_suivant is not None:
                chemin += chemin_suivant

        return chemin


def encode_text(texte, codes):
    texte_encode = ''
    for lettre in texte:
        texte_encode += codes[lettre]
    return texte_encode


def decode_text(texte_encode, codes):
    texte_decode = ''
    code = ''
    for n in texte_encode:
        code += n
        if code in codes.values():
            texte_decode += list(codes.keys())[list(codes.values()).index(code)]
            code = ''
    return texte_decode


def affiche_gain(texte_decode, texte_encode):
    print("Gain:")
    print("Sans encoder:", len(texte_decode), '* 7 (les codes ASCII utilisent 7 bits par caractère)', '=', len(texte_decode)*7, 'bits')
    print("En encodant:", len(texte_encode), '=', len(texte_encode), 'bits')
    print("Soit un gain de", len(texte_decode)*7-len(texte_encode), 'bits')


def main():
    texte = 'a'*240 + 'b'*140 + 'c'*160 + 'd'*51 + 'e'*280 + 'f'*49 + 'G'*45 + 'h'*35
    texte = 'Hello world'
    texte = "En politique, mon cher, vous le savez comme moi, il n'y a pas d'hommes, mais des idées ; pas de sentiments, mais des intérêts ; en politique, on ne tue pas un homme : on supprime un obstacle, voilà tout. - Apprendre n'est pas savoir ; il y a les sachant et les savants : c'est la mémoire qui fait les uns, c'est le philosophie qui fait les autres.\n- Mais ne peut-on apprendre la philosophie ?\n- La philosophie ne s'apprend pas ; la philosophie est la réunion des sciences acquises au génie qui les applique : la philosophie, c'est le nuage éclatant sur lequel le Christ a posé le pied pour remonter au ciel.Je sonnai pour qu'on m'apportât de la lumière, personne ne vint ; je résolus alors de me servir moi-même. C'était d'ailleurs une habitude de philosophe qu'il allait me falloir prendre.La haine est aveugle, la colère étourdie, et celui qui se verse la vengeance risque de boire un breuvage amer.Menez deux moutons à la boucherie, deux boeufs à l'abattoir, et faites comprendre à l'un d'eux que son compagnon ne mourra pas, le mouton bêlera de joie, le boeuf mugira de plaisir ; mais l'homme, l'homme que Dieu a fait à son image, l'homme à qui Dieu a imposé pour première, pour unique, pour suprême loi, l'amour de son prochain, l'homme à qui Dieu a donné une voix pour exprimer sa pensée, quel sera son premier cri quand il apprendra que son camarade est sauvé ? Un blasphème.Je n'ai que deux adversaires ; je ne dirai pas deux vainqueurs, car avec la persistance je les soumets : c'est la distance et le temps. Le troisième, et le plus terrible, c'est ma condition d'homme mortel. Celle-là seule peut m'arrêter dans le chemin où je marche, et avant que j'aie atteint le but auquel je tends : tout le reste, je l'ai calculé.Or, l'homme ne sera parfait que lorsqu'il saura créer et détruire comme Dieu ; il sait déjà détruire, c'est la moitié du chemin de fait.Supposez que le Maître suprême, après avoir créé le monde, après avoir fertilisé le chaos, se fût arrêté au tiers de la création pour épargner à un ange les larmes que nos crimes devaient faire couler un jour de ses yeux immortels ; supposez qu'après avoir tout préparé, tout pétri, tout fécondé, au moment d'admirer son oeuvre, Dieu ait éteint le soleil et repoussé du pied le monde dans la nuit éternelle, alors vous aurez une idée, ou plutôt non, non, vous ne pourrez pas encore vous faire une idée de ce que je perds en perdant la vie en ce moment."
    apc = apparition_par_charactere(texte)

    tab_arbres = creation_tableau_arbres(apc)

    tab_arbres.reverse()

    arbre = creation_arbre_huffman(tab_arbres)

    dict_de_codes = {}

    for key in apc.keys():
        dict_de_codes[key] = chemin_lettre(key, arbre)

    texte_encode = encode_text(texte, dict_de_codes)

    texte_decode = decode_text(texte_encode, dict_de_codes)
    print(texte_decode)

    affiche_gain(texte_decode, texte_encode)



if __name__ == '__main__':
    main()
