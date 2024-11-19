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

from flask import Flask, render_template, request
from dechiffre_MCMC import decrypt_message, crypt_message

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
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        encrypted_text = request.form['encrypted_text']  # Récupère la phrase cryptée
        print(f"texte chiffré : {encrypted_text}")

        # Assure-toi que decrypt_message fonctionne et renvoie le texte décrypté
        decrypted_text = decrypt_message("swann.txt", "bigrams.dat", encrypted_text)

        return render_template('decrypt.html', decrypted_text=decrypted_text)

    return render_template('decrypt.html')


if __name__ == '__main__':
    app.run(debug=True)