import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import OpenSSL.crypto as crypto

app = FastAPI()

class CardDetails(BaseModel):
    public_key: str
    card_number: str
    month: str
    year: str
    cvv: str

def encrypt(text, public_key_string):
    public_key_bytes = base64.b64decode(public_key_string)
    public_key_obj = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_bytes)
    encrypted = crypto.public_encrypt(text.encode('utf8'), public_key_obj, crypto.constants.RSA_PKCS1_PADDING)
    return base64.b64encode(encrypted).decode('utf8')

@app.post("/")
async def encrypt_card_details(card_details: CardDetails):
    encrypted_card_number = encrypt(card_details.card_number, card_details.public_key)
    encrypted_month = encrypt(card_details.month, card_details.public_key)
    encrypted_year = encrypt(card_details.year, card_details.public_key)
    encrypted_cvv = encrypt(card_details.cvv, card_details.public_key)
    return {
        "encryptedCardNumber": encrypted_card_number,
        "encryptedMonth": encrypted_month,
        "encryptedYear": encrypted_year,
        "encryptedCVV": encrypted_cvv
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

