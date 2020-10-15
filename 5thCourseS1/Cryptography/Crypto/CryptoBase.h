#pragma once

#include <filesystem>
#include <string>
#include <fstream>

class CryptoBase
  {
  public:
    virtual ~CryptoBase() = default;

    void SetKey(const std::string& i_key);

    void Encrypt(const std::filesystem::path& i_from, const std::filesystem::path& i_to) const;
    virtual std::string EncryptString(const std::string& i_data) const = 0;

    void Decrypt(const std::filesystem::path& i_from, const std::filesystem::path& i_to) const;
    virtual std::string DecryptString(const std::string& i_data) const = 0;

  protected:
    virtual void _ProcessNewKey() = 0;

    virtual void _Encrypt(std::ifstream& i_from, std::ofstream& i_to) const = 0;
    virtual void _Decrypt(std::ifstream& i_from, std::ofstream& i_to) const = 0;

  protected:
    std::string m_key;
  };