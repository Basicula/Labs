#pragma once
#include "BigInt.h"

class RSA
  {
  public:
    RSA(const bigint& i_prime_bit_size = 64);

    bigint Encrypt(const bigint& i_message) const;
    bigint Decrypt(const bigint& i_message) const;

    friend std::ostream& operator<<(std::ostream& o_stream, const RSA& i_rsa);

  private:
    void _PrepareKeys();

  private:
    bigint m_prime_bit_size;
    bigint m_n;
    bigint m_e;
    bigint m_d;
    bigint m_p;
    bigint m_q;
    bigint m_ctf;
  };