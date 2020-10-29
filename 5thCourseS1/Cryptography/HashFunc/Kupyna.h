#pragma once
#include "HashFuncBase.h"

class Kupyna : public HashfuncBase
  {
  public:
    enum class HashSize
      {
      Kupyna256,
      Kupyna512
      };

  public:
    Kupyna(HashSize i_size = HashSize::Kupyna256);

    virtual std::string operator()(std::string i_data) const override;

  private:
    void _Padding(std::string& io_data) const;
    void _Digest(const uint8_t* ip_data, size_t i_data_size, uint8_t* iop_state) const;
    void _ApplyRounds(uint8_t* iop_state, bool i_p_or_q) const;

    void _AddRoundConstant(uint8_t* iop_state, int i_round, bool i_p_or_q) const;
    void _SubBytes(uint8_t* iop_state) const;
    void _ShiftBytes(uint8_t* iop_state) const;
    void _MixColumns(uint8_t* iop_state) const;

    std::string _StateToHash(uint8_t* iop_state) const;

  private:
    static const uint8_t m_rows = 8;

    HashSize m_size;
    uint8_t m_nb;
    uint8_t m_nr;
    uint8_t m_block_size;
    uint8_t m_hash_size;
  };