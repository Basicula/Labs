#include "Salsa20.h"

namespace
  {
  constexpr uint32_t g_max_uint32_t = std::numeric_limits<uint32_t>::max();

  uint32_t rotate(uint32_t a, uint32_t b)
    {
    return ((a << b) | (a >> (32 - b)));
    }

  void quater_round(uint32_t& a, uint32_t& b, uint32_t& c, uint32_t& d)
    {
    b ^= rotate(a + d, 7);
    c ^= rotate(b + a, 9);
    d ^= rotate(c + b, 13);
    a ^= rotate(d + c, 18);
    }

  uint32_t uint8_to_uint32(const uint8_t* i_bytes)
    {
    return ((static_cast<uint32_t>(i_bytes[0]) << 0) |
      (static_cast<uint32_t>(i_bytes[1]) << 8) |
      (static_cast<uint32_t>(i_bytes[2]) << 16) |
      (static_cast<uint32_t>(i_bytes[3]) << 24));
    }
  }

const uint8_t Salsa20::mg_key16_const[16] = { 'e','x','p','a','n','d',' ','1','6','-','b','y','t','e',' ','k' };
const uint8_t Salsa20::mg_key32_const[16] = { 'e','x','p','a','n','d',' ','3','2','-','b','y','t','e',' ','k' };
const size_t Salsa20::mg_num_rounds = 20;

Salsa20::Salsa20(KeyLength i_key_length)
  : m_key_length(i_key_length)
  , m_init_key()
  {
  }

void Salsa20::SetNonce(uint64_t i_nonce)
  {
  auto raw_nonce = reinterpret_cast<uint32_t*>(&i_nonce);
  m_init_key[6] = raw_nonce[0];
  m_init_key[7] = raw_nonce[1];
  }

std::string Salsa20::EncryptString(const std::string& i_data) const
  {
  return _Process(i_data);
  }

std::string Salsa20::DecryptString(const std::string& i_data) const
  {
  return _Process(i_data);
  }

void Salsa20::_ProcessNewKey()
  {
  std::string temp_key(m_key);
  while (temp_key.size() < 32)
    temp_key.push_back(0x00);
  switch (m_key_length)
    {
    case Salsa20::KeyLength::Key256:
      temp_key = temp_key.substr(0, 32);
      break;
    case Salsa20::KeyLength::Key128:
    default:
      temp_key = temp_key.substr(0, 16);
      break;
    }
  const auto& constant = (m_key_length == KeyLength::Key128 ? mg_key16_const : mg_key32_const);
  const auto& key = reinterpret_cast<const uint8_t*>(temp_key.data());
  auto init_key_bytes = reinterpret_cast<uint8_t*>(m_init_key);
  std::copy(constant, constant + 4, &init_key_bytes[0]);
  std::copy(key, key + 16, &init_key_bytes[4]);
  std::copy(constant + 4, constant + 8, &init_key_bytes[20]);
  std::copy(constant + 8, constant + 12, &init_key_bytes[40]);
  std::copy(key + 16, key + 32, &init_key_bytes[44]);
  std::copy(constant + 12, constant + 16, &init_key_bytes[60]);
  }

void Salsa20::_ProcessBlock(uint32_t* io_block, size_t i_block_size, size_t i_stream_pos) const
  {
  uint32_t x[16];
  std::copy(m_init_key, m_init_key + 16, x);
  x[8] = static_cast<uint32_t>(i_stream_pos % g_max_uint32_t);
  x[9] = static_cast<uint32_t>(i_stream_pos / g_max_uint32_t);
  for (size_t i = 0; i < mg_num_rounds; ++i)
    {
    quater_round(x[0], x[4], x[8], x[12]);
    quater_round(x[5], x[9], x[13], x[1]);
    quater_round(x[10], x[14], x[2], x[6]);
    quater_round(x[15], x[3], x[7], x[11]);

    quater_round(x[0], x[1], x[2], x[3]);
    quater_round(x[5], x[6], x[7], x[4]);
    quater_round(x[10], x[11], x[8], x[9]);
    quater_round(x[15], x[12], x[13], x[14]);
    }
  for (auto i = 0; i < 16; ++i)
    x[i] += m_init_key[i];
  for (auto i = 0; i < i_block_size; ++i)
    io_block[i] ^= x[i];
  }

std::string Salsa20::_Process(const std::string& i_data) const
  {
  std::string res(i_data);
  auto raw_data = reinterpret_cast<uint32_t*>(res.data());
  const auto size_in_words = (res.size() + 3) / 4;
  const auto num_blocks = (size_in_words + 15) / 16;
  for (size_t i = 0; i < num_blocks; ++i)
    _ProcessBlock(raw_data + i * 16, std::min(size_in_words - i * 16, static_cast<size_t>(16)), i);
  return res;
  }

void Salsa20::_Process(std::ifstream& i_from, std::ofstream& i_to) const
  {
  std::vector<uint32_t> buffer(16);
  auto raw_data = reinterpret_cast<char*>(buffer.data());
  size_t stream_pos = 0;
  while (i_from.read(raw_data, 64))
    {
    _ProcessBlock(buffer.data(), 16, stream_pos++);
    i_to.write(raw_data, 64);
    }
  if (i_from.gcount() > 0)
    {
    _ProcessBlock(buffer.data(), i_from.gcount(), stream_pos);
    i_to.write(raw_data, i_from.gcount());
    }
  }

void Salsa20::_Encrypt(std::ifstream& i_from, std::ofstream& i_to) const
  {
  _Process(i_from, i_to);
  }

void Salsa20::_Decrypt(std::ifstream& i_from, std::ofstream& i_to) const
  {
  _Process(i_from, i_to);
  }

