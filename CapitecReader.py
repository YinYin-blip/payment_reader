import PyPDF2
import hashlib

CAPITEC_FIRST_NAME_POSITION = 84
CAPITEC_NEGATIVE_REF_FROM_FIRST_NAME_OFFSET = 114
CAPITEC_DATE_FROM_FIRST_NAME_OFFSET = 13
CAPITEC_NEGATIVE_AMOUNT_FROM_FIRST_NAME_OFFSET = 115

def getReference(page_content, nameOffset, bankName = "Capitec"):
    referencePosition = len(page_content) - CAPITEC_NEGATIVE_REF_FROM_FIRST_NAME_OFFSET
    referenceText = page_content[referencePosition]
    return referenceText[9:-9]

def getCustomerName(page_content, bankName = "Capitec"):
    offset = 0
    for word in page_content[84:]:
        if word == "made":
            break
        else:
            offset += 1

    name = page_content[84:84+offset]

    return (name, offset)

def getPaymentDate(page_content, nameOffset, bankName = "Capitec"):

    dayPosition = CAPITEC_FIRST_NAME_POSITION + nameOffset + CAPITEC_DATE_FROM_FIRST_NAME_OFFSET
    day = page_content[dayPosition][4:]
    timePosition = dayPosition+1
    time = page_content[timePosition][:-7]
    return [day, time]

def getAmount(page_content, nameOffset, bankName = "Capitec"):
    amountPosition = len(page_content) - CAPITEC_NEGATIVE_AMOUNT_FROM_FIRST_NAME_OFFSET
    amount = page_content[amountPosition][:-4]
    return amount

def getNotificationDetails(page_content, bankName = 'Captitec'):
    nameTuple = getCustomerName(page_content)
    customerName = nameTuple[0]
    nameOffset = nameTuple[1]
    reference = getReference(page_content, nameOffset)
    paymentDate = getPaymentDate(page_content, nameOffset)
    amount = getAmount(page_content, nameOffset)

    return [customerName, paymentDate, amount, reference]
