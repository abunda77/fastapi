import os
import base64

secret_key_bytes = os.urandom(32)  # Menghasilkan 32 byte acak
secret_key = base64.urlsafe_b64encode(secret_key_bytes).decode('utf-8')
print(secret_key)
