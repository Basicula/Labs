#pragma once
#include "BigInt.h"

class PrimeChecker
  {
  public:
    enum class Mode
      {
      BruteForce,
      MillerRabin
      };
  public:
    PrimeChecker(Mode i_mode = Mode::BruteForce);

    bool operator()(const bigint& i_number);
    bool IsPrime(const bigint& i_number);

  private:
    bool _BruteForce(const bigint& i_number);

    bool _MillerRabin(const bigint& i_number);
    bool _MillerRabinTest(const bigint& n, const bigint& d, const bigint& r);

  private:
    Mode m_mode;
  };