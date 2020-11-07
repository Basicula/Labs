#include "RSA.h"
#include "PrimeChecker.h"
#include "ModuloOperations.h"

#include <algorithm>
#include <limits>
#include <time.h>
#include <iostream>

namespace
  {
  const size_t g_max_number = std::numeric_limits<int>::max();

  bigint get_prime_number(const bigint& i_prime_bit_size)
    {
    PrimeChecker checker(PrimeChecker::Mode::MillerRabin);
    bigint min = ModuloOperations::pow(2, i_prime_bit_size - 1);
    bigint max = ModuloOperations::pow(2, i_prime_bit_size);
    bigint prime = 1;
    while (!checker(prime))
      prime = bigint::random(min, max);
    return prime;
    }
  }

RSA::RSA(const bigint& i_prime_bit_size)
  : m_prime_bit_size(i_prime_bit_size)
  {
  _PrepareKeys();
  }

bigint RSA::Encrypt(const bigint& i_message) const
  {
  return ModuloOperations::pow(i_message, m_e, m_n);
  }

bigint RSA::Decrypt(const bigint& i_message) const
  {
  return ModuloOperations::pow(i_message, m_d, m_n);
  }

void RSA::_PrepareKeys()
  {
  m_p = get_prime_number(m_prime_bit_size);
  m_q = get_prime_number(m_prime_bit_size);
  m_n = m_p * m_q;
  m_ctf = (m_p - 1) * (m_q - 1) / ModuloOperations::gcd(m_p - 1, m_q - 1);
  m_e = bigint::random(3, m_ctf);
  while (ModuloOperations::gcd(m_e, m_ctf) != 1)
    ++m_e;//m_e = bigint::random(3, m_ctf); // to generate between [3, ctf] <=> [3, λ(n)]
  m_d = ModuloOperations::inverse(m_e, m_ctf);
  }

std::ostream& operator<<(std::ostream& o_stream, const RSA& i_rsa)
  {
  o_stream << "RSA state: " << std::endl
    << "\tfirst prime:    " << i_rsa.m_p << std::endl
    << "\tsecond prime:   " << i_rsa.m_q << std::endl
    << "\tprime product:  " << i_rsa.m_n << std::endl
    << "\tctf:            " << i_rsa.m_ctf << std::endl
    << "\tpublic key:     " << i_rsa.m_e << std::endl
    << "\tprivate key:    " << i_rsa.m_d;
  return o_stream;
  }
