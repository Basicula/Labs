#pragma once
#include "BigInt.h"

#include <stdint.h>

namespace ModuloOperations
  {
  bigint gcd(const bigint& a, const bigint& b);
  bigint gcd_extended(const bigint& a, const bigint& b, bigint& x, bigint& y);
  bigint inverse(const bigint& a, const bigint& n);
  bigint pow(const bigint& x, const bigint& y, const bigint& n);
  bigint pow(const bigint& x, const bigint& y);
  }