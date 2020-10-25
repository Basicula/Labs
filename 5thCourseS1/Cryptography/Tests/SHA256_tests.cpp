#include <SHA256.h>

#include <gtest/gtest.h>

// All test vectors took from https://www.di-mgt.com.au/sha_testvectors.html

TEST(SHA256, empty_string)
  {
  const std::string expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
  EXPECT_EQ(expected, SHA256()(""));
  }

TEST(SHA256, abc_test_vector)
  {
  const std::string expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
  EXPECT_EQ(expected, SHA256()("abc"));
  }

TEST(SHA256, big_test_vector)
  {
  const std::string text = "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu";
  const std::string expected = "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1";
  EXPECT_EQ(expected, SHA256()(text));
  }

TEST(SHA256, very_big_message)
  {
  const std::string text(1000000, 'a');
  const std::string expected = "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0";
  EXPECT_EQ(expected, SHA256()(text));
  }

TEST(SHA256, extremely_big_message)
  {
  std::string text;
  for (auto i = 0u; i < 16777216; ++i)
    text += "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno";
  const std::string expected = "50e72a0e26442fe2552dc3938ac58658228c0cbfb1d2ca872ae435266fcd055e";
  EXPECT_EQ(expected, SHA256()(text));
  }