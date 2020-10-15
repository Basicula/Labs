#include <RC4.h>

#include <gtest/gtest.h>

TEST(RC4, common_case)
  {
  RC4 rc4;
  rc4.SetKey("key");
  const std::string text = "testtext";
  const auto encrypted = rc4.EncryptString(text);
  const auto dectypted = rc4.DecryptString(encrypted);
  EXPECT_EQ(text, dectypted);
  }

TEST(RC4, empty_key)
  {
  RC4 rc4;
  EXPECT_THROW(rc4.SetKey(""), std::runtime_error);
  }

TEST(RC4, too_big_key)
  {
  RC4 rc4;
  std::string key257(257, '1');
  EXPECT_THROW(rc4.SetKey(key257), std::runtime_error);
  }