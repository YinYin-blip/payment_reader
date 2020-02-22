import PyPDF2
import hashlib

STANDARD_FIRST_NAME_POSITION = 128
OFFSET = 0

def getCustomerName(page_content):
    global OFFSET
    customerName = page_content[STANDARD_FIRST_NAME_POSITION]
    for word in page_content[STANDARD_FIRST_NAME_POSITION+1:]:
        if word == "Reference":
            break
        else:
            OFFSET += 1
            customerName = customerName + " " + word
    return customerName

def getRecipientName(page_content):
    global OFFSET

    recipientNamePosition = STANDARD_FIRST_NAME_POSITION+OFFSET+5
    recipientName = page_content[recipientNamePosition]

    for word in page_content[recipientNamePosition+1:]:
        if word != "Bank":
            OFFSET += 1
            recipientName = recipientName + " " + word
        else:
            break
    return recipientName

def getRecipientBankName(page_content):
    global OFFSET
    OFFSET += 1
    recipientBankNamePosition = STANDARD_FIRST_NAME_POSITION+OFFSET+7
    recipientBankName = page_content[recipientBankNamePosition]

    for word in page_content[recipientBankNamePosition+1:]:
        if word != "Bene®ciary":
            OFFSET += 1
            recipientBankName = recipientBankName + " " + word
        else:
            break
    return recipientBankName

def getRecipientAccountNumber(page_content):
    global OFFSET

    accountNumberPosition = STANDARD_FIRST_NAME_POSITION + OFFSET + 11
    accountNumber = page_content[accountNumberPosition]
    return accountNumber

def getRecipientBranchNumber(page_content):
    global OFFSET

    branchNumberPosition = STANDARD_FIRST_NAME_POSITION + OFFSET + 15
    branchNumber = page_content[branchNumberPosition]
    return branchNumber

def getReference(page_content):
    global OFFSET

    referencePosition = STANDARD_FIRST_NAME_POSITION + OFFSET + 18
    referenceNumber = page_content[referencePosition]
    return referenceNumber

def getAmount(page_content):
    global OFFSET

    amountPosition = STANDARD_FIRST_NAME_POSITION + OFFSET + 20
    amountText = page_content[amountPosition]
    return amountText

def getPaymentDate(page_content):
    global OFFSET

    datePosition = STANDARD_FIRST_NAME_POSITION + OFFSET + 25
    day = page_content[datePosition]
    time = page_content[datePosition + 1]
    return [day, time]

def getNotificationDetails(page_content):
    OFFSET = 1
    customerName = getCustomerName(page_content)
    recipientName = getRecipientName(page_content)
    recipientBankName = getRecipientBankName(page_content)
    recipientAccountNumber = getRecipientAccountNumber(page_content)
    recipientBranchNumber = getRecipientBranchNumber(page_content)
    referenceNumber = getReference(page_content)
    paymentAmount = getAmount(page_content)
    paymentDate = getPaymentDate(page_content)
    return [customerName, recipientName, recipientBankName, recipientAccountNumber, recipientBranchNumber, referenceNumber, paymentAmount, paymentDate]
