import secrets
import string


def generate_family_code():

    alphabet = string.ascii_uppercase + string.digits
    for char in "0O1I":
        alphabet = alphabet.replace(char, "")
    family_code = ""
    for _ in range(8):
        family_code += secrets.choice(alphabet)
    return family_code

