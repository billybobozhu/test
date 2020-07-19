#!/usr/bin/env python

from flask import Flask, g

import login
import index
import users
import transfer
import echo
import zoobarjs
import zoodb
import auth
from debug import catch_err

app = Flask(__name__)

app.add_url_rule("/", "index", index.index, methods=['GET', 'POST'])
app.add_url_rule("/users", "users", users.users)
app.add_url_rule("/transfer", "transfer", transfer.transfer, methods=['GET', 'POST'])
app.add_url_rule("/zoobarjs", "zoobarjs", zoobarjs.zoobarjs, methods=['GET'])
app.add_url_rule("/login", "login", login.login, methods=['GET', 'POST'])
app.add_url_rule("/logout", "logout", login.logout)
app.add_url_rule("/echo", "echo", echo.echo)
@app.before_request
@catch_err
def dbinit():
    g.persondb   = zoodb.person_setup()
    g.transferdb = zoodb.transfer_setup()
    #g.creddb = zoodb.cred_setup()
    #g.bankdb = zoodb.bank_setup()
@app.after_request
@catch_err
def dbcommit(response):
    g.persondb.commit()
    g.transferdb.commit()
    #g.creddb.commit()
    #g.bankdb.commit()
    return response

if __name__ == "__main__":
    app.run()