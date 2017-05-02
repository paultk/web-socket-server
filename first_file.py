"""The handshake resembles HTTP in allowing servers to handle HTTP connections as well as WebSocket connections on the same port.
Once the connection is established, communication switches to a bidirectional binary protocol which doesn't conform to the HTTP protocol.
In addition to Upgrade headers, the client sends a Sec-WebSocket-Key header containing base64-encoded random bytes, and the server replies
 with a hash of the key in the Sec-WebSocket-Accept header. 
 This is intended to prevent a caching proxy from re-sending a previous WebSocket conversation,[32] and does not provide any authentication, privacy or integrity. The hashing function appends the fixed string 258EAFA5-E914-47DA-95CA-C5AB0DC85B11 (a GUID) to the value from Sec
-WebSocket-Key header (which is not decoded from base64), applies the SHA-1 hashing function, and encodes the result using base64.[33]
"""
'''web_key is bas64 endoded random bytes'''
# return value is hash of the web_key
import hashlib, base64


def message_finished(byte):
    if (byte & 1) == 1:
        return True
    return False


def decode_message(masked_data):
    data_in_bytes = bytearray(masked_data)
    '''If 126, the following 2 bytes interpreted as a
      16-bit unsigned integer are the payload length.  If 127, the
      following 8 bytes interpreted as a 64-bit unsigned integer (the
      most significant bit MUST be 0) are the payload length.'''
    # We get the
    payload_length = data_in_bytes[1] & 127

    mask_start_index = 2
    if payload_length == 126:
        mask_start_index = 4
        payload_length = (data_in_bytes[2] + data_in_bytes[3])
    elif payload_length == 127:
        mask_start_index = 10
        payload_length = 0
#         todo: map
        for i in range(2,10):
            payload_length += data_in_bytes[i]
    payload_start = mask_start_index + 4

    return_string = ''
    '''Octet i of the transformed data ("transformed-octet-i") is the XOR of
   octet i of the original data ("original-octet-i") with octet at index
   i modulo 4 of the masking key ("masking-key-octet-j"):

     j                   = i MOD 4
     transformed-octet-i = original-octet-i XOR masking-key-octet-j
'''
    # to get the inverse(the unmasked char) of the XOR function, we simply do a XOR operation with the the masked byte and the key again
    # the masking key for the individual byte is rotated on the 32 bit(4 bytes) masking key
    for i in range(payload_start, payload_start + payload_length):
        charcode = (data_in_bytes[i] ^ data_in_bytes[mask_start_index + ((i - payload_start) % 4)])
        return_string += chr(charcode)
    return return_string, message_finished(data_in_bytes[0])


def encode(web_key):
    secret_key = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    m = hashlib

    input1 = web_key + secret_key
    input1 = input1.encode('utf-8')
    hashed = hashlib.sha1()
    d = hashed.update(input1)
    done = hashed.digest()

    output = ''
    m = base64

    encoded_finish = base64.b64encode(done)
    return encoded_finish


def create_message(test):
    return_array = bytearray()


    # test='this is a test'
    for char in test:
        return_array.append(int((ord(char))))
        print(bin(ord(char)))
    return return_array
