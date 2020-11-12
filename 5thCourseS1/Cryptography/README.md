# **RSA Cryptosystem**
Implemented RSA algorithm together with BigInt type.
Custom BigInt has all common arithmetic functions and also implemented additional functional for modulo calculations. Some examples for using BigInt:
```cpp
bigint a = "123456324124352512324351"; // can be as long as you want
bigint b = 421; // can be any fundamental type (int, double, etc)
// common operations
a /= b;
b += a;
b += 2321;
a = -321;
a = bigint::abs(a);
// comparison operations also present
bool less = a < b;
bool is_eq = a == b;
// more complex functional located in separate namespace
a = ModuloOperations::pow(a, b, a + b); // same as a ^ b mod (a + b)
a = ModuloOperations::inverse(a, b); // solve the equation a * x = 1 mod b
auto gcd = ModuloOperations::gcd(a, b); // find gcd for a and b
```
RSA implementation based on bigint and created with prime bit size.
```cpp
RSA rsa1024(1024); // create rsa that will have prime numbers length 1024 bits
bigint message = "123453234532151";
// rsa usage
auto encrypted = rsa1024.Encrypt(message);
auto decrypted = rsa1024.Decrypt(encrypted);
```
Dump samples:
```sh
Using prime bit size: 256
Message to process: 57896044618658097711785492504343961863040629611515393858897269864914353142265
RSA state:
        first prime:    57896044618658097711785492504343953926634992332820282019728792003956564843089
        second prime:   57896686804586701181427108462449056461312956639576724580893816771635585163341
        prime product:  3351989162510825175755397010316566485590355462592732348226647965364821537341066621595831584414726541776707788896222112762658355090277279629682980100000349
        ctf:            837997290627706293938849252579141621397588865648183087056661991341205384335237707216102084903958332293935248971458541203421489520919164255226846987498480
        public key:     10872174001704354348532258153991117509373222432705076520708283076799075921881000151669857516800489049
        private key:    217591612420062367971435934483911932491567290002712201798729285422904930700643068784657477582140956297331235062776520017993809930223037062260746792512489
RSA initialized in: 242.403 ms
Encrypted 2010995147826476728127887546824349171637382668077414849394579796282903908015577718810999441171831765815430103184301873475143840247599097952711762472737152
in: 13.1092 ms
Decrypted 57896044618658097711785492504343961863040629611515393858897269864914353142265
in: 11.8167 ms

Using prime bit size: 1024
Message to process: 89884656743115795386465259539451236680898848947115328636715040578866337902750481566354238661203768010560056939935696678829394884407208311246423715319737062188883946712432742638151109800623047059726541476042502884419075341171231440736956555270413618581675255342293149646730726774527257578886341507097414346784
RSA state:
        first prime:    89884656743115795386465259539451236680898848947115328636715040578866337902750481566354238661203768010560056939935696678829394884407208311246423715319737062188883946712432742638151109800623049975475092987667654368900134581785482617699121855943955582753436362314388432441490379904427296006915343709196137839263
        second prime:   89884656743115795386465259539451236680898848947115328636715040578866337902750481566354238661203768010560056939935696678829394884407208311246423715319737062188883946712432742638151109800623047059726541476042502884419075341171231440736956555270413618581675264977973443423302652782081465896681773302836577194749
        prime product:  8079251517827751825178719172167487990111025667428871008032586356881163784716972723299300352880728365922179490230474504873529889787622730273772038096612070780157719341825249022937549437597413288780072111455527637694964302123678277660350348841966049401890468790261538483539823400595009349947276018550868180116783511398909381758734971417446749344473837312789559190008570904432986716852518171075082202073624172246491419569020135523225796423365819237159984468906140051040600588963155708751428044074449440033901180905827960311987616309854646858916236449779274352449222556831358404057201322453330479933930183821770809629987
        ctf:            4039625758913875912589359586083743995055512833714435504016293178440581892358486361649650176440364182961089745115237252436764944893811365136886019048306035390078859670912624511468774718798706644390036055727763818847482151061839138830175174420983024700945234395130769241769911700297504674973638009275434090058301871042711575083981020449183923435556019807447664266367570411637627020523508603971186862375608318112685652844574371082783503327275701307333568519133332963331416347769145111737562912236601671499349773221058901529334203193448966400240079019282452575557055464769498264096204144883410859015166533404869047297988
        public key:     4262941548746997331633432388580814903484506985196254015039845761238454916049288819515971450366757779706706696118739414997768228477639341717300050705916884585640653448022822497565650926676467298534521216652693077929370488371065065999461868123612537528725165798175560643068668956113328687820559542451055166350993490640871508433069757710266289100195756771253118485534623368037527146941846518066571474487359423124371309774820882156072352418593677504245020013849337475959019914351339839067807850310748865175938997344859555663976353630050421195224155908587936362431960974379142151642150523612790569
        private key:    1239022267856069755754185915415961560903362236836181858900976895430781294159045805030999429886047707657189858985030825572549768452348283841189630560375949967232038815491813117560057647382718658235003889411999545873368489966271871654425376080769826414426843888616455755466627464893308732213016386686258568299414797127169609612953857536611374336902058152654625996188557072685571506404569266609480412118166156733293051335927692508219280261560399128273477191240138906171960435667415208829722605024964199456424142480265593179438831605553929248024381004654583558013426484032178882160888358849971542131231437207847223155089
RSA initialized in: 1.102 m
Encrypted 5701312713116880604158675177030314932072466216872589687746279632243284812713755028292099178261815585392677393055201988586531584921245027510272618414978738051623032303209938200729487571505355525437367400002348156387619083542382088205060084130745434066030191615039761278215731017890489311063162085723994403777534922372912450786422950978171021750370755602301101001938376742955634689875272414769915674522711092245063051170213513211972263007856608577269845979243602869473687250921841896302598793360957539922477605127240758264771712384092509403760809916675737666446093092535217843752765282683834053411862312403011063926753
in: 761.251 ms
Decrypted 89884656743115795386465259539451236680898848947115328636715040578866337902750481566354238661203768010560056939935696678829394884407208311246423715319737062188883946712432742638151109800623047059726541476042502884419075341171231440736956555270413618581675255342293149646730726774527257578886341507097414346784
in: 228.391 ms
```
Final performance results for different prime size
| Prime bit size | Init time | Encrypt | Decrypt |
|----------------|-----------|---------|---------|
| 8              | 1 ms      | 35 us   | 55 us   |
| 16             | 2 ms      | 60 us   | 120 us  |
| 32             | 5 ms      | 70 us   | 200 us  |
| 64             | 20 ms     | 700 us  | 700 ms  |
| 128            | 40 ms     | 1.5 ms  | 2 ms    |
| 256            | 150 ms    | 10 ms   | 7 ms    |
| 512            | 2 s       | 32 ms   | 35 ms   |
| 1024           | 50 s      | 700 ms  | 300 ms  |


# **Hash Functions**
Implemented SHA256, Kupyna512 and Kupyna256 hash functions. Birthday attack and brute force algorithms for proof-of-work/finding partial collisions
## **Average iterations for birthday attack to get partial collision with specific prefix length**
| Prefix length | Kupyna256 | Kupyna512 | SHA256 |
|---------------|-----------|-----------|--------|
| 1             | 4         | 4         | 4      |
| 2             | 20        | 18        | 18     |
| 3             | 73        | 75        | 75     |
| 4             | 334       | 309       | 307    |
| 5             | 1342      | 1192      | 1295   |
| 6             | 4795      | 5366      | 4904   |
| 7             | 19353     | 20086     | 21201  |
| 8             | 85105     | 89316     | 82990  |

## **Samples for prefix length 8**
```
Kupyna256:
        Text1                                   = "w61vgz86w9wdbeunpeikelve:46073"
        Text2                                   = "w61vgz86w9wdbeunpeikelve:15385"
        Hash1                                   = "eb63d31007b4995fdf9daa6c23a9a342c274d251388429e26efbe455a3521661"
        Hash2                                   = "eb63d3104d8ab039e8a77403d506c558281c6e9a17fc9c752983e9f95aed4145"
        Avarage tries to get partial collision  = "85105"
Kupyna512:
        Text1                                   = "55fx7a3eyzp9z6xo906v56586xn9qxuznury1lcjfrryqr2v92ve03aqxgr1a6a564pql664gw5x2heccoe9urx:91362"
        Text2                                   = "55fx7a3eyzp9z6xo906v56586xn9qxuznury1lcjfrryqr2v92ve03aqxgr1a6a564pql664gw5x2heccoe9urx:35424"
        Hash1                                   = "f206465acb3f3ad35f75b37271725b56e6c51b1011041384633212aad8d7c098716e2983c4bc9349a70aef41eb4bed54df03508f879a8cacbfb4bc6b9fa143a3"
        Hash2                                   = "f206465ac33ddb3574a0844a905fc37406f6b3dc47f03a34535bb61d724e31458c8955aaceccb367ec95e69b88c95863e775fed743ff73b003bd81f565f7c276"
        Avarage tries to get partial collision  = "89316"
SHA256   :
        Text1                                   = "8x7letkkm2hbt8yxlxcg7d8aeaq7xpi0dw3wps238d2zbmr6nbaw0d2u9ecn006fzt6meexw6v7jki2muc80iw577bok92jnuh8qbfcf6yvhentk327do4olp1r:120203"
        Text2                                   = "8x7letkkm2hbt8yxlxcg7d8aeaq7xpi0dw3wps238d2zbmr6nbaw0d2u9ecn006fzt6meexw6v7jki2muc80iw577bok92jnuh8qbfcf6yvhentk327do4olp1r:84233"
        Hash1                                   = "792234e443f410cefe0736db87ccca09ee6f323935f2824b49a5ad0f1d19c872"
        Hash2                                   = "792234e4e689d1c561b2fb151a249040ec8218a02355e202fede948157bdc58d"
        Avarage tries to get partial collision  = "82990"
```

#
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

#
# **Stream enciphers**
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


#
# **AES and Kalyna enciphers**

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