#include <RC4.h>

#include <numeric>

RC4::RC4()
  : m_s(256)
  , m_t(256)
  {
  }

std::string RC4::EncryptString(const std::string& i_data) const
  {
  return _Process(i_data);
  }

std::string RC4::DecryptString(const std::string& i_data) const
  {
  return _Process(i_data);
  }

void RC4::_ProcessNewKey()
  {
  if (m_key.empty() || m_key == "" || m_key.size() >= 256)
    throw std::runtime_error("Wrong key length for RC4");

  std::iota(m_s.begin(), m_s.end(), static_cast<uint8_t>(0));
  size_t j = 0;
  for (auto i = 0u; i < 256; ++i)
    {
    j = (j + m_s[i] + m_key[i % m_key.size()]) % 256;
    std::swap(m_s[i], m_s[j]);
    }
  }

std::string RC4::_Process(const std::string& i_data) const
  {
  size_t i, j;
  i = j = 0;
  std::vector<uint8_t> temp_s(m_s);
  std::string res;
  res.resize(i_data.size());
  for (int k = 0; k < i_data.size(); ++k)
    {
    i = (i + 1) % 256;
    j = (j + temp_s[i]) % 256;
    std::swap(temp_s[i], temp_s[j]);
    res[k] = temp_s[(temp_s[i] + temp_s[j]) % 256] ^ i_data[k];
    }
  return res;
  }

void RC4::_Process(std::ifstream& i_from, std::ofstream& i_to) const
  {
  std::string buffer;
  buffer.resize(256);
  while (i_from.read(buffer.data(), buffer.size()))
    {
    buffer = _Process(buffer);
    i_to.write(buffer.data(), buffer.size());
    }
  if (i_from.gcount() > 0)
    {
    buffer = _Process(buffer);
    i_to.write(buffer.data(), buffer.size());
    }
  }

void RC4::_Encrypt(std::ifstream& i_from, std::ofstream& i_to) const
  {
  _Process(i_from, i_to);
  }

void RC4::_Decrypt(std::ifstream& i_from, std::ofstream& i_to) const
  {
  _Process(i_from, i_to);
  }

