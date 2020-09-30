#include "CryptoBase.h"

#include <fstream>

void CryptoBase::SetKey(const std::string& i_key)
  {
  if (m_key != i_key)
    {
    m_key = i_key;
    _ProcessNewKey();
    }
  }

void CryptoBase::Encrypt(const std::filesystem::path& i_from, const std::filesystem::path& i_to) const
  {
  std::ifstream from(i_from.native(), std::ios::binary);
  std::ofstream to(i_to.native(), std::ios::app | std::ios::binary);
  _Encrypt(from, to);
  }

void CryptoBase::Decrypt(const std::filesystem::path& i_from, const std::filesystem::path& i_to) const
  {
  std::ifstream from(i_from.native(), std::ios::binary);
  std::ofstream to(i_to.native(), std::ios::app | std::ios::binary);
  _Decrypt(from, to);
  }
