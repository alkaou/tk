import string

from .json_manager import JsonManager

tokenizer_path = "Tokenizer.json"
start_word = 1
end_word = 2
start_phrase = 3
end_phrase = 4

ponctuations = string.punctuation
space = "ದೄ"
punctuation = "ಐ"
sym_ponctuations = [f"{punctuation}{punct}{punctuation}" for punct in ponctuations]


class Tokenizer:

    @staticmethod
    def split_words(word):

        # Remplacer les espaces par l'icon de l'espace :"ದೄ"
        word = word.replace(" ", f" {space}")
        
        for idx, punct in enumerate(ponctuations):
            # Mettre les ponctuations au milieu l'icon de ponctuation "ಐ". Ex: "ಐ.ಐ", "ಐ!ಐ", "ಐ?ಐ"
            word = word.replace(punct, f" {sym_ponctuations[idx]} ")

        # Spliter la phrase pour qu'elle devienne un tableau. EX: ["Hello", "ದೄyou", "ಐ!ಐ"]
        result = word.split()
        return result # Resultat
    
    @staticmethod
    def tokenize(letter_or_word, tokens=[], add_special_tokens=False):
        my_tokenizer = JsonManager.load_json_file(tokenizer_path)
        vocab = my_tokenizer['vocab']

        # Récupérer le dernier token utilisé
        last_token = max(vocab.values())
        for letter in letter_or_word:
            if letter in vocab:
                # Si le mot ou la lettre existe dans le token. Pas besoin de nouvel enregistrement.
                token = vocab[letter]
                tokens.append(token)
                # print(token)
            else:
                # Si le mot n'existe pas, ajoutez-le avec un nouveau token
                if last_token in [31, 63, 123, 255, 513, 1023, 2047, 4095]:
                    last_token += 2
                else:
                    last_token += 1
                vocab[letter] = last_token
                tokens.append(last_token)
                my_tokenizer['vocab'] = vocab

        # Enregistrer les données dans le fichier JSON
        JsonManager.write_json(tokenizer_path, my_tokenizer)

        if add_special_tokens == True:
            tokens = [start_phrase] + tokens + [end_phrase]

        return tokens
    
    @staticmethod
    def encode(word_or_phrase, add_end_and_start_word=False, add_end_and_start_phrase=False):
        # Obtenir la phrase bien Spliter avec la methode: split_words
        letters_splited = Tokenizer.split_words(word_or_phrase)

        # print(letters_splited)
        # print(num_word_split)
        tokens = []

        tokens = Tokenizer.tokenize(letters_splited, tokens, add_end_and_start_phrase)

        if add_end_and_start_word == True and add_end_and_start_phrase == False:
            tokens = [start_word] + tokens + [end_word]
        return tokens
    
    @staticmethod
    def get_value(data, key):
        # print(data.get(key, None))
        return data.get(key, None)

    @staticmethod
    def decode(tokens):
        my_tokenizer = JsonManager.load_json_file(tokenizer_path)
        # Inverser le dictionnaire 'vocab'
        inverse_vocab = {v: k for k, v in my_tokenizer['vocab'].items()}

        text = ""
        for token in tokens:
            # Obtenir le mot avec la clé : key : token
            letter_or_word = Tokenizer.get_value(inverse_vocab, token)

            if letter_or_word is not None:
                # Remplace maintenant les icons: "ದೄ" par " " et "ಐ" par ""
                letter_or_word = letter_or_word.replace(space, " ").replace(punctuation, "")
                # print(letter_or_word)
                text += letter_or_word
        
        return text
    
# print(Tokenizer.encode("Hi all brothers. How are you ?"))
# print(Tokenizer.decode([8, 9, 10, 11, 12, 13, 14, 15, 16]))