import PyPDF2
import os
import hashlib

from AbsaReader import getNotificationDetails as getAbsaNotificationDetails
from CapitecReader import getNotificationDetails as getCapitecNotificationDetails
from StandardBankReader import getNotificationDetails as getStandardNotificationDetails


#this should be moved to the readers if more than one statement per bank is added. Leaving here for now
checkBankNotifications = [
(5,19),
(0,20),
(0,113)
]

knownBankNotifications = {
'e695c81d5e98aa1a2dd65d67dde515365e6619d537573bff40732ecc5b48dde0': "ABSA Payment Notification - Afrikaans",
'1df1031aefb1629e71e98fd8cee26e6a8c126493a855d023ff62f33203dac4a6': "Capitec Payment Notification",
'68ce464aa652c8e0062ae61c796329ac15215a168ba0c98516acaf0b08043fac': "Standard Bank Payment Notification"
}
#end



class ProofOfPayment:
    def __init__(self, fileName):
        isPDF = False
        if (fileName[-4:]==".pdf"):
            isPDF = True
        assert(isPDF)

        self.__fileName = fileName
        self.__content = []
        self.__signature = ''
        self.__bank = ''

        self.__hasCustomerName = False
        self.__hasPaymentAmount = False
        self.__hasPaymentDate = False
        self.__hasPaymentReference = False
        self.__hasPaymentType = False
        self.__hasRecipientName = False
        self.__hasRecipientBranchNumber = False
        self.__hasRecipientAccountNumber = False
        self.__hasRecipientBankName = False

        self.__customerName = ''
        self.__paymentAmount = ''
        self.__paymentDate = ''
        self.__paymentReference = ''
        self.__recipientName = ''
        self.__recipientBankName = ''
        self.__recipientAccountNumber = ''
        self.__recipientBranchNumber = ''
        self.__isInstantPayment = False

        self.setContent()
        assert(self.__isKnownProofOfPayment())
        assert(self.setPaymentDetails())

    #getters
    def getCustomerName(self):
        return self.__customerName
    def getPaymentAmount(self):
        return self.__paymentAmount
    def getPaymentDate(self):
        return self.__paymentDate
    def getPaymentReference(self):
        return self.__paymentReference
    def getRecipientName(self):
        return self.__recipientName
    def getRecipientBankName(self):
        return self.__recipientBankName
    def getRecipientAccountNumber(self):
        return self.__recipientAccountNumber
    def getRecipientBranchNumber(self):
        return self.__recipientBranchNumber
    def getIsInstantPayment(self):
        return self.__isInstantPayment

    def setContent(self):
        with open(self.__fileName, 'rb') as pop:
            read_pdf = PyPDF2.PdfFileReader(pop)
            number_of_pages = read_pdf.getNumPages()
            page = read_pdf.getPage(0)
            self.__content = page.extractText().split()#this could return an index out of bounds because it is saving a word list into a list

    def __isKnownProofOfPayment(self):
        for bank in checkBankNotifications:
            m = hashlib.sha256()
            for word in self.__content[bank[0]:bank[1]]:
                m.update(word.encode())
            signature = m.hexdigest()

            print(signature, bank[0], bank[1])

            if(signature in knownBankNotifications):
                self.__signature = signature
                self.__bank = knownBankNotifications[signature].split()[0]
                return True
        return False

    def setPaymentDetails(self):
        if self.__bank == "ABSA":
            paymentDetails = getAbsaNotificationDetails(self.__content)

            self.__hasPaymentType = True
            self.__hasCustomerName = True
            self.__hasRecipientName = True
            self.__customerName = paymentDetails[0]
            self.__paymentDate = paymentDetails[1]
            self.__paymentAmount = paymentDetails[2]
            self.__paymentReference = paymentDetails[3]
            self.__recipientName= paymentDetails[4]
            self.__isInstantPayment = paymentDetails[5]
        elif self.__bank == "Capitec":
            paymentDetails = getCapitecNotificationDetails(self.__content)

            self.__hasCustomerName = True
            self.__customerName = paymentDetails[0]
            self.__paymentDate = paymentDetails[1]
            self.__paymentAmount = paymentDetails[2]
            self.__paymentReference = paymentDetails[3]
        elif self.__bank == "Standard":
            paymentDetails = getStandardNotificationDetails(self.__content)

            self.__customerName = paymentDetails[0]
            self.__hasCustomerName = True
            self.__recipientName = paymentDetails[1]
            self.__hasRecipientName = True
            self.__recipientBankName = paymentDetails[2]
            self.__hasRecipientBankName = True
            self.__recipientAccountNumber = paymentDetails[3]
            self.__hasRecipientAccountNumber = True
            self.__recipientBranchNumber = paymentDetails[4]
            self.__hasRecipientBranchNumber = True
            self.__paymentReference = paymentDetails[5]
            self.__hasPaymentReference = True
            self.__paymentAmount = paymentDetails[6]
            self.__hasPaymentAmount = True
            self.__paymentDate = paymentDetails[7]
            self.__hasPaymentDate = True
        else:
            return False
        return True
