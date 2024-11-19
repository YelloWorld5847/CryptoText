import numpy as np
from text_utils import load_corpus, transform_to_caps, char_to_id, count_correct_words, \
    score_correct_words, frequency_order, apply_code
import pickle


# Fonction pour calculer la vraisemblance d'un texte
def likelihood(s, logp):
    res = 0
    c1 = s[0]
    for c2 in s[1:]:
        i = char_to_id(c1)
        j = char_to_id(c2)
        res += logp[i, j]
        c1 = c2
    return res / len(s)


# Fonction pour permuter deux indices dans un code
def permute_code(code, i, j):
    newcode = code.copy()
    newcode[j] = code[i]
    newcode[i] = code[j]
    return newcode


# Fonction principale pour déchiffrer un message
def decrypt_message(corpus_filename, bigrams_filename, text_to_decrypt, MIN_ITER=2000, MAX_ITER=100000, THRESHOLD=-2.05,
                    ALPHA=1, GAMMA=4.0, NITER2=2000, temperature=0.05, rho=0.999):
    # Charger les bigrammes et la matrice de probabilité
    bigrams = np.fromfile(bigrams_filename, dtype="int32").reshape(27, 27)
    p = bigrams.astype('float') / np.tile(sum(bigrams.T), (27, 1)).T
    p[np.isnan(p)] = 0
    EPSILON = 1e-6
    logp = np.log(p + EPSILON)

    # Préparer le texte pour l'initialisation
    freq_text = transform_to_caps(load_corpus(corpus_filename))
    ciphered_text = transform_to_caps(text_to_decrypt)

    # Initialisation du code basé sur la fréquence
    ref_freq = frequency_order(freq_text)
    obs_freq = frequency_order(ciphered_text)
    freq_code = [0] + list(range(1, 27))

    for i in range(1, 27):
        pos = obs_freq.index(i)
        freq_code[i] = ref_freq[pos]

    # Initialisation du meilleur code trouvé
    cur_code = freq_code.copy()
    cur_trad = apply_code(ciphered_text, cur_code)
    cur_like = likelihood(cur_trad, logp)

    best_code = cur_code.copy()
    best_like = cur_like
    best_trad = cur_trad

    print(best_trad + "    N=" + str(0) + " L={0:.2f}".format(best_like))

    # Boucle principale pour l'optimisation
    for k in range(MAX_ITER):
        i = np.random.randint(1, 27)
        j = np.random.randint(1, 27)
        tt_code = permute_code(cur_code, i, j)
        tt_trad = apply_code(ciphered_text, tt_code)
        tt_like = likelihood(tt_trad, logp)

        x = np.random.rand()
        p = np.exp(ALPHA * (tt_like - cur_like) * len(ciphered_text))

        if x < p:
            cur_code = tt_code.copy()
            cur_trad = tt_trad
            cur_like = tt_like

            if cur_like > best_like:
                best_code = cur_code.copy()
                best_like = cur_like
                best_trad = cur_trad
                print(best_trad + "    [k=" + str(k) + " L={0:.2f}]".format(best_like))

        if k > MIN_ITER and best_like > THRESHOLD:
            break

    # Phase 2 : Amélioration du score avec les mots corrects
    with open('dictionnary.data', 'rb') as filehandle:
        dictionnary_words = pickle.load(filehandle)

    cnt, total = count_correct_words(best_trad, dictionnary_words)
    word_score = score_correct_words(best_trad, dictionnary_words)

    print("Mots OK " + str(cnt) + "/" + str(total) + " score=" + str(word_score))

    best_score = GAMMA * word_score + best_like
    cur_code = best_code
    cur_score = best_score
    cur_trad = best_trad

    # Seconde phase : optimisation plus fine
    for k in range(NITER2):
        i = np.random.randint(1, 27)
        j = np.random.randint(1, 27)
        tt_code = permute_code(cur_code, i, j)
        tt_trad = apply_code(ciphered_text, tt_code)
        tt_word_score = score_correct_words(tt_trad, dictionnary_words)
        tt_like = likelihood(tt_trad, logp)
        tt_score = GAMMA * tt_word_score + tt_like

        x = np.random.rand()
        p = np.exp((tt_score - cur_score) / temperature)
        temperature = temperature * rho

        if x < p:
            cur_code = tt_code.copy()
            cur_trad = tt_trad
            cur_score = tt_score

            if cur_score > best_score:
                best_code = cur_code
                best_score = cur_score
                best_trad = cur_trad
                print(tt_trad + "  W={0:.2f}".format(tt_word_score))

    # Retourner le message déchiffré
    return best_trad

def crypt_message(otis):
    original = transform_to_caps(otis)
    np.random.seed(3)
    true_code = [0] + list(np.random.permutation(range(1, 27)))
    ciphered_text = apply_code(original, true_code)
    return ciphered_text

if __name__ == '__main__':

    # Exemple d'appel
    ciphered_text = (
        """
        VSBL AHTL LSAPK VHB WP GP MJHBL FSL UT BE Y SBZ XP RHGGP HT XP VSTASBLP LBZTSZBHG VHB LB WP XPASBL JPLTVPJ VS ABP STWHTJX CTB SAPM AHTL WP XBJSBL UTP M PLZ X SRHJX XPL JPGMHGZJPL XPL NPGL UTB V HGZ ZPGXT ES VSBG
        """
    )
    decrypted_message = decrypt_message("swann.txt", "bigrams.dat", ciphered_text)
    print("\n")
    print(decrypted_message)
