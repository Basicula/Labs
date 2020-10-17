#include <Salsa20.h>

#include <gtest/gtest.h>

TEST(Salsa20_128, common_case)
  {
  Salsa20 salsa20_128(Salsa20::KeyLength::Key128);
  const std::string key = "0123456789abcdef";
  salsa20_128.SetKey(key);
  const std::string text = "sometext";
  const auto encrypted = salsa20_128.EncryptString(text);
  const auto decrypted = salsa20_128.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Salsa20_128, small_key)
  {
  Salsa20 salsa20_128(Salsa20::KeyLength::Key128);
  const std::string key = "key";
  salsa20_128.SetKey(key);
  const std::string text = "sometext";
  const auto encrypted = salsa20_128.EncryptString(text);
  const auto decrypted = salsa20_128.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Salsa20_128, big_key)
  {
  Salsa20 salsa20_128(Salsa20::KeyLength::Key128);
  const std::string key = "0123456789abcdefadghj";
  salsa20_128.SetKey(key);
  const std::string text = "sometext";
  const auto encrypted = salsa20_128.EncryptString(text);
  const auto decrypted = salsa20_128.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Salsa20_128, different_keys_deifferent_encrypted_string)
  {
  Salsa20 salsa20_128(Salsa20::KeyLength::Key128);
  const std::string small_key = "key";
  const std::string key = "0123456789abcdef";
  const std::string big_key = "afhabsgkljawbrlwh,hfas";
  const std::string text = "sometext";

  salsa20_128.SetKey(small_key);
  const auto encrypted1 = salsa20_128.EncryptString(text);
  const auto decrypted1 = salsa20_128.DecryptString(encrypted1);
  EXPECT_EQ(text, decrypted1);

  salsa20_128.SetKey(key);
  const auto encrypted2 = salsa20_128.EncryptString(text);
  const auto decrypted2 = salsa20_128.DecryptString(encrypted2);
  EXPECT_EQ(text, decrypted2);

  salsa20_128.SetKey(big_key);
  const auto encrypted3 = salsa20_128.EncryptString(text);
  const auto decrypted3 = salsa20_128.DecryptString(encrypted3);
  EXPECT_EQ(text, decrypted3);

  EXPECT_NE(encrypted1, encrypted2);
  EXPECT_NE(encrypted1, encrypted3);
  EXPECT_NE(encrypted2, encrypted3);
  }

TEST(Salsa20_256, common_case)
  {
  Salsa20 salsa20_256(Salsa20::KeyLength::Key256);
  const std::string key = "0123456789abcdef0123456789abcdef";
  salsa20_256.SetKey(key);
  const std::string text = "sometext";
  const auto encrypted = salsa20_256.EncryptString(text);
  const auto decrypted = salsa20_256.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Salsa20_256, small_key)
  {
  Salsa20 salsa20_256(Salsa20::KeyLength::Key256);
  const std::string key = "key";
  salsa20_256.SetKey(key);
  const std::string text = "sometext";
  const auto encrypted = salsa20_256.EncryptString(text);
  const auto decrypted = salsa20_256.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Salsa20_256, big_key)
  {
  Salsa20 salsa20_256(Salsa20::KeyLength::Key256);
  const std::string key = "jdlfurmandrilfmanrtifl,adeurfncadasf";
  salsa20_256.SetKey(key);
  const std::string text = "sometext";
  const auto encrypted = salsa20_256.EncryptString(text);
  const auto decrypted = salsa20_256.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Salsa20_256, different_keys_deifferent_encrypted_string)
  {
  Salsa20 salsa20_256(Salsa20::KeyLength::Key256);
  const std::string small_key = "key";
  const std::string key = "0123456789abcdef0123456789abcdef";
  const std::string big_key = "jdlfurmandrilfmanrtiflasdasdasd,hfas";
  const std::string text = "sometext";

  salsa20_256.SetKey(small_key);
  const auto encrypted1 = salsa20_256.EncryptString(text);
  const auto decrypted1 = salsa20_256.DecryptString(encrypted1);
  EXPECT_EQ(text, decrypted1);

  salsa20_256.SetKey(key);
  const auto encrypted2 = salsa20_256.EncryptString(text);
  const auto decrypted2 = salsa20_256.DecryptString(encrypted2);
  EXPECT_EQ(text, decrypted2);

  salsa20_256.SetKey(big_key);
  const auto encrypted3 = salsa20_256.EncryptString(text);
  const auto decrypted3 = salsa20_256.DecryptString(encrypted3);
  EXPECT_EQ(text, decrypted3);

  EXPECT_NE(encrypted1, encrypted2);
  EXPECT_NE(encrypted1, encrypted3);
  EXPECT_NE(encrypted2, encrypted3);
  }

TEST(Salsa20, different_key_length_different_encrypted_results)
  {
  Salsa20 salsa20_128(Salsa20::KeyLength::Key128);
  Salsa20 salsa20_256(Salsa20::KeyLength::Key256);
  const std::string key128 = "0123456789abcdef";
  const std::string key256 = "0123456789abcdef0123456789abcdef";
  const std::string text = "sometext";

  salsa20_128.SetKey(key128);
  const auto encrypted128 = salsa20_128.EncryptString(text);
  const auto decrypted128 = salsa20_128.DecryptString(encrypted128);
  EXPECT_EQ(text, decrypted128);

  salsa20_256.SetKey(key256);
  const auto encrypted256 = salsa20_256.EncryptString(text);
  const auto decrypted256 = salsa20_256.DecryptString(encrypted256);
  EXPECT_EQ(text, decrypted256);

  EXPECT_NE(encrypted128, encrypted256);
  }