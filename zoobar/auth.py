from zoodb import *
from debug import *

import hashlib
import random
import pbkdf2
import bank_client
def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == pbkdf2.PBKDF2(password, cred.salt).hexread(32) :
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    creddb = cred_setup()
    persondb = person_setup()
    #bankdb = bank_setup()
    person = persondb.query(Person).get(username)
    if person:
        return None
    newcred = Cred()
    newcred.username = username
    newcred.salt     = os.urandom(8).encode('base_64')
    newcred.password = pbkdf2.PBKDF2(password, newcred.salt).hexread(32)
    creddb.add(newcred)
    creddb.commit()

    newperson = Person()
    newperson.username = username
    persondb.add(newperson)
    persondb.commit()
    
    #newbank = Bank()
    #newbank.username = username
    #bankdb.add(newbank)
    #bankdb.commit()
    bank_client.register(username)
    return newtoken(creddb, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

def is_registered(username):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if (cred):
        return True
    else:
        return False
