#include "SHA256.h"

#include <vector>
#include <iostream>

namespace
  {
  constexpr uint32_t k[64] =
    {
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
    };

  constexpr uint32_t init_h[8] =
    {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    };

  uint32_t rotr(uint32_t x, uint32_t n)
    {
    return (x >> n) | (x << (32 - n));
    }

  uint32_t sig0(uint32_t x)
    {
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3);
    }

  uint32_t sig1(uint32_t x)
    {
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10);
    }

  uint32_t majority(uint32_t a, uint32_t b, uint32_t c)
    {
    return (a & (b | c)) | (b & c);
    }

  uint32_t choose(uint32_t e, uint32_t f, uint32_t g)
    {
    return (e & f) ^ (~e & g);
    }

  void _Padding(std::string& i_data)
    {
    const auto bit_length = i_data.size() * 8;
    i_data.push_back(static_cast<char>(0x80));
    while (i_data.size() % 64 != 56)
      i_data.push_back(static_cast<char>(0x00));
    i_data.push_back(static_cast<char>(bit_length >> 56));
    i_data.push_back(static_cast<char>(bit_length >> 48));
    i_data.push_back(static_cast<char>(bit_length >> 40));
    i_data.push_back(static_cast<char>(bit_length >> 32));
    i_data.push_back(static_cast<char>(bit_length >> 24));
    i_data.push_back(static_cast<char>(bit_length >> 16));
    i_data.push_back(static_cast<char>(bit_length >> 8));
    i_data.push_back(static_cast<char>(bit_length >> 0));
    }

  void _ProcessBlock(const uint8_t* i_data, uint32_t io_state[8])
    {
    uint32_t words[64];
    for (size_t i = 0u, j = 0u; i < 16; ++i, j += 4)
      words[i] = (i_data[j] << 24) | (i_data[j + 1] << 16) | (i_data[j + 2] << 8) | (i_data[j + 3]);
    for (size_t i = 16; i < 64; ++i)
      words[i] = words[i - 16] + sig0(words[i - 15]) + words[i - 7] + sig1(words[i - 2]);

    uint32_t state[8];
    std::copy(io_state, io_state + 8, state);

    for (auto i = 0; i < 64; ++i)
      {
      const auto s0 = rotr(state[0], 2) ^ rotr(state[0], 13) ^ rotr(state[0], 22);
      const auto s1 = rotr(state[4], 6) ^ rotr(state[4], 11) ^ rotr(state[4], 25);
      const auto ch = choose(state[4], state[5], state[6]);
      const auto maj = (state[0] & state[1]) ^ (state[0] & state[2]) ^ (state[1] & state[2]);
      const auto temp1 = state[7] + s1 + ch + k[i] + words[i];
      const auto temp2 = s0 + maj;

      state[7] = state[6];
      state[6] = state[5];
      state[5] = state[4];
      state[4] = state[3] + temp1;
      state[3] = state[2];
      state[2] = state[1];
      state[1] = state[0];
      state[0] = temp1 + temp2;
      }

    for (size_t i = 0; i < 8; ++i)
      io_state[i] += state[i];
    }

  bool IsBigEndian()
    {
    int x = 1;
    auto raw_x = reinterpret_cast<uint8_t*>(&x);
    return (raw_x[0] == 0);
    }

  std::string byte_to_string(uint8_t i_byte)
    {
    std::string res;
    const auto a = i_byte / 16;
    const auto b = i_byte % 16;
    res += static_cast<char>(a < 10 ? int('0') + a : int('a') + a - 10);
    res += static_cast<char>(b < 10 ? int('0') + b : int('a') + b - 10);
    return res;
    }

  std::string to_hex_string(const uint32_t i_state[8])
    {
    std::string res;
    const bool big_endian = IsBigEndian();
    for (auto i = 0; i < 8; ++i)
      {
      auto bytes = reinterpret_cast<const uint8_t*>(&i_state[i]);
      if (!big_endian)
        for (int j = sizeof(uint32_t) - 1; j >= 0; --j)
          res += byte_to_string(bytes[j]);
      else
        for (auto j = 0u; j < sizeof(uint32_t); ++j)
          res += byte_to_string(bytes[j]);
      }
    return res;
    }
  }

std::string SHA256::operator()(std::string i_data) const
  {
  _Padding(i_data);
  uint32_t state[8];
  std::copy(init_h, init_h + 8, state);
  auto raw_data = reinterpret_cast<const uint8_t*>(i_data.c_str());
  for (size_t i = 0u; i + 64u <= i_data.size(); i += 64)
    _ProcessBlock(raw_data + i, state);
  return to_hex_string(state);
  }