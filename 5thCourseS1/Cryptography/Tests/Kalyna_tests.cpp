#include <Kalyna.h>

#include <gtest/gtest.h>

TEST(Kalyna128x128, good_scenario)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128);
  const std::string key = "qwertyuioplkjhfm";
  const std::string text = "absdfkaleruaionf";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna128x128, small_key)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128);
  const std::string key = "qwertyu";
  const std::string text = "absdfkaleruaionf";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna128x128, small_data)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128);
  const std::string key = "qwertyuioplkjhfm";
  const std::string text = "abs";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna128x256, good_scenario)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256);
  const std::string key = "qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkaleruaionf";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna128x256, small_key)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256);
  const std::string key = "qwertyuioplkjhfm1234";
  const std::string text = "absdfkaleruaionf";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna128x256, small_data)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256);
  const std::string key = "qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkalerua";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna128x512, wrong_constructor_info)
  {
  EXPECT_ANY_THROW(Kalyna(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey512));
  }

TEST(Kalyna256x128, wrong_constructor_info)
  {
  EXPECT_ANY_THROW(Kalyna(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey128));
  }

TEST(Kalyna256x256, good_scenario)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256);
  const std::string key = "qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkaleruaionfqwertyuioplkjhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna256x256, small_data)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256);
  const std::string key = "qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkalerujhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna256x256, small_key)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256);
  const std::string key = "qwertyuioplkjhfm123";
  const std::string text = "absdfkaleruaionfqwertyuioplkjhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna256x512, good_scenario)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  const std::string key = "qwertyuioplkjhfm1234567890123456qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkaleruaionfqwertyuioplkjhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna256x512, small_data)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  const std::string key = "qwertyuioplkjhfm1234567890123456qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkalerujhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna256x512, small_key)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  const std::string key = "qwertyuioplkjhfm123";
  const std::string text = "absdfkaleruaionfqwertyuioplkjhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna512x128, wrong_constructor_info)
  {
  EXPECT_ANY_THROW(Kalyna(Kalyna::BlockSize::kBlock512, Kalyna::KeySize::kKey128));
  }

TEST(Kalyna512x256, wrong_constructor_info)
  {
  EXPECT_ANY_THROW(Kalyna(Kalyna::BlockSize::kBlock512, Kalyna::KeySize::kKey256));
  }

TEST(Kalyna512x512, good_scenario)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  const std::string key = "qwertyuioplkjhfm1234567890123456qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkaleruaionfqwertyuioplkjhfmabsdfkaleruaionfqwertyuioplkjhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna512x512, small_data)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  const std::string key = "qwertyuioplkjhfm1234567890123456qwertyuioplkjhfm1234567890123456";
  const std::string text = "absdfkalerujhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna512x512, small_key)
  {
  Kalyna kal(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  const std::string key = "qwertyuioplkjhfm123";
  const std::string text = "absdfkaleruaionfqwertyuioplkjhfmabsdfkaleruaionfqwertyuioplkjhfm";
  kal.SetKey(key);
  const std::string encrypted = kal.EncryptString(text);
  const std::string decrypted = kal.DecryptString(encrypted);
  EXPECT_EQ(text, decrypted);
  }

TEST(Kalyna, different_combinations_comparison)
  {
  Kalyna kal128x128(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128);
  Kalyna kal128x256(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256);
  Kalyna kal256x256(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256);
  Kalyna kal256x512(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512);
  Kalyna kal512x512(Kalyna::BlockSize::kBlock512, Kalyna::KeySize::kKey512);
  const std::string key = "12334567";
  kal128x128.SetKey(key);
  kal128x256.SetKey(key);
  kal256x256.SetKey(key);
  kal256x512.SetKey(key);
  kal512x512.SetKey(key);
  const std::string data = "testdata";
  const std::string encrypted128x128 = kal128x128.EncryptString(data);
  const std::string encrypted128x256 = kal128x256.EncryptString(data);
  const std::string encrypted256x256 = kal256x256.EncryptString(data);
  const std::string encrypted256x512 = kal256x512.EncryptString(data);
  const std::string encrypted512x512 = kal512x512.EncryptString(data);
  std::set<std::string> encrypted{
    encrypted128x128,
    encrypted128x256,
    encrypted256x256,
    encrypted256x512,
    encrypted512x512 };
  ASSERT_EQ(5, encrypted.size());
  const std::string decrypted128x128 = kal128x128.DecryptString(encrypted128x128);
  const std::string decrypted128x256 = kal128x256.DecryptString(encrypted128x256);
  const std::string decrypted256x256 = kal256x256.DecryptString(encrypted256x256);
  const std::string decrypted256x512 = kal256x512.DecryptString(encrypted256x512);
  const std::string decrypted512x512 = kal512x512.DecryptString(encrypted512x512);
  EXPECT_EQ(decrypted128x128, data);
  EXPECT_EQ(decrypted128x256, data);
  EXPECT_EQ(decrypted256x256, data);
  EXPECT_EQ(decrypted256x512, data);
  EXPECT_EQ(decrypted512x512, data);
  }