#include <AES.h>

#include <gtest/gtest.h>

TEST(AES, common_scenario)
  {
  AES aes;
  const std::string key = "qwertyuioplkjhfm";
  const std::string text = "absdfkaleruaionf";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, different_keys)
  {
  AES aes;
  const std::string key1 = "qwertyuioplkjhfm";
  const std::string key2 = "qwertyuioplkjhfa";
  const std::string text = "absdfkaleruaionf";
  aes.SetKey(key1);
  const std::string encrypted = aes.EncryptString(text);
  aes.SetKey(key2);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_FALSE(text == decrypted);
  }

TEST(AES, small_key)
  {
  AES aes;
  const std::string key = "123";
  const std::string text = "absdfkaleruaionf";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, small_data)
  {
  AES aes;
  const std::string key = "qwertyuioplkjhfm";
  const std::string text = "123";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, not_even_data)
  {
  AES aes;
  const std::string key = "qwertyuioplkjhfm";
  const std::string text = "123123t354yersdDASDafsdfasda";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, small_data_small_key)
  {
  AES aes;
  const std::string key = "123";
  const std::string text = "123";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, key_length_128)
  {
  AES aes(AES::KeySize::AES128);
  const std::string key = "1234567890123456";
  const std::string text = "123";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, key_length_192)
  {
  AES aes(AES::KeySize::AES192);
  const std::string key = "123456789012345612345678";
  const std::string text = "123";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, key_length_256)
  {
  AES aes(AES::KeySize::AES256);
  const std::string key = "12345678901234561234567890123456";
  const std::string text = "123";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, key_length_influance)
  {
  AES aes128(AES::KeySize::AES128);
  AES aes192(AES::KeySize::AES192);
  AES aes256(AES::KeySize::AES256);
  const std::string key128 = "1234567890123456";
  const std::string key192 = "123456789012345612345678";
  const std::string key256 = "12345678901234561234567890123456";
  const std::string text = "0123456789abcdef0123456789abcdef0123456";
  aes128.SetKey(key128);
  aes192.SetKey(key192);
  aes256.SetKey(key256);
  const std::string encrypted128 = aes128.EncryptString(text);
  const std::string encrypted192 = aes192.EncryptString(text);
  const std::string encrypted256 = aes256.EncryptString(text);
  EXPECT_FALSE(encrypted128 == encrypted192);
  EXPECT_FALSE(encrypted128 == encrypted256);
  EXPECT_FALSE(encrypted192 == encrypted256);
  const std::string decrypted128 = aes128.DecryptString(encrypted128);
  const std::string decrypted192 = aes192.DecryptString(encrypted192);
  const std::string decrypted256 = aes256.DecryptString(encrypted256);
  EXPECT_EQ(text, decrypted128);
  EXPECT_EQ(text, decrypted192);
  EXPECT_EQ(text, decrypted256);
  }

TEST(AES_CBC, common_case)
  {
  AES aes(AES::KeySize::AES128, AES::Mode::CBC);
  const std::string key = "1234567890123456";
  const std::string text = "0123456789abcdef0123456789abcdef0123456";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES_CFB, common_case)
  {
  AES aes(AES::KeySize::AES128, AES::Mode::CFB);
  const std::string key = "1234567890123456";
  const std::string text = "0123456789abcdef0123456789abcdef0123456";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES_OFB, common_case)
  {
  AES aes(AES::KeySize::AES128, AES::Mode::OFB);
  const std::string key = "1234567890123456";
  const std::string text = "0123456789abcdef0123456789abcdef0123456";
  aes.SetKey(key);
  const std::string encrypted = aes.EncryptString(text);
  const std::string decrypted = aes.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(AES, different_modes_comparison)
  {
  AES aes_ecb(AES::KeySize::AES128, AES::Mode::ECB);
  AES aes_cbc(AES::KeySize::AES128, AES::Mode::CBC);
  AES aes_cfb(AES::KeySize::AES128, AES::Mode::CFB);
  AES aes_ofb(AES::KeySize::AES128, AES::Mode::OFB);
  AES aes_ctr(AES::KeySize::AES128, AES::Mode::CTR);
  const std::string key = "1234567890123456";
  const std::string text = "0123456789abcdef0123456789abcdef0123456";
  aes_ecb.SetKey(key);
  aes_cbc.SetKey(key);
  aes_cfb.SetKey(key);
  aes_ofb.SetKey(key);
  aes_ctr.SetKey(key);
  const auto encrypted_ecb = aes_ecb.EncryptString(text);
  const auto encrypted_cbc = aes_cbc.EncryptString(text);
  const auto encrypted_cfb = aes_cfb.EncryptString(text);
  const auto encrypted_ofb = aes_ofb.EncryptString(text);
  const auto encrypted_ctr = aes_ctr.EncryptString(text);
  EXPECT_NE(encrypted_ecb, encrypted_cbc);
  EXPECT_NE(encrypted_ecb, encrypted_cfb);
  EXPECT_NE(encrypted_ecb, encrypted_ofb);
  EXPECT_NE(encrypted_ecb, encrypted_ctr);
  EXPECT_NE(encrypted_cbc, encrypted_cfb);
  EXPECT_NE(encrypted_cbc, encrypted_ofb);
  EXPECT_NE(encrypted_cbc, encrypted_ctr);
  EXPECT_NE(encrypted_cfb, encrypted_ofb);
  EXPECT_NE(encrypted_cfb, encrypted_ctr);
  EXPECT_NE(encrypted_ofb, encrypted_ctr);

  const auto decrypted_ecb = aes_ecb.DecryptString(encrypted_ecb);
  const auto decrypted_cbc = aes_cbc.DecryptString(encrypted_cbc);
  const auto decrypted_cfb = aes_cfb.DecryptString(encrypted_cfb);
  const auto decrypted_ofb = aes_ofb.DecryptString(encrypted_ofb);
  const auto decrypted_ctr = aes_ctr.DecryptString(encrypted_ctr);
  EXPECT_EQ(decrypted_ecb, text);
  EXPECT_EQ(decrypted_cbc, text);
  EXPECT_EQ(decrypted_cfb, text);
  EXPECT_EQ(decrypted_ofb, text);
  EXPECT_EQ(decrypted_ctr, text);
  }