# from flask import Flask, render_template, request
# from dechiffre_MCMC import decrypt_message, crypt_message
# app = Flask(__name__)
#
# # Page d'accueil
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# # Page de cryptage
# @app.route('/encrypt', methods=['GET', 'POST'])
# def encrypt():
#     if request.method == 'POST':
#         plain_text = request.form['plain_text']  # Récupère la phrase entrée
#         encrypted_text = crypt_message(plain_text)
#         # encrypted_text = "CRYPTER_PLAINT_TEXT_ICI"  # Remplacer par le résultat
#         return render_template('encrypt.html', encrypted_text=encrypted_text)
#     return render_template('encrypt.html')
#
# # Page de décryptage
# @app.route('/decrypt', methods=['GET', 'POST'])
# def decrypt():
#     if request.method == 'POST':
#         encrypted_text = request.form['encrypted_text']  # Récupère la phrase cryptée
#         print(f"texte chiffré : {encrypted_text}")
#         decrypted_text = decrypt_message("swann.txt", "bigrams.dat", encrypted_text)
#         # decrypted_text = "DECRYPTER_ENCRYPTED_TEXT_ICI"  # Remplacer par le résultat
#         return render_template('decrypt.html', decrypted_text=decrypted_text)
#     return render_template('decrypt.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, Response
from dechiffre_MCMC import decrypt_message_progressive, crypt_message
import time  # Pour simuler des retards
app = Flask(__name__)


# Page d'accueil
@app.route('/')
def home():
    return render_template('index.html')


# Page de cryptage
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        plain_text = request.form['plain_text']  # Récupère la phrase entrée
        encrypted_text = crypt_message(plain_text)  # Applique ton cryptage
        return render_template('encrypt.html', encrypted_text=encrypted_text)
    return render_template('encrypt.html')


# Page de décryptage

# Simuler un générateur de décryptage progressif
def decrypt_message_stream(text_to_decrypt):
    for i in range(20):  # Exemple de 10 étapes progressives
        time.sleep(0.5)  # Simuler un traitement
        yield f"data: Étape {i + 1} : Résultat partiel pour '{text_to_decrypt}'\n\n"
    yield f"data: Décryptage terminé pour '{text_to_decrypt}'\n\n"

# Endpoint pour les événements SSE
# @app.route('/stream')
# def stream():
#     encrypted_text = request.args.get('text', 'Texte par défaut')
#     langue = request.args.get('langue', 'bigrams.dat')
#     print(f"langue :{langue}")
#     return Response(decrypt_message_progressive("swann.txt", langue, encrypted_text), content_type='text/event-stream')
#
@app.route('/stream')
def stream():
    encrypted_text = request.args.get('text', 'Texte par défaut')
    langue = request.args.get('langue', 'bigrams.dat')  # Récupère la langue passée dans l'URL
    print(langue)
    return Response(decrypt_message_progressive("swann.txt", langue, encrypted_text), content_type='text/event-stream')



# Page de décryptage
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        encrypted_text = request.form['encrypted_text']  # Récupère la phrase cryptée
        langue = request.form['langue']  # Récupère la langue choisi
        return render_template('decrypt.html', encrypted_text=encrypted_text, langue=langue)

    return render_template('decrypt.html')
# @app.route('/decrypt', methods=['GET', 'POST'])
# def decrypt():
#     if request.method == 'POST':
#         encrypted_text = request.form['encrypted_text']  # Récupère la phrase cryptée
#         print(f"texte chiffré : {encrypted_text}")
#
#         # # Assure-toi que decrypt_message fonctionne et renvoie le texte décrypté
#         # decrypted_text = decrypt_message_progressive("swann.txt", "bigrams.dat", encrypted_text)
#         #
#         # return render_template('decrypt.html', decrypted_text=decrypted_text)
#
#         def generate():
#             for update in decrypt_message_progressive("swann.txt", "bigrams.dat", encrypted_text):
#                 yield f"data:{update}\n\n"  # Protocole SSE (Server-Sent Events)
#
#         return Response(generate(), content_type='text/event-stream')
#
#     return render_template('decrypt.html')



if __name__ == '__main__':
    app.run(debug=True)