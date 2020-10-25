#pragma once
#include <string>

class SHA256
  {
  public:
    SHA256();

    std::string operator()(std::string i_data) const;
    std::string Hash(std::string i_data) const;
  };