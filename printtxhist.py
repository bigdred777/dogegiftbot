
from dogegiftbottables import *
session = create_session()
txs = session.query(Transactions).order_by(Transactions.tx_type)
session.close()
for tx in txs:
    print "type: %s donor: %s amount: %f date: %s " % \
    (tx.tx_type, tx.donor,tx.amount, tx.date)

    
    