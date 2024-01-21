from bcrypt import gensalt,hashpw,checkpw

def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(entered_password, hashed_password):
    return checkpw(entered_password.encode('utf-8'), hashed_password)

