from ecdsa import SigningKey, SECP256k1, VerifyingKey
import os
import binascii

class ECCCipher:
    def __init__(self):
        self.keys_dir = os.path.join(os.path.dirname(__file__), 'keys')
        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)

    def generate_keys(self):
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.get_verifying_key()
        
        with open(os.path.join(self.keys_dir, 'privateKey.pem'), 'wb') as f:
            f.write(sk.to_pem())
        with open(os.path.join(self.keys_dir, 'publicKey.pem'), 'wb') as f:
            f.write(vk.to_pem())
        return "Keys generated successfully!"

    def load_keys(self):
        try:
            with open(os.path.join(self.keys_dir, 'privateKey.pem'), 'rb') as f:
                sk = SigningKey.from_pem(f.read())
            with open(os.path.join(self.keys_dir, 'publicKey.pem'), 'rb') as f:
                vk = VerifyingKey.from_pem(f.read())
            return sk, vk
        except:
            return None, None

    def sign(self, message):
        sk, _ = self.load_keys()
        if not sk: return "Keys not found"
        # Ký message (đã encode) và trả về hex string
        signature = sk.sign(message.encode('utf-8'))
        return binascii.hexlify(signature).decode('utf-8')

    def verify(self, message, signature):
        _, vk = self.load_keys()
        if not vk: return False
        try:
            # Verify signature (convert hex string back to bytes)
            return vk.verify(binascii.unhexlify(signature), message.encode('utf-8'))
        except:
            return False