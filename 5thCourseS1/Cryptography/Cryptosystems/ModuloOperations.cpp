#include "ModuloOperations.h"

namespace ModuloOperations
  {
  bigint gcd(const bigint& a, const bigint& b)
    {
    if (b == 0)
      return a;
    return gcd(b, a % b);
    }

  bigint gcd_extended(const bigint& a, const bigint& b, bigint& x, bigint& y)
    {
    if (a == 0)
      {
      x = 0;
      y = 1;
      return b;
      }

    bigint x1, y1;
    const auto gcd = gcd_extended(b % a, a, x1, y1);

    x = y1 - (b / a) * x1;
    y = x1;

    return gcd;
    }

  bigint inverse(const bigint& a, const bigint& n)
    {
    bigint x, y;
    gcd_extended(a, n, x, y);
    return (x % n + n) % n;
    }

  bigint pow(const bigint& x, const bigint& y, const bigint& n)
    {
    if (y < 2)
      return x % n;
    if (y % 2)
      return (pow(x, y - 1, n) * x) % n;
    const auto root = pow(x, y / 2, n);
    return (root * root) % n;
    }

  bigint pow(const bigint& x, const bigint& y)
    {
    if (y < 2)
      return x;
    if (y % 2)
      return pow(x, y - 1) * x;
    const auto root = pow(x, y / 2);
    return root * root;
    }
  }