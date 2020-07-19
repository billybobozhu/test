from zoodb import *
from debug import *
import bank
import time

def transfer(sender, recipient, zoobars):
    #persondb = person_setup()
    #senderp = persondb.query(Person).get(sender)
    #recipientp = persondb.query(Person).get(recipient)
    if zoobars < 0:
        raise ValueError()

    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    print "recipientp.name %s\n"%recipient
    print "recipientp zoobars %s\n"%recipientp.zoobars
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    #db = person_setup()
    #person = db.query(Person).get(username)
    bankdb = bank_setup()
    person = bankdb.query(Bank).get(username)
    print "in balance: balance:%s\n"%person.zoobars
    return int(person.zoobars)

def getlog(username):
    db = transfer_setup()
    
    result =  db.query(Transfer).filter(or_(Transfer.sender==username,Transfer.recipient==username))
    #result = db.query(Transfer).get(Transfer.sender==username)
    #print "result %s" %result
    def format_transfer(transfer):
        return {
                'username':username,
                'user':username,
               'time':transfer.time,
               'sender':transfer.sender,
               'recipient':transfer.recipient,
               'amount':transfer.amount}
    return [format_transfer(transfer) for transfer in result]

def register(username):
    bankdb = bank_setup()
    bank = bankdb.query(Bank).get(username)
    if bank:
        return None
    newbank = Bank()
    newbank.username = username
    bankdb.add(newbank)
    bankdb.commit()
