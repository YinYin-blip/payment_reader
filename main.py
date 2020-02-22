from payment import *

POP_PATH = "/Users/stjohn/Documents/Py/Pop/popJam/paymentTest/"

def main():
    with os.scandir(POP_PATH) as it:
        for pop in it:
            if pop.name[0] == '.':
                continue
            else:
                print(pop.name)
                print(POP_PATH+pop.name)
                payment = ProofOfPayment(POP_PATH+pop.name)

if __name__ == '__main__':
    main()
