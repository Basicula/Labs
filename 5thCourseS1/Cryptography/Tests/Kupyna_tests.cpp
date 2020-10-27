#include <Kupyna.h>

#include <gtest/gtest.h>

TEST(Kupyna256, empty_text)
  {
  Kupyna kup256(Kupyna::HashSize::Kupyna256);
  const std::string expected = "cd5101d1ccdf0d1d1f4ada56e888cd724ca1a0838a3521e7131d4fb78d0f5eb6";
  EXPECT_EQ(expected, kup256(""));
  }

TEST(Kupyna256, common_test)
  {
  Kupyna kup256(Kupyna::HashSize::Kupyna256);
  std::string text = "The quick brown fox jumps over the lazy dog";
  const std::string expected1 = "996899f2d7422ceaf552475036b2dc120607eff538abf2b8dff471a98a4740c6";
  EXPECT_EQ(expected1, kup256(text));
  text += '.';
  const std::string expected2 = "88ea8ce988fe67eb83968cdc0f6f3ca693baa502612086c0dcec761a98e2fb1f";
  EXPECT_EQ(expected2, kup256(text));
  }

TEST(Kupyna512, empty_string)
  {
  Kupyna kup256(Kupyna::HashSize::Kupyna512);
  const std::string expected =  "656b2f4cd71462388b64a37043ea55dbe445d452aecd46c3298343314ef04019"
                                "bcfa3f04265a9857f91be91fce197096187ceda78c9c1c021c294a0689198538";
  EXPECT_EQ(expected, kup256(""));
  }