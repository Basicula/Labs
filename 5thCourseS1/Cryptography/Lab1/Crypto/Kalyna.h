#pragma once
#include "CryptoBase.h"

#include <filesystem>
#include <fstream>
#include <string>
#include <vector>

class Kalyna : public CryptoBase
  {
  public:
    enum class BlockSize
      {
      kBlock128,
      kBlock256,
      kBlock512
      };

    enum class KeySize
      {
      kKey128,
      kKey256,
      kKey512
      };

  public:
    Kalyna(BlockSize i_block_size, KeySize i_key_size);

    virtual std::string EncryptString(const std::string& i_data) const override;
    virtual std::string DecryptString(const std::string& i_data) const override;

  private:
    virtual void _ProcessNewKey() override;

    virtual void _Encrypt(std::ifstream& i_from, std::ofstream& i_to) const override;
    void _EncryptBlock(std::vector<uint64_t>& io_block) const;

    virtual void _Decrypt(std::ifstream& i_from, std::ofstream& i_to) const override;
    void _DecryptBlock(std::vector<uint64_t>& io_block) const;

    std::vector<uint64_t> _Prepare(const std::string& i_data, size_t i_size) const;
    void _KeyExpansion();

    void _EncipherRound(std::vector<uint64_t>& io_state) const;
    void _DecipherRound(std::vector<uint64_t>& io_state) const;

    void _SubBytes(std::vector<uint64_t>& io_state, bool i_inverted = false) const;
    void _ShiftRows(std::vector<uint64_t>& io_state, bool i_inverted = false) const;
    void _MixColumns(std::vector<uint64_t>& io_state, bool i_inverted = false) const;

    void _AddRoundKey(size_t i_round_idx, std::vector<uint64_t>& io_state) const;
    void _SubRoundKey(size_t i_round_idx, std::vector<uint64_t>& io_state) const;
    void _XorRoundKey(size_t i_round_idx, std::vector<uint64_t>& io_state) const;

    void _AddRoundKeyExpand(
      const std::vector<uint64_t>& i_values, 
      std::vector<uint64_t>& io_state);
    void _XorRoundKeyExpand(
      const std::vector<uint64_t>& i_values,
      std::vector<uint64_t>& io_state);
    void _ShiftLeft(std::vector<uint64_t>& io_state);
    void _RotateLeft(std::vector<uint64_t>& io_state);
    void _Rotate(std::vector<uint64_t>& io_state);

  private:
    BlockSize m_block_size;
    KeySize m_key_size;

    size_t m_nb;
    size_t m_nk;
    size_t m_nr;
    
    std::string m_key;

    std::vector<std::vector<uint64_t>> m_round_keys;
  };