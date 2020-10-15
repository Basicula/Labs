# **AES and Kalyna enciphers**

## **Implementation details**
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

## **Configuring and Build**
To configure project you will need CMake. Just ran CMake gui select source dir where CMakeLists.txt is located and select custom build directort, press Generate and project will be generated. To run benchmark comparison you'll need to set as startup project ***Main*** compile and build code and wait while benchmark complete. This comparison will generate file "results.txt" that will contain time performance results for files that locate in **test_files** folder. Also the same report will be available in the command prompt. To run google tests (unittests) set as startup project ***Tests*** compile and build code and wait for testing report.

## **Structure:**
 - Crypto
   - CryptoBase - common functionality for AES and Kalyna
   - AES implementation
   - Kalyna implementation
 - Tests
   - AES tests
   - Kalyna tests
 - aes.py - python version of AES implementation ( very slow :) )

## **Tools**
 - C++17 - main language
 - VisualStudio19 - IDE
 - Cmake - configuration tool
 - GTests - testing tool

## **Results**
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

## **Conclusion**
AES kind of easy to implement and use and also quite fast. Kalyna is more complicated to implement and slower than AES, but maybe more secure than AES.