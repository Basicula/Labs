#pragma once
#include <CryptoBase.h>

class RC4 : public CryptoBase
  {
  public:
    RC4();

    virtual std::string EncryptString(const std::string& i_data) const override;
    virtual std::string DecryptString(const std::string& i_data) const override;

  private:
    virtual void _ProcessNewKey() override;

    std::string _Process(const std::string& i_data) const;
    void _Process(std::ifstream& i_from, std::ofstream& i_to) const;

    virtual void _Encrypt(std::ifstream& i_from, std::ofstream& i_to) const override;
    virtual void _Decrypt(std::ifstream& i_from, std::ofstream& i_to) const override;

  private:
    std::vector<uint8_t> m_s;
    std::vector<uint8_t> m_t;
  };