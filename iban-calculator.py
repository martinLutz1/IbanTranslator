import requests
import argparse

class Iban:
    def __init__(self, iban):
        self._iban = iban
        self._error = ''

        self._check()

    def _check(self):
        if self._iban.lower().startswith('de'):
            if len(self._iban) != 22:
                self._error = 'German IBANs must have a length of 22.'
                return
        
        headers = {'Authorization': 'token zRLH_7YfeEgZVhU1gM_G9f3nbFhOcWIDeje2-xaYHcQAsCFoncktoVMiD80VwMXT'}
        r = requests.post('https://fintechtoolbox.com/validate/iban.json?iban={}'.format(self._iban), headers=headers)
        try:
            result = r.json()
            if 'valid' in result and not result['valid']:
                self._error = 'IBAN is not valid. Please check again.'
                return
            iban = result['iban']
            print('Country code:   {}'.format(iban['country_code']))
            print('BIC:            {}'.format(iban['bic']))
            print('Bank code:      {}'.format(iban['bank_code']))
            print('Account number: {}'.format(iban['account_number']))
        except ValueError:
            self._error = str(r)
            return

    def printError(self):
        if self._error:
            print('Error: ' + self._error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get detailed information about an IBAN.')
    parser.add_argument('iban', type=str, help='An IBAN.')

    args = parser.parse_args()
    ib = Iban(args.iban)
    ib.printError()
    