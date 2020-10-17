#pragma once
#include <CryptoBase.h>

class Salsa20 : public CryptoBase
  {
  public:
    enum class KeyLength
      {
      Key128,
      Key256
      };

  public:
    Salsa20(KeyLength i_key_length = KeyLength::Key128);

    void SetNonce(uint64_t i_nonce);

    virtual std::string EncryptString(const std::string& i_data) const override;
    virtual std::string DecryptString(const std::string& i_data) const override;

  private:
    void _ProcessNewKey();

    void _ProcessBlock(uint32_t* i_block, size_t i_block_size, size_t i_stream_pos) const;
    std::string _Process(const std::string& i_data) const;
    void _Process(std::ifstream& i_from, std::ofstream& i_to) const;

    virtual void _Encrypt(std::ifstream& i_from, std::ofstream& i_to) const override;
    virtual void _Decrypt(std::ifstream& i_from, std::ofstream& i_to) const override;

  private:
    KeyLength m_key_length;

    uint32_t m_init_key[16];

    static const uint8_t mg_key16_const[16];
    static const uint8_t mg_key32_const[16];
    static const size_t mg_num_rounds;
  };