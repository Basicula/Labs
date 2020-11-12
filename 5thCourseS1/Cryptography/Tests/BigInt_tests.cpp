#include <BigInt.h>

#include <gtest/gtest.h>

TEST(BigIntConstruction, empty_constructor)
  {
  bigint bi;
  EXPECT_EQ("0", bi.str());
  }

TEST(BigIntConstruction, string_constructor)
  {
  const std::string number("1234567875312456353561231242");
  bigint bi(number);
  EXPECT_EQ(number, bi.str());

  const std::string negative_number("-1234567875312456353561231242");
  bigint nbi(negative_number);
  EXPECT_EQ(negative_number, nbi.str());
  }

TEST(BigIntConstruction, int_constructor)
  {
  bigint bi(123);
  EXPECT_EQ("123", bi.str());

  bigint nbi(-321);
  EXPECT_EQ("-321", nbi.str());
  }

TEST(BigIntConstruction, float_constructor)
  {
  bigint bi(123.12431f);
  EXPECT_EQ("123", bi.str());

  bigint nbi(-321.15235f);
  EXPECT_EQ("-321", nbi.str());
  }

TEST(BigIntBoolOperations, bool_operations)
  {
  bigint a, b;

  a = 9;
  b = 123;
  EXPECT_TRUE(a < b);
  EXPECT_TRUE(b > a);
  EXPECT_TRUE(b != a);

  a = 123;
  b = 123;
  EXPECT_TRUE(a == b);
  }

TEST(BigIntAdding, common_cases)
  {
  bigint a, b, c;

  a = 321;
  b = 123;
  c = a + b;
  EXPECT_EQ("444", c.str());
  c = a;
  c += b;
  EXPECT_EQ("444", c.str());

  a = -321;
  b = -123;
  c = a + b;
  EXPECT_EQ("-444", c.str());
  c = a;
  c += b;
  EXPECT_EQ("-444", c.str());

  a = -321;
  b = 123;
  c = a + b;
  EXPECT_EQ("-198", c.str());
  c = b + a;
  EXPECT_EQ("-198", c.str());
  c = a;
  c += b;
  EXPECT_EQ("-198", c.str());
  c = b;
  c += a;
  EXPECT_EQ("-198", c.str());

  a = 999;
  b = 11;
  c = a + b;
  EXPECT_EQ("1010", c.str());
  }

TEST(BigIntSubtraction, common_cases)
  {
  bigint a, b, c;

  a = 321;
  b = 123;
  c = a - b;
  EXPECT_EQ("198", c.str());
  c = a;
  c -= b;
  EXPECT_EQ("198", c.str());
  c = b - a;
  EXPECT_EQ("-198", c.str());
  c = b;
  c -= a;
  EXPECT_EQ("-198", c.str());

  a = -321;
  b = 123;
  c = a - b;
  EXPECT_EQ("-444", c.str());
  c = a;
  c -= b;
  EXPECT_EQ("-444", c.str());
  c = b - a;
  EXPECT_EQ("444", c.str());
  c = b;
  c -= a;
  EXPECT_EQ("444", c.str());

  a = 10000;
  b = 1;
  c = a - b;
  EXPECT_EQ("9999", c.str());
  }

TEST(BigIntMultiply, mult_cases)
  {
  bigint a(123), b(3);
  auto c = a * b;
  EXPECT_EQ("369", c.str());

  a = -2;
  b = -3;
  c = a * b;
  EXPECT_EQ("6", c.str());

  a = -2;
  b = 3;
  c = a * b;
  EXPECT_EQ("-6", c.str());

  a = 2;
  b = -3;
  c = a * b;
  EXPECT_EQ("-6", c.str());

  a = "111111111111111111111111111111111111111";
  b = 9;
  c = a * b;
  EXPECT_EQ("999999999999999999999999999999999999999", c.str());

  a = "1234567890";
  b = "987654321";
  c = a * b;
  EXPECT_EQ("1219326311126352690", c.str());
  }

TEST(BigIntDivide, divide_cases)
  {
  bigint a, b, c;

  a = 4;
  b = 2;
  c = a / b;
  EXPECT_EQ("2", c.str());
  c = b / a;
  EXPECT_EQ("0", c.str());

  a = -4;
  b = 2;
  c = a / b;
  EXPECT_EQ("-2", c.str());
  c = b / a;
  EXPECT_EQ("0", c.str());

  a = 4;
  b = -2;
  c = a / b;
  EXPECT_EQ("-2", c.str());
  c = b / a;
  EXPECT_EQ("0", c.str());

  a = -4;
  b = -2;
  c = a / b;
  EXPECT_EQ("2", c.str());
  c = b / a;
  EXPECT_EQ("0", c.str());

  a = 12526;
  b = 1;
  c = a / b;
  EXPECT_EQ("12526", c.str());

  a = -12526;
  b = 1;
  c = a / b;
  EXPECT_EQ("-12526", c.str());

  a = 12526;
  b = -1;
  c = a / b;
  EXPECT_EQ("-12526", c.str());

  a = -12526;
  b = -1;
  c = a / b;
  EXPECT_EQ("12526", c.str());

  a = "222222222222222222222222222";
  b = 2;
  c = a / b;
  EXPECT_EQ("111111111111111111111111111", c.str());
  c = b / a;
  EXPECT_EQ("0", c.str());

  a = 2 * 3 * 5 * 7 * 11 * 13 * 17;
  b = 11;
  c = 2 * 3 * 5 * 7 * 13 * 17;
  EXPECT_EQ(c, a / b);

  a = "246913579975308643";
  b = "123456789987654321";
  c = a / b;
  EXPECT_EQ("2", c.str());
  c = a % b;
  EXPECT_EQ("1", c.str());
  EXPECT_EQ(a, b * (a / b) + a % b);

  a = "1524157887334247844875781101930955772112635270";
  b = "12345678900987654321";
  c = a / b;
  EXPECT_EQ("123456789987654321123456789", c.str());
  c = a % b;
  EXPECT_EQ("1", c.str());
  EXPECT_EQ(a, b * (a / b) + a % b);

  a = "123";
  b = "1";
  c = a % b;
  EXPECT_EQ("0", c.str());

  a = 23;
  b = 2;
  EXPECT_TRUE(a % b);

  a = 22;
  b = 2;
  EXPECT_FALSE(a % b);
  }