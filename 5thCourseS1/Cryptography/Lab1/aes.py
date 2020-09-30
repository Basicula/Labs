import numpy as np
import random as rand
import time

sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

inv_sbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

def sub_word(word):
    return [sbox[byte] for byte in word]
    
def shift_line(line, inv = False):
    if inv:
        line.insert(0, line.pop())
    else:
        line.append(line.pop(0))
    return line
    
def mult(byte, k):
    if k <= 0:
        return 0
    if k == 1:
        return byte
    
    if k == 2:
        if byte < 0x80:
            return (byte << 1)
        else:
            return ((byte << 1) ^ 0x1b) % 0x100
            
    power = -1
    n = k
    while n:
        n = (n >> 1)
        power += 1
    
    return (mult(mult(byte, 2**(power-1)), 2) ^ mult(byte, k - 2**power)) % 0x100

def state_to_str(state):
    b = []
    for word in state:
        for byte in word:
            b.append(byte)

    res = None
    for byte in b:
        if not res:
            res = bytes([byte])
        else:
            res += bytes([byte])

    return res

class AES:
    def __init__(self):
        self.cipher_key = ''
        self.nb = 4
        self.nk = 4
        self.nr = 10
        
        self.generate_mult_table()
        
    def generate_mult_table(self):
        self.mult = []
        for num in range(16):
            self.mult.append([])
            for byte in range(256):
                self.mult[num].append(mult(byte, num))
        
    def set_key(self, key):
        self.key_expansion(key)
        
    def check_input(self, input):
        if len(input) != 4 * self.nb:
            raise Exception("wrong size of sequence ", len(input))
        if type(input) == str:
            return
        for x in input:
            if x < 0 or x > 255:
                raise Exception("unsopported value in sequence, not in interval [0, 255]")
        
    def prepare_key(self, key):
        if type(key) == str:
            key_bytes = bytes(key, 'utf8')
            return [[key_bytes[i * 4 + j] for j in range(4)] for i in range(self.nk)]
        return [[key[i * 4 + j] for j in range(4)] for i in range(self.nk)]
            
        
    def key_expansion(self, key):
        key = self.prepare_key(key)

        self.key_schedule = []
        for word in key:
            self.key_schedule.append(word)

        for i in range(self.nk, self.nb * (self.nr + 1)):
            temp = self.key_schedule[i-1][:]
            if i % self.nk == 0:
                temp = sub_word(shift_line(temp))
                temp[0] ^= rcon[i // self.nk]
            elif self.nk > 6 and i % self.nk == 4:
                temp = sub_word(temp)
            
            for j in range(len(temp)):
                temp[j] ^= self.key_schedule[i - self.nk][j]
                
            self.key_schedule.append(temp[:])
           
        
    def encrypt(self, sequence):
        self.check_input(sequence)
        
        state = self.prepare_key(sequence)
        
        state = self.add_round_key(state, 0)
        for round_idx in range(1, self.nr):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, round_idx)
            
        
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, self.nr)
        
        return state_to_str(state)
        
    def decrypt(self, sequence):        
        state = self.prepare_key(sequence)
        
        for word in state:
            print(hex(word[0]),hex(word[1]),hex(word[2]),hex(word[3]))
        state = self.add_round_key(state, self.nr)
    
        for round_idx in range(self.nr - 1, 0, -1):
            state = self.shift_rows(state, True)
            state = self.sub_bytes(state, True)
            state = self.add_round_key(state, round_idx)
            state = self.mix_columns(state, True)
    
        state = self.shift_rows(state, True)
        state = self.sub_bytes(state, True)
        state = self.add_round_key(state, 0)
        
        return state_to_str(state)
        
    def sub_bytes(self, state, inv = False):
        return [[inv_sbox[byte] if inv else sbox[byte] for byte in word] for word in state]
        
    def shift_rows(self, state, inv = False):
        new_state = [word[:] for word in state]
    
        for i in range(len(state)):
            for j in range(4):
                new_state[i][j] = state[(i-j if inv else i+j) % len(state)][j]
    
        return new_state
        
    def mix_columns(self, state, inv = False):
        new_state = [word[:] for word in state]
        for i in range(self.nb):
            if inv == False:
                new_state[i][0] = self.mult[2][state[i][0]]     ^ self.mult[3][state[i][1]]     ^ state[i][2]                   ^ state[i][3]
                new_state[i][1] = state[i][0]                   ^ self.mult[2][state[i][1]]     ^ self.mult[3][state[i][2]]     ^ state[i][3]
                new_state[i][2] = state[i][0]                   ^ state[i][1]                   ^ self.mult[2][state[i][2]]     ^ self.mult[3][state[i][3]]
                new_state[i][3] = self.mult[3][state[i][0]]     ^ state[i][1]                   ^ state[i][2]                   ^ self.mult[2][state[i][3]]
            else:
                new_state[i][0] = self.mult[14][state[i][0]]    ^ self.mult[11][state[i][1]] ^ self.mult[13][state[i][2]] ^ self.mult[9][state[i][3]]
                new_state[i][1] = self.mult[9][state[i][0]]     ^ self.mult[14][state[i][1]] ^ self.mult[11][state[i][2]] ^ self.mult[13][state[i][3]]
                new_state[i][2] = self.mult[13][state[i][0]]    ^ self.mult[9][state[i][1]]  ^ self.mult[14][state[i][2]] ^ self.mult[11][state[i][3]]
                new_state[i][3] = self.mult[11][state[i][0]]    ^ self.mult[13][state[i][1]] ^ self.mult[9][state[i][2]]  ^ self.mult[14][state[i][3]]
        return new_state
        
    def add_round_key(self, state, round_idx):
        new_state = [[0 for j in range(4)] for i in range(len(state))]
    
        for i, word in enumerate(state):
            for j, byte in enumerate(word):
                new_state[i][j] = byte ^ self.key_schedule[round_idx * self.nb + i][j]
    
        return new_state
    
aes = AES()

def encode_file(input, output):
    fin = open(input, 'rb')
    fout = open(output, 'wb')
    while True:
        data = fin.read(16)
        if data:
            fout.write(aes.encrypt(data))
        else:
            break
            
def decode_file(input, output):
    fin = open(input, 'rb')
    fout = open(output, 'wb')
    while True:
        data = fin.read(16)
        if data:
            fout.write(aes.decrypt(data))
        else:
            break
        
def generate_file(size, file):
    with open(file, 'wb') as f:
        data = [rand.randint(0, 255) for i in range(size)]
        f.write(bytes(data))

if __name__ == "__main__":
    key = b'qwertyuioplkjhfm'
    #aes.set_key(key)
    #start_time = time.time()
    #for size in { 1024, 1024 * 1024, 100 * 1024 * 1024, 1024 * 1024 * 1024}:
    #    original_file = "original_{0}.txt".format(size)
    #    encoded_file =  "encoded_{0}.txt".format(size)
    #    decoded_file =  "decoded_{0}.txt".format(size)
    #    generate_file(size, original_file)
    #    print("generated file with size {0} in {1} seconds".format(size, time.time() - start_time))
    #    start_time = time.time()
    #    encode_file(original_file, encoded_file)
    #    print("encoded file with size {0} in {1} seconds".format(size, time.time() - start_time))
    #    start_time = time.time()
    #    decode_file(encoded_file, decoded_file)
    #    print("decoded file with size {0} in {1} seconds".format(size, time.time() - start_time))
    #    start_time = time.time()
    #key = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    #data = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff]
    data = b'1234567890123456'
    aes = AES()
    aes.set_key(key)
    print(data)
    data = aes.encrypt(data)
    print(data)
    data = aes.decrypt(data)
    print(data)
    #print(hex(mult(0x57, 2)))
    #print(hex(mult(0x57, 4)))
    #print(hex(mult(0x57, 8)))
    #print(hex(mult(0x57, 10)))
    #print(hex(mult(0x57, 13)))