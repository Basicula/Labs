#pragma once
#include <string>

class HashfuncBase
  {
  public:
    virtual ~HashfuncBase() = default;

    virtual std::string operator()(std::string i_data) const = 0;
  };