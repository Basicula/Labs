#include "AES.h"

#include <sstream>

namespace
  {
  std::vector<uint32_t> g_temp_block;

  std::vector<uint8_t> sbox = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    };

  std::vector<uint8_t> inv_sbox = {
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
      0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
      0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
      0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
      0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
      0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
      0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
      0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
      0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
      0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
      0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
      0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
      0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
      0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
      0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
      0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    };

  std::vector<uint8_t> rcon = { 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 };

  uint32_t sub_word(uint32_t i_word) {
    auto data = reinterpret_cast<uint8_t*>(&i_word);
    for (auto i = 0u; i < 4; ++i)
      data[i] = sbox[data[i]];
    return i_word;
    }

  uint32_t shift(uint32_t i_word, int i_offset, bool i_inverted = false) {
    uint32_t res;
    auto res_data = reinterpret_cast<uint8_t*>(&res);
    auto data = reinterpret_cast<uint8_t*>(&i_word);
    for (int i = 0; i < 4; ++i)
      res_data[i] = data[(i + (i_inverted ? -i_offset : i_offset)) % 4];
    return res;
    }

  uint8_t mult(uint8_t i_byte, int i_power) {
    if (i_power <= 0)
      return 0;
    if (i_power == 1)
      return i_byte;

    if (i_power == 2)
      return (i_byte << 1) ^ (((i_byte >> 7) & 1) * 0x1b);

    int near = 1;
    int n = i_power;
    while (n)
      {
      n = (n >> 1);
      near *= 2;
      }
    near /= 2;

    return (mult(mult(i_byte, near / 2), 2) ^ mult(i_byte, i_power - near)) % 0x100;
    }

  std::string state_to_str(const std::vector<uint32_t>& i_state)
    {
    std::stringstream ss;
    for (const auto& word : i_state)
      {
      auto bytes = reinterpret_cast<const uint8_t*>(&word);
      for (auto i = 0u; i < 4; ++i)
        ss << bytes[i];
      }
    return ss.str();
    }
  }

AES::AES(KeySize i_type, Mode i_mode)
  : m_nb(4)
  , m_mult_table(16, std::vector<uint8_t>(256))
  , m_type(i_type)
  , m_mode(i_mode)
  {
  switch (m_type)
    {
    case KeySize::AES128:
      m_nk = 4;
      m_nr = 10;
      break;
    case KeySize::AES192:
      m_nk = 6;
      m_nr = 12;
      break;
    case KeySize::AES256:
      m_nk = 8;
      m_nr = 14;
      break;
    default:
      static_assert("Bad key size");
      break;
    }
  _GenerateMultTable();
  }

std::string AES::EncryptString(const std::string& i_data) const
  {
  std::string res;

  std::vector<uint32_t> IV;
  _InitInitialVector(IV);

  for (size_t i = 0; i < i_data.size(); i += 16)
    {
    auto to = std::min(i_data.size(), i + 16);
    auto state = _Prepare(i_data.substr(i, to), 4);

    _EncryptBlock(state, IV);

    res += state_to_str(state);
    }

  return res;
  }

void AES::_Encrypt(std::ifstream& i_from, std::ofstream& i_to) const
  {
  std::vector<uint32_t> buffer(4);
  auto raw_data = reinterpret_cast<char*>(buffer.data());
  
  std::vector<uint32_t> IV;
  _InitInitialVector(IV);

  while (i_from.read(raw_data, 16))
    {
    _EncryptBlock(buffer, IV);
    i_to.write(raw_data, 16);
    }
  if (i_from.gcount() > 0)
    {
    _EncryptBlock(buffer, IV);
    i_to.write(raw_data, i_from.gcount());
    }
  }

void AES::_EncryptBlock(std::vector<uint32_t>& block) const
  {
  _AddRoundKey(block, 0);
  for (auto round_idx = 1u; round_idx < m_nr; ++round_idx)
    {
    _SubBytes(block);
    _ShiftRows(block);
    _MixColumns(block);
    _AddRoundKey(block, round_idx);
    }

  _SubBytes(block);
  _ShiftRows(block);
  _AddRoundKey(block, m_nr);
  }

void AES::_EncryptBlock(std::vector<uint32_t>& io_block, std::vector<uint32_t>& io_IV) const
  {
  switch (m_mode)
    {
    case AES::Mode::CBC:
      _ApplyIV(io_block, io_IV);
      _EncryptBlock(io_block);
      _UpdateIV(io_IV, io_block);
      break;
    case AES::Mode::CFB:
      _EncryptBlock(io_IV);
      _ApplyIV(io_block, io_IV);
      _UpdateIV(io_IV, io_block);
      break;
    case AES::Mode::OFB:
      _EncryptBlock(io_IV);
      _ApplyIV(io_block, io_IV);
      break;
    case AES::Mode::CTR:
      _EncryptBlock(io_IV);
      _ApplyIV(io_block, io_IV);
      _UpdateIV(io_IV, io_block);
      break;
    case AES::Mode::ECB:
    default:
      _EncryptBlock(io_block);
      break;
    }
  }

std::string AES::DecryptString(const std::string& i_data) const
  {
  std::string res;

  std::vector<uint32_t> IV;
  _InitInitialVector(IV);

  for (size_t i = 0; i < i_data.size(); i += 16)
    {
    auto to = std::min(i_data.size(), i + 16);
    auto state = _Prepare(i_data.substr(i, to), 4);

    _DecryptBlock(state, IV);

    res += state_to_str(state);
    }

  size_t null_cnt = 0;
  while (res[res.size() - null_cnt] == 0x00)
    ++null_cnt;
  res = res.substr(0, res.size() - null_cnt + 1);
  return res;
  }

void AES::_ProcessNewKey()
  {
  _KeyExpansion();
  }

void AES::_InitInitialVector(std::vector<uint32_t>& o_IV) const
  {
  uint32_t sum = 0;
  for (const auto& k : m_key_schedule)
    sum += k;
  srand(sum);
  o_IV.clear();
  o_IV.resize(m_nb);
  for (auto& v : o_IV)
    v = rand() % sum;
  }

void AES::_UpdateIV(std::vector<uint32_t>& o_IV, const std::vector<uint32_t>& i_block) const
  {
  switch (m_mode)
    {
    case AES::Mode::CBC:
    case AES::Mode::CFB:
    case AES::Mode::OFB:
      o_IV = i_block;
      break;
    case AES::Mode::CTR:
      for (auto i = 1u; i < o_IV.size(); ++i)
        {
        ++o_IV[i - 1];
        if (o_IV[i - 1] != 0)
          break;
        }
      break;
    case AES::Mode::ECB:
    default:
      break;
    }
  }

void AES::_ApplyIV(std::vector<uint32_t>& io_block, const std::vector<uint32_t>& i_IV) const
  {
  switch (m_mode)
    {
    case AES::Mode::CBC:
    case AES::Mode::CFB:
    case AES::Mode::OFB:
    case AES::Mode::CTR:
      for (auto i = 0u; i < io_block.size(); ++i)
        io_block[i] ^= i_IV[i];
      break;
    case AES::Mode::ECB:
    default:
      break;
    }
  }

void AES::_Decrypt(std::ifstream& i_from, std::ofstream& i_to) const
  {
  std::vector<uint32_t> buffer(4);
  auto raw_data = reinterpret_cast<char*>(buffer.data());
  
  std::vector<uint32_t> IV;
  _InitInitialVector(IV);

  while (i_from.read(raw_data, 16))
    {
    _DecryptBlock(buffer, IV);
    i_to.write(raw_data, 16);
    }

  if (i_from.gcount() > 0)
    {
    _DecryptBlock(buffer, IV);
    i_to.write(raw_data, i_from.gcount());
    }
  }

void AES::_DecryptBlock(std::vector<uint32_t>& io_block) const
  {
  _AddRoundKey(io_block, m_nr);
  for (auto round_idx = m_nr - 1; round_idx > 0; --round_idx)
    {
    _ShiftRows(io_block, true);
    _SubBytes(io_block, true);
    _AddRoundKey(io_block, round_idx);
    _MixColumns(io_block, true);
    }

  _ShiftRows(io_block, true);
  _SubBytes(io_block, true);
  _AddRoundKey(io_block, 0);
  }

void AES::_DecryptBlock(std::vector<uint32_t>& io_block, std::vector<uint32_t>& io_IV) const
  {
  g_temp_block.assign(io_block.begin(), io_block.end());
  switch (m_mode)
    {
    case AES::Mode::CBC:
      _DecryptBlock(io_block);
      _ApplyIV(io_block, io_IV);
      _UpdateIV(io_IV, g_temp_block);
      break;
    case AES::Mode::CFB:
      _EncryptBlock(io_IV);
      _ApplyIV(io_block, io_IV);
      _UpdateIV(io_IV, g_temp_block);
      break;
    case AES::Mode::OFB:
      _EncryptBlock(io_IV);
      _ApplyIV(io_block, io_IV);
      break;
    case AES::Mode::CTR:
      _EncryptBlock(io_IV);
      _ApplyIV(io_block, io_IV);
      _UpdateIV(io_IV, io_block);
      break;
    case AES::Mode::ECB:
    default:
      _DecryptBlock(io_block);
      break;
    }
  }

std::vector<uint32_t> AES::_Prepare(const std::string& i_data, size_t i_size) const
  {
  std::string temp = i_data;
  while (temp.size() < i_size * 4)
    temp.push_back(0x00);
  std::vector<uint32_t> res(i_size);
  for (auto i = 0u; i < i_size; ++i)
    for (auto j = 0u; j < 4; ++j)
      reinterpret_cast<uint8_t*>(&res[i])[j] = temp[i * 4ull + j];
  return res;
  }

void AES::_GenerateMultTable()
  {
  for (auto i = 0u; i < 16; ++i)
    for (auto byte = 0u; byte < 256; ++byte)
      m_mult_table[i][byte] = mult(static_cast<uint8_t>(byte), i);
  }

void AES::_KeyExpansion()
  {
  m_key_schedule.clear();
  auto key_prepared = _Prepare(m_key, m_nk);
  for (auto i = 0u; i < m_nb * (m_nr + 1); ++i)
    {
    if (i < m_nk)
      m_key_schedule.push_back(key_prepared[i]);
    else
      {
      auto temp = m_key_schedule[i - 1];
      if (i % m_nk == 0)
        {
        temp = sub_word(shift(temp, 1));
        reinterpret_cast<uint8_t*>(&temp)[0] ^= rcon[i / m_nk];
        }
      else if (m_nk > 6 && i % m_nk == 4)
        temp = sub_word(temp);
      temp ^= m_key_schedule[i - m_nk];
      m_key_schedule.push_back(temp);
      }
    }
  }

void AES::_AddRoundKey(std::vector<uint32_t>& i_state, size_t i_round_idx) const
  {
  for (auto i = 0u; i < i_state.size(); ++i)
    i_state[i] ^= m_key_schedule[i_round_idx * m_nb + i];
  }

void AES::_SubBytes(std::vector<uint32_t>& i_state, bool i_inverted) const
  {
  for (auto& word : i_state)
    {
    auto bytes = reinterpret_cast<uint8_t*>(&word);
    for (auto i = 0; i < 4; ++i)
      bytes[i] = (i_inverted ? inv_sbox[bytes[i]] : sbox[bytes[i]]);
    }
  }

void AES::_ShiftRows(std::vector<uint32_t>& i_state, bool i_inverted) const
  {
  for (auto i = 1u; i < i_state.size(); ++i)
    shift(i_state[i], i, i_inverted);
  }

void AES::_MixColumns(std::vector<uint32_t>& i_state, bool i_inverted) const
  {
  for (auto i = 0u; i < m_nb; ++i)
    {
    auto bytes = reinterpret_cast<uint8_t*>(&i_state[i]);
    const auto x0 = bytes[0];
    const auto x1 = bytes[1];
    const auto x2 = bytes[2];
    const auto x3 = bytes[3];
    if (!i_inverted)
      {
      bytes[0] = m_mult_table[2][x0] ^ m_mult_table[3][x1] ^ x2 ^ x3;
      bytes[1] = x0 ^ m_mult_table[2][x1] ^ m_mult_table[3][x2] ^ x3;
      bytes[2] = x0 ^ x1 ^ m_mult_table[2][x2] ^ m_mult_table[3][x3];
      bytes[3] = m_mult_table[3][x0] ^ x1 ^ x2 ^ m_mult_table[2][x3];
      }
    else
      {
      bytes[0] = m_mult_table[14][x0] ^ m_mult_table[11][x1] ^ m_mult_table[13][x2] ^ m_mult_table[9][x3];
      bytes[1] = m_mult_table[9][x0] ^ m_mult_table[14][x1] ^ m_mult_table[11][x2] ^ m_mult_table[13][x3];
      bytes[2] = m_mult_table[13][x0] ^ m_mult_table[9][x1] ^ m_mult_table[14][x2] ^ m_mult_table[11][x3];
      bytes[3] = m_mult_table[11][x0] ^ m_mult_table[13][x1] ^ m_mult_table[9][x2] ^ m_mult_table[14][x3];
      }
    }
  }