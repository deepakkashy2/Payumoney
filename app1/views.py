from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template,render_to_string
from django.template import Context, Template, RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
#from django.core.context_processors import csrf
from django.template.context_processors import csrf


def Home(request):
    MERCHANT_KEY = "un10fQ"
    key = "rjQUPktU"
    SALT = "e5iIg1jwi8"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted = {}
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i] = request.POST[i]
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid'] = txnid
    #posted['productinfo'] = "laptop"
    #posted['firstname'] = "deepak"
    #posted['email'] = "email@gmail.com"
    posted['txnid'] = txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    print("--->",hash_string)
    # hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    print("--->2", hashh)
    action = PAYU_BASE_URL
    t=get_template('current_datetime.html')
    if (posted.get("key")   != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
            "firstname") != None and posted.get("email") != None):

        pargs = {"posted": posted, "hashh": hashh,
                                      "MERCHANT_KEY": MERCHANT_KEY,
                                       "txnid": txnid,
                                        "hash_string": hash_string,
                                        "action": "https://test.payu.in/_payment"}
        html = render_to_string(
            'current_datetime.html', context=pargs, request=request)
        return HttpResponse(html)


        # return render_to_response('current_datetime.html', requestcontext(request, {"posted": posted, "hashh": hashh,
        #                                                                             "merchant_key": merchant_key,
        #                                                                              "txnid": txnid,
        #                                                                             "hash_string": hash_string,
        #                                                                             "action": "https://test.payu.in/_payment"}))
    else:
        pargs = {"posted": posted, "hashh": hashh,
                                  "MERCHANT_KEY": MERCHANT_KEY,
                                  "txnid": txnid,
                                  "hash_string": hash_string,
                                  "action": "."}
        html1 = render_to_string(
            'current_datetime.html', context=pargs, request=request)
        return HttpResponse(html1 )
        # return render_to_response('current_datetime.html', RequestContext(request, {"posted": posted, "hashh": hashh,
        #                                                                             "MERCHANT_KEY": MERCHANT_KEY,
        #                                                                             "txnid": txnid,
        #                                                                             "hash_string": hash_string,
        #                                                                             "action": "."}))


@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "GQs7yium"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
     #t = get_template('sucess.html')
    pargs = {"txnid": txnid, "status": status, "amount": amount}
    if (hashh != posted_hash):
        print
        "Invalid Transaction. Please try again"
    else:
        print
        "Thank You. Your order status is ", status
        print
        "Your Transaction ID for this transaction is ", txnid
        print
        "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."
    html = render_to_string(
            'sucess.html', context=pargs, request=request)
    return HttpResponse(html)
    # return render_to_response('sucess.html',
    #                           RequestContext(request, {"txnid": txnid, "status": status, "amount": amount}))


@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = ""
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
     #t = get_template('Failure.htmls')
    #html = t.render(c)
    if (hashh != posted_hash):
        print
        "Invalid Transaction. Please try again"
    else:
        print
        "Thank You. Your order status is ", status
        print
        "Your Transaction ID for this transaction is ", txnid
        print
        "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."
    html = render_to_string('Failure.html', context=c, request=request)
    return HttpResponse(html)
    # return render_to_response("Failure.html", RequestContext(request, c)



