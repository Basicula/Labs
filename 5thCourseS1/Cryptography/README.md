## **All implemented enciphers comparison**
| Encipher       | 1kb|1kb| 1024kb|1024kb| 100mb|100mb| 500mb|500mb| 1gb|1gb|
|----------------|------------|-----------|-------------|-------------|-------------|-------------|-----------|-----------|-----------|-----------|
|                | Encrypted  | Decrypted | Encrypted   | Decrypted   | Encrypted   | Decrypted   | Encrypted | Decrypted | Encrypted | Decrypted |
| AES_CBC_128    | 21.3913 ms | 1.2356 ms | 51.2005 ms  | 43.0060 ms  | 3.0159 s    | 3.6962 s    | 15.8754 s | 18.9562 s | 31.0963 s | 38.5976 s |
| AES_CBC_192    | 5.7989 ms  | 1.4627 ms | 43.1875 ms  | 49.9300 ms  | 3.5474 s    | 4.4970 s    | 18.3803 s | 22.7626 s | 37.1052 s | 45.8658 s |
| AES_CBC_256    | 6.1312 ms  | 2.6950 ms | 47.4833 ms  | 57.6856 ms  | 3.8525 s    | 4.8636 s    | 20.1730 s | 25.2684 s | 40.1374 s | 51.0398 s |
| AES_CFB_128    | 4.8047 ms  | 1.8511 ms | 33.2778 ms  | 39.0076 ms  | 3.0064 s    | 3.0054 s    | 15.6555 s | 15.3256 s | 30.9342 s | 30.9831 s |
| AES_CFB_192    | 4.4550 ms  | 1.5670 ms | 40.2130 ms  | 39.7169 ms  | 3.4854 s    | 3.5346 s    | 18.2149 s | 17.6152 s | 35.6647 s | 36.0189 s |
| AES_CFB_256    | 6.1212 ms  | 2.0195 ms | 52.3962 ms  | 43.7479 ms  | 3.8651 s    | 3.9409 s    | 20.1840 s | 20.1105 s | 40.4273 s | 41.7156 s |
| AES_CTR_128    | 5.5453 ms  | 1.2257 ms | 33.1774 ms  | 36.4067 ms  | 2.9798 s    | 3.0032 s    | 15.2673 s | 15.0603 s | 30.6893 s | 30.4366 s |
| AES_CTR_192    | 6.3785 ms  | 1.8652 ms | 37.2244 ms  | 39.3541 ms  | 3.3636 s    | 3.3917 s    | 17.3909 s | 17.5033 s | 34.7717 s | 34.9647 s |
| AES_CTR_256    | 4.4551 ms  | 2.4164 ms | 54.2517 ms  | 58.3572 ms  | 3.8508 s    | 3.9053 s    | 19.7497 s | 19.7166 s | 39.3894 s | 39.4547 s |
| AES_ECB_128    | 5.4189 ms  | 1.2446 ms | 35.2733 ms  | 43.6031 ms  | 2.8926 s    | 3.6022 s    | 14.8924 s | 18.4679 s | 29.9003 s | 36.8866 s |
| AES_ECB_192    | 4.8646 ms  | 1.3033 ms | 38.2416 ms  | 48.5278 ms  | 3.3942 s    | 4.2328 s    | 17.4821 s | 21.6017 s | 40.7788 s | 54.9137 s |
| AES_ECB_256    | 7.1960 ms  | 2.4884 ms | 44.8378 ms  | 52.7900 ms  | 3.7870 s    | 4.8110 s    | 19.6915 s | 24.6646 s | 47.0781 s | 51.7243 s |
| AES_OFB_128    | 5.7994 ms  | 1.8531 ms | 34.4731 ms  | 34.2065 ms  | 2.9581 s    | 3.0090 s    | 15.1559 s | 15.1602 s | 31.3619 s | 31.5183 s |
| AES_OFB_192    | 4.9686 ms  | 3.2795 ms | 41.5597 ms  | 63.4866 ms  | 3.3606 s    | 3.4717 s    | 17.3372 s | 17.4225 s | 35.7662 s | 36.0692 s |
| AES_OFB_256    | 4.8432 ms  | 1.1843 ms | 42.5543 ms  | 42.7605 ms  | 3.9343 s    | 3.9353 s    | 19.6079 s | 20.1627 s | 40.6933 s | 41.1745 s |
| Kalyna_128x128 | 5.3443 ms  | 1.5503 ms | 204.1995 ms | 204.5372 ms | 19.5447 s   | 19.8946 s   | 1.6467 m  | 1.6307 m  | 3.3953 m  | 3.2863 m  |
| Kalyna_128x256 | 4.8547 ms  | 2.2139 ms | 281.6466 ms | 273.2889 ms | 27.1125 s   | 27.5462 s   | 2.2776 m  | 2.2670 m  | 4.6444 m  | 4.6199 m  |
| Kalyna_256x256 | 5.0218 ms  | 1.7167 ms | 233.3455 ms | 219.6846 ms | 22.0423 s   | 21.9345 s   | 1.8323 m  | 1.8040 m  | 3.7577 m  | 3.6962 m  |
| Kalyna_256x512 | 4.9057 ms  | 1.7247 ms | 288.5588 ms | 282.8807 ms | 28.9035 s   | 27.9216 s   | 2.3393 m  | 2.3114 m  | 4.7791 m  | 4.8026 m  |
| Kalyna_512x512 | 6.9184 ms  | 1.7299 ms | 247.6187 ms | 248.8048 ms | 25.7251 s   | 25.9889 s   | 2.0927 m  | 2.0782 m  | 4.3022 m  | 4.2653 m  |
| RC4            | 4.1183 ms  | 1.0706 ms | 10.4383 ms  | 12.7882 ms  | 626.4285 ms | 642.2768 ms | 3.2864 s  | 3.0476 s  | 6.6257 s  | 6.4003 s  |
| Salsa20_128    | 5.4184 ms  | 1.7593 ms | 13.4839 ms  | 14.3502 ms  | 782.8532 ms | 781.1428 ms | 3.9065 s  | 4.1111 s  | 8.7431 s  | 8.2860 s  |
| Salsa20_256    | 5.5149 ms  | 1.1322 ms | 15.3037 ms  | 13.1515 ms  | 802.9705 ms | 778.6795 ms | 4.0720 s  | 4.0915 s  | 8.1933 s  | 8.0952 s  |

# **LAB №2**
Added RC4 stream cipher.
Added Salsa20 stream cipher with 128 and 256 key length modes.
Added CBC, CFB, OFB and CTR stream cipher modes for AES cipher.

### **Results**

**ms - milliseconds**, **s - seconds**, **us - microseconds** 
| Encipher\Size | 1kb       |    1kb    | 1024kb     |1024kb     | 100mb      |100mb      | 500mb     |500mb     | 1gb       |1gb       |
|---------------|-----------|-----------|------------|------------|------------|------------|-----------|-----------|-----------|-----------|
|               | Encrypted | Decrypted | Encrypted  | Decrypted  | Encrypted  | Decrypted  | Encrypted | Decrypted | Encrypted | Decrypted |
| AES_CBC_128   | 4.8679 ms | 3.6701 ms | 35.138 ms  | 51.6287 ms | 3.08446 s  | 4.13229 s  | 14.7417 s | 18.1743 s | 29.7394 s | 41.4549 s |
| AES_CFB_128   | 4.7728 ms | 903.7 us  | 34.796 ms  | 37.8838 ms | 2.93613 s  | 3.57207 s  | 14.6224 s | 14.9392 s | 29.7324 s | 34.564 s  |
| AES_CTR_128   | 4.379 ms  | 822.3 us  | 32.6665 ms | 38.7065 ms | 2.90884 s  | 3.37622 s  | 14.2903 s | 14.7707 s | 29.9022 s | 34.4539 s |
| AES_ECB_128   | 4.4351 ms | 813.7 us  | 33.6062 ms | 45.9605 ms | 2.84921 s  | 4.13495 s  | 14.4315 s | 17.7446 s | 29.2932 s | 41.3833 s |
| AES_OFB_128   | 4.2873 ms | 869.6 us  | 32.8818 ms | 40.462 ms  | 2.94179 s  | 3.69081 s  | 14.2960 s | 14.6986 s | 29.5473 s | 34.2836 s |
| RC4           | 5.3642 ms | 1.0662 ms | 10.0334 ms | 10.9 ms    | 574.354 ms | 574.874 ms | 8.9127 s  | 8.8914 s  | 6.02778 s | 6.01359 s |
| Salsa20_128   | 5.0588 ms | 986.9 us  | 11.7557 ms | 14.2947 ms | 746.795 ms | 754.257 ms | 3.7795 s  | 3.8042 s  | 7.73646 s | 7.95147 s |
| Salsa20_256   | 3.9793 ms | 1.0937 ms | 10.9296 ms | 12.0526 ms | 752.026 ms | 759.084 ms | 3.7404 s  | 3.9691 s  | 7.88292 s | 8.00517 s |


# **LAB №1**
## **AES and Kalyna enciphers**

### **Implementation details**
All enciphers have similar and simple usage, file-to-file or string-to-string. First of all need to define some key as some string:
```
const std::string key = "someKey";
```
Then define string for encryption or path to file that need to be encrypted/decrypted
```
const std::string original_text = "originalText";
const std::filesystem::path original_file_path("path/to/original_file.ext");
```
Initialize all possible variants for AES:
```
Aes aes128(AES::KeySize::128);
Aes aes192(AES::KeySize::192);
Aes aes256(AES::KeySize::256);
```
Initialize all possible variants for Kalyna:
```
Kalyna kal128x128(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128);
Kalyna kal128x256(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256);
Kalyna kal256x256(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256);
Kalyna kal256x512(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
Kalyna kal512x512(Kalyna::BlockSize::kBlock512, Kalyna::KeySize::kKey512);
```
After initializing encipher it needs a key so set it:
```
aes128.SetKey(key);
kal128x256.SetKey(key);
```
Then it's easy to encrypt/decrypt data. Example for string:
```
const std::string encrypted = aes128.EncryptString(original_text);
const std::string decrypted = aes128.DecryptString(encrypted);
```
Example for files:
```
const std::filesystem::path encrypted_file_path("path/to/encrypted_file.ext");
kal256x256.Encrypt(original_file_path, encrypted_file_path);
const std::filesystem::path decrypted_file_path("path/to/decrypted_file.ext");
kal256x256.Decrypt(encrypted_file_path, decrypted_file_path);
```

### **Configuring and Build**
To configure project you will need CMake. Just ran CMake gui select source dir where CMakeLists.txt is located and select custom build directort, press Generate and project will be generated. To run benchmark comparison you'll need to set as startup project ***Main*** compile and build code and wait while benchmark complete. This comparison will generate file "results.txt" that will contain time performance results for files that locate in **test_files** folder. Also the same report will be available in the command prompt. To run google tests (unittests) set as startup project ***Tests*** compile and build code and wait for testing report.

### **Structure:**
 - Crypto
   - CryptoBase - common functionality for AES and Kalyna
   - AES implementation
   - Kalyna implementation
 - Tests
   - AES tests
   - Kalyna tests
 - aes.py - python version of AES implementation ( very slow :) )

### **Tools**
 - C++17 - main language
 - VisualStudio19 - IDE
 - Cmake - configuration tool
 - GTests - testing tool

### **Results**
**ms - milliseconds**, **s - seconds**, **m - minutes**
| Encipher\Size | 1kb       |      1kb     | 1024kb    |    1024kb       | 100mb     |     100mb      | 500mb     |   500mb        | 1gb       |     1gb      |
|---------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
|               | Encrypted | Decrypted | Encrypted | Decrypted | Encrypted | Decrypted | Encrypted | Decrypted | Encrypted | Decrypted |
| AES128        | 9.3066ms  | 1.5467ms  | 40.55ms   | 44.7304ms | 3.58523s  | 3.90233s  | 19.498s   | 23.7948s  | 31.0494s  | 38.3934s  |
| AES192        | 12.6109ms | 1.9193ms  | 39.6ms    | 48.394ms  | 3.70167s  | 4.66571s  | 21.1684s  | 28.6421s  | 35.7853s  | 44.6767s  |
| AES256        | 10.4882ms | 2.0864ms  | 42.8ms    | 58.5326ms | 4.04517s  | 5.35s     | 24.1312s  | 29.6591s  | 40.5293s  | 51.6038s  |
| Kalyna128x128 | 10.8718ms | 9.3837ms  | 247.1ms   | 303.028ms | 25.2859s  | 25.3347s  | 2.48115m  | 2.52444m  | 4.48912m  | 4.5376m   |
| Kalyna128x256 | 16.1848ms | 17.405ms  | 367.053ms | 362.9ms   | 34.3875s  | 35.0783s  | 3.41846m  | 3.53432m  | 6.51244m  | 5.95694m  |
| Kalyna256x256 | 7.5392ms  | 9.1422ms  | 305.954ms | 303.988ms | 27.2734s  | 27.9587s  | 2.73317m  | 2.76116m  | 4.78525m  | 4.83001m  |
| Kalyna256x512 | 7.1829ms  | 10.22ms   | 365.949ms | 360.204ms | 34.7049s  | 35.6366s  | 3.46135m  | 3.5269m   | 5.78953m  | 6.77706m  |
| Kalyna512x512 | 9.367ms   | 9.6509ms  | 298.93ms  | 305.998ms | 29.832s   | 30.4354s  | 2.90871m  | 2.96645m  | 6.11886m  | 6.19385m  |

### **Conclusion**
AES kind of easy to implement and use and also quite fast. Kalyna is more complicated to implement and slower than AES, but maybe more secure than AES.