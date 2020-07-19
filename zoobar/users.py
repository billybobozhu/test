from flask import g, render_template, request, Markup

from login import requirelogin
from zoodb import *
from debug import *
import bank_client
@catch_err
@requirelogin
def users():
    args = {}
    args['req_user'] = Markup(request.args.get('user', ''))
    if 'user' in request.values:
        user = g.persondb.query(Person).get(request.values['user'])
        if user:
            args['profile'] = Markup("<b>%s</b>" % user.profile)
            args['user'] = user
#<<<<<<< HEAD
            print "hehe, setting\n"
            print bank_client.balance(user.username)
            args['zoobars'] = bank_client.balance(user.username)
            args['transfers'] = bank_client.getlog(user.username)
#=======
#            args['transfers'] = g.transferdb.query(Transfer).filter(
#                                    or_(Transfer.sender==user.username,
#                                        Transfer.recipient==user.username))
#>>>>>>> lab1
        else:
            print "what in here\n"
            args['warning'] = "Cannot find that user."
    return render_template('users.html', **args)
