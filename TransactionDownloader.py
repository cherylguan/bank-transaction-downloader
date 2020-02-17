import http.client
import uuid
import json
import base64

clientId = "REPLACE_THIS_VALUE"
password = "REPLACE_THIS_VALUE"
transFromDate = "REPLACE_THIS_VALUE"
transToDate = "REPLACE_THIS_VALUE"
outputFileName = "output.csv"

conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

payload = "grant_type=client_credentials&scope=/dda/customer, /dda/accountlist, /dda/account, /dda/accountsdetails, /dda/account/transactions"

headers = {
    'authorization': base64.b64encode(clientId + ":" + password),
    'content-type': "application/x-www-form-urlencoded",
    'accept': "application/json"
    }

conn.request("POST", "/gcb/api/clientCredentials/oauth2/token/us/gcb", payload, headers)

res = conn.getresponse()
data = res.read()
authToken = data.decode("utf-8")

conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

headers = {
    'authorization': authToken,
    'uuid': uuid.uuid1(),
    'client_id': clientId,
    'accept': "application/json"
    }

conn.request("GET", "/gcb/api/v2/accounts/details", headers=headers)

res = conn.getresponse()
data = res.read()

accountId = data.accountGroupDetails[0].accountId

conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

headers = {
    'authorization': authToken,
    'uuid': uuid.uuid1(),
    'client_id': clientId,
    'accept': "application/json"
    }

conn.request("GET", f'/gcb/api/v2/accounts/{accountId}/transactions?transactionFromDate={transFromDate}&transactionToDate={transToDate}', headers=headers)

res = conn.getresponse()
data = res.read()

outputFile = open(outputFileName, 'w')
output = csv.writer(outputFile)

for row in data.checkingAccountTransactions:
        output.writerow(row.values())