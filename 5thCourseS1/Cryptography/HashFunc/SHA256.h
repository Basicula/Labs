#pragma once
#include "HashFuncBase.h"

class SHA256 : public HashfuncBase
  {
  public:
    virtual std::string operator()(std::string i_data) const override;
  };