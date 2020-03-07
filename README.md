# payment reader
Library that can extract payment information for __known__ proof of payments in pdf format. At the moment only written for specific South African banks

## Installation
```git clone https://github.com/YinYin-blip/payment_reader```
## Usage

```payment = ProofOfPayment("/Users/stjohn/Documents/Py/Pop/popJam/Capitec/test-payment_notification.pdf")```
> payment.ProofOfPayment object at 0x102c6b320

```payment.getPaymentAmount()```
> '3000.00'

```payment.getIsInstantPayment()```
> False

```payment.getPaymentDate()```
> ['28/11/2019', '22:23']

If the proof of payment is unknown, the code will crash with assertion self.__isKnownProfOfPayment:

```payment = ProofOfPayment("/Users/stjohn/Documents/Py/Pop/popJam/Capitec/unknown_statement.pdf")```

>Traceback (most recent call last):
>File "<stdin>", line 1, in <module>
>File "/Users/stjohn/Documents/Py/Pop/payment.py", line 59, in __init__
>assert(self.__isKnownProofOfPayment())
>AssertionError


**Important**: this library does not validate the authenticity / integrity of a proof of payments.
