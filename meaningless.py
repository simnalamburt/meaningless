import base64, struct

class Meaningless(object):
    def __init__(self, key_64):
        self._upper = key_64 >> 32
        self._lower = key_64 & 0xFFFFFFFF

    def encode(self, plain_64):
        lower_plain = plain_64 & 0xFFFFFFFF
        upper_coded = \
            (plain_64 >> 32) ^ \
            (self._upper * lower_plain & 0xFFFFFFFF)

        lower_coded = (upper_coded * self._lower & 0xFFFFFFFF ^ lower_plain)

        return upper_coded << 32 | lower_coded

    def decode(self, coded_64):
        lower_coded = coded_64 & 0xFFFFFFFF
        upper_coded = coded_64 >> 32

        lower_plain = upper_coded * self._lower & 0xFFFFFFFF ^ lower_coded
        upper_plain = upper_coded ^ (self._upper * lower_plain & 0xFFFFFFFF)

        return upper_plain << 32 | lower_plain

    def encode_hex(self, plain_64):
        return '%016x' % self.encode(plain_64)

    def decode_hex(self, cstr):
        return self.decode(int(cstr, 16))

    def encode_base64(self, plain_64):
        coded = self.encode(plain_64)
        bytes = struct.pack('<Q', coded).rstrip(b'\x00')
        if len(bytes) == 0:
            bytes = b'\x00'
        return base64.urlsafe_b64encode(bytes).rstrip(b'=')

    def decode_base64(self, coded_base64):
        bytes = base64.urlsafe_b64decode(coded_base64 + b'==')
        coded = struct.unpack('<Q', bytes + b'\x00'* (8-len(bytes)) )[0]
        return self.decode(coded)
