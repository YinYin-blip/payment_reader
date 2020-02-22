import PyPDF2
import hashlib

def getCustomerName(page_content):
    title = page_content[20]
    initials = page_content[21]
    lastName = page_content[22][:page_content[22].rfind('O')]
    name = title, initials, lastName
    return name

def getRecipientName(page_content):
    recipient = page_content[37], page_content[38], page_content[39]
    return recipient

def getPaymentDate(page_content):
    dateText = page_content[44]
    date = dateText[9:-8]
    return date

def getReference(page_content):
    referenceText = page_content[53]
    referenceNumber = referenceText[15:][:-4]
    return referenceNumber

def getAmount(page_content):
    amountText = page_content[57]
    amount = amountText[4:amountText.rfind("O")]
    return amount

def getPaymentType(page_content):
    isInstantDeposit = False
    instantDepositText = page_content[59]
    if instantDepositText[instantDepositText.find(":"):instantDepositText.rfind("V")] == "Y":
        isInstantDeposit = True
    return isInstantDeposit

def getNotificationDetails(page_content):
    customerName = getCustomerName(page_content)
    recipientName = getRecipientName(page_content)
    referenceNumber = getReference(page_content)
    paymentDate = getPaymentDate(page_content)
    paymentAmount = getAmount(page_content)
    isInstantDeposit = getPaymentType(page_content)
    return [customerName, paymentDate, paymentAmount, referenceNumber, recipientName, isInstantDeposit]
