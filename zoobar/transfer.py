from flask import g, render_template, request
import time
import bank_client
from login import requirelogin
from zoodb import *
from debug import *

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            zoobars = int(request.form['zoobars'])
            if g.user.person.username == request.form['recipient']:
                raise AttributeError()

            ret = bank_client.transfer(str(g.user.person.username), str(request.form['recipient']), zoobars)
            if ret == 0: 
                raise AttributeError()
#=======
#            recipient = g.persondb.query(Person).get(request.form['recipient'])
#            zoobars = eval(request.form['zoobars'])
#            sender_balance = g.user.person.zoobars - zoobars
#            recipient_balance = recipient.zoobars + zoobars
#
#            if sender_balance < 0 or recipient_balance < 0:
#                raise ValueError()
#
#            g.user.person.zoobars = sender_balance
#            recipient.zoobars = recipient_balance
#            transfer = Transfer()
#            transfer.sender = g.user.person.username
#            transfer.recipient = recipient.username
#            transfer.amount = zoobars
#            transfer.time = time.asctime()
#            g.transferdb.add(transfer)
#>>>>>>> lab1
            warning = "Sent %d zoobar s" % zoobars
    except (KeyError, ValueError, AttributeError) as e:
        log("Transfer exception: %s" % str(e))
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
