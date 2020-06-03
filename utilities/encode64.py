import base64

# generating a base64 url encoded string from the image
def encode(path):
    with open(path, 'rb') as reader:
        encoded_string = base64.b64encode(reader.read())

    return encoded_string.decode('utf-8')

