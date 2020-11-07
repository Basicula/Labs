#include "PrimeChecker.h"
#include "ModuloOperations.h"

#include <algorithm>

PrimeChecker::PrimeChecker(Mode i_mode)
  : m_mode(i_mode)
  {
  }

bool PrimeChecker::operator()(const bigint& i_number)
  {
  return IsPrime(i_number);
  }

bool PrimeChecker::IsPrime(const bigint& i_number)
  {
  switch (m_mode)
    {
    case PrimeChecker::Mode::BruteForce:
      return _BruteForce(i_number);
    case PrimeChecker::Mode::MillerRabin:
      return _MillerRabin(i_number);
    default:
      return false;
    }
  }

bool PrimeChecker::_BruteForce(const bigint& i_number)
  {
  if (i_number < 2)
    return false;

  for (bigint i = 2; i < i_number/2; ++i)
    if (i_number % i == 0)
      return false;
  return true;
  }

bool PrimeChecker::_MillerRabin(const bigint& i_number)
  {
  if (i_number < 2 || i_number % 2 == 0)
    return false;

  if (i_number < 4)
    return true;

  auto d = i_number - 1;
  size_t r = 0;
  while (d % 2 == 0)
    {
    d /= 2;
    ++r;
    }

  for (auto k = 0; k < 10; ++k)
    if (!_MillerRabinTest(i_number, d, r))
      return false;

  return true;
  }

bool PrimeChecker::_MillerRabinTest(const bigint& n, const bigint& d, const bigint& r)
  {
  auto a = bigint::random(2, n - 2);
  auto x = ModuloOperations::pow(a, d, n);
  if (x == 1 || x == n - 1)
    return true;
  for (bigint i = 0; i < r - 1; ++i)
    {
    x = ModuloOperations::pow(x, 2, n);
    if (x == 1)
      return false;
    if (x == n - 1)
      return true;
    }
  return false;
  }
