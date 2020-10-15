#pragma once
#include "CryptoBase.h"

#include <vector>
#include <string>

class AES : public CryptoBase
  {
  public:
    enum class KeySize
      {
      AES128,
      AES192,
      AES256
      };

  public:
    AES(KeySize i_type = KeySize::AES128);

    virtual std::string EncryptString(const std::string& i_data) const override;
    virtual std::string DecryptString(const std::string& i_data) const override;

  private:
    virtual void _ProcessNewKey() override;

    virtual void _Encrypt(std::ifstream& i_from, std::ofstream& i_to) const override;
    void _EncryptBlock(std::vector<uint32_t>& io_block) const;

    virtual void _Decrypt(std::ifstream& i_from, std::ofstream& i_to) const override;
    void _DecryptBlock(std::vector<uint32_t>& io_block) const;

    std::vector<uint32_t> _Prepare(const std::string& i_data, size_t i_size) const;
    void _GenerateMultTable();

    void _KeyExpansion();

    void _AddRoundKey(std::vector<uint32_t>& i_state, size_t i_round_idx) const;
    void _SubBytes(std::vector<uint32_t>& i_state, bool i_inverted = false) const;
    void _ShiftRows(std::vector<uint32_t>& i_state, bool i_inverted = false) const;
    void _MixColumns(std::vector<uint32_t>& i_state, bool i_inverted = false) const;


  private:
    uint32_t m_nb = 4;
    uint32_t m_nk = 4;
    uint32_t m_nr = 10;

    KeySize m_type;
    std::vector<std::vector<uint8_t>> m_mult_table;
    std::vector<uint32_t> m_key_schedule;
  };