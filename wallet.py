import time
import hashlib
import string
import codecs
import base58
import ecdsa
import random

""" Litecoin Wallet Generator v0.1

         Pedro Fortes - 02/2018

         https://pypi.python.org/pypi/ecdsa - ECDSA manual"""

class Keys:


        def __init__(self):
            self.privkey = ''
            self.pubkey  = ''
            self.pubaddr = ''

            self.generate()
 
        def generate(self, seed=None):

            if(seed==None): seed = str(time.time()) + ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

            oPk = hashlib.sha256(seed.encode())
            self.privkey = oPk.hexdigest()
            
            # SECP256k1 - Bitcoin elliptic curve
            oSk = ecdsa.SigningKey.from_string(oPk.digest(), curve=ecdsa.SECP256k1)                    
            oVk = oSk.get_verifying_key()

            hexlify = codecs.getencoder('hex')
             
            self.pubkey = str(hexlify(b'\04' + oVk.to_string())[0].decode('utf-8'))
            #print(self.pubkey)
            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(hashlib.sha256(codecs.decode(self.pubkey, "hex")).digest())

            middle_man = b'\x30' + ripemd160.digest()
            checksum = hashlib.sha256(hashlib.sha256(middle_man).digest()).digest()[:4]        
            binary_addr = middle_man + checksum
 
            self.pubaddr = base58.b58encode(binary_addr)            

        def __str__(self):
                
            return 'Private Key: {0}\nPublic Key: {1}'.format(self.privkey, self.pubaddr)


if __name__ == "__main__":
        
        wallet = Keys()
        print(wallet)
  
