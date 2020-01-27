import json
import os

import hmac
import hashlib 

# ss = b'abc' # This is the secret that was entered for webhook in Glo
# dd = b"{\"action\":\"updated\",\"board\":{\"id\":\"5e1b2b8a553d4500116e117d\",\"name\":\"ToDos\"},\"card\":{\"id\":\"5e2da7369a4c6500104a9f8c\",\"name\":\"TEST CARD\",\"created_date\":\"2020-01-26T14:50:30.521Z\",\"board_id\":\"5e1b2b8a553d4500116e117d\",\"column_id\":\"5e1b2be20af39d00106c436b\",\"due_date\":\"2020-01-27T05:00:00.000Z\",\"description\":{\"text\":\"this is a test post\\nadded a secret\\nKept the secrest , let's see\\nremoved some descs.\"},\"labels\":[{\"name\":\"recuring task - monthly\",\"id\":\"5e1b3155553d4500116e11da\"}],\"assignees\":[],\"completed_task_count\":0,\"total_task_count\":0,\"attachment_count\":0,\"comment_count\":1,\"created_by\":{\"id\":\"65f0a2cf-194f-42a3-b280-16193a7e5bad\"},\"previous\":{\"id\":\"5e2da7369a4c6500104a9f8c\",\"name\":\"TEST CARD\",\"due_date\":\"2020-01-27T05:00:00.000Z\",\"description\":{\"text\":\"this is a test post\\nadded a secret\\nKept the secrest , let's see\\nremoved some descs.\\nanother one\"},\"assignees\":[]}},\"sender\":{\"name\":\"Madushan D. Memmendarachchi\",\"id\":\"65f0a2cf-194f-42a3-b280-16193a7e5bad\",\"username\":\"damiththa\"},\"sequence\":8}"

# signature = hmac.new(ss, dd, hashlib.sha1).hexdigest()
# print("signature = {0}".format(signature))

# Getting webhook secrect and encoding to bytes
GLO_WEBHOOK_SECRET = bytes(os.environ['GLO_WEBHOOK_SECRET'], encoding='utf8')

def verifySignature(eBody, gloSignature):
    signature_check_pass = False # default values

    # getting the raw body by 'stringifying' it and encoding to bytes
    eBody_stringify = bytes(json.dumps(eBody), encoding='utf8')

    rtn_signature = createSignature(eBody_stringify)
    # print (rtn_signature)
    # print (gloSignature)

    if rtn_signature == gloSignature: # checking whether signatures match
        signature_check_pass = True
    
    return 'signature_check_pass'
    
def createSignature(raw_eventBody):
    signature  = hmac.new(GLO_WEBHOOK_SECRET, raw_eventBody, hashlib.sha1).hexdigest()
    return signature
