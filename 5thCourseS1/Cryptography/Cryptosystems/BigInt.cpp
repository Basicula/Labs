#include "BigInt.h"

#include <stdexcept>
#include <time.h>


const uint32_t bigint::g_base = std::numeric_limits<uint32_t>::max();

bigint::bigint()
  : m_number(1, 0)
  , m_negative(false)
  {
  }

bigint::bigint(const std::string& i_number)
  : m_number()
  , m_negative(false)
  {
  if (!_IsValid(i_number))
    throw std::runtime_error(i_number + " can't be a number");

  auto num_str = i_number;
  auto dot = num_str.find_first_of('.');
  num_str = num_str.substr(0, dot);

  m_negative = (num_str[0] == '-');
  m_number.push_back(0);
  const BigNumber ten(1, 10);
  BigNumber symb(1);
  for (size_t i = m_negative; i < num_str.size(); ++i)
    {
    _Mult(m_number, ten);
    const auto s = num_str[i] - '0';
    symb[0] = static_cast<uint32_t>(s);
    _Sum(m_number, symb);
    }
  }

bigint::bigint(const bigint& i_other)
  : m_number(i_other.m_number)
  , m_negative(i_other.m_negative)
  {
  }

bigint::bigint(bigint&& i_other)
  : m_number(std::move(i_other.m_number))
  , m_negative(i_other.m_negative)
  {
  }

bigint bigint::random(const bigint& i_max)
  {
  const auto size = rand() % i_max.m_number.size() + 1;
  bigint res = i_max;
  while (res >= i_max)
    {
    res.m_number.clear();
    for (auto i = 0; i < size; ++i)
      res.m_number.push_back(rand() % g_base);
    }
  return res;
  }

bigint bigint::random(const bigint& i_min, const bigint& i_max)
  {
  if (i_min > i_max)
    return bigint();
  return random(i_max - i_min) + i_min;
  }

bigint& bigint::operator=(const bigint& i_number)
  {
  m_number.clear();
  m_number.assign(i_number.m_number.begin(), i_number.m_number.end());
  m_negative = i_number.m_negative;
  return *this;
  }

bigint& bigint::operator=(const std::string& i_number)
  {
  if (!_IsValid(i_number))
    throw std::runtime_error(i_number + " can't be a number");
  m_number.clear();
  auto num_str = i_number;
  auto dot = num_str.find_first_of('.');
  num_str = num_str.substr(0, dot);

  m_negative = (num_str[0] == '-');
  m_number.push_back(0);
  const BigNumber ten(1, 10);
  BigNumber symb(1);
  for (size_t i = m_negative; i < num_str.size(); ++i)
    {
    _Mult(m_number, ten);
    const auto s = num_str[i] - '0';
    symb[0] = static_cast<uint32_t>(s);
    _Sum(m_number, symb);
    }
  return *this;
  }

bigint::operator bool() const
  {
  for (const auto& num : m_number)
    if (num)
      return true;
  return false;
  }

void bigint::operator++()
  {
  *this += 1;
  }

bigint bigint::operator-() const
  {
  bigint res(*this);
  res.m_negative = !res.m_negative;
  return res;
  }

bool bigint::operator<(const bigint& i_other) const
  {
  if (!m_negative && !i_other.m_negative)
    {
    if (m_number.size() < i_other.m_number.size())
      return true;
    if (m_number.size() > i_other.m_number.size())
      return false;
    for (auto i = 0u; i < m_number.size(); ++i)
      if (m_number[i] < i_other.m_number[i])
        return true;
      else if (m_number[i] > i_other.m_number[i])
        return false;
    return false;
    }
  else if (m_negative && i_other.m_negative)
    {
    if (m_number.size() > i_other.m_number.size())
      return true;
    if (m_number.size() < i_other.m_number.size())
      return false;
    for (auto i = 0u; i < m_number.size(); ++i)
      if (m_number[i] > i_other.m_number[i])
        return true;
      else if (m_number[i] < i_other.m_number[i])
        return false;
    return false;
    }
  else if (m_negative)
    return true;
  else
    return false;
  }

bool bigint::operator<=(const bigint& i_other) const
  {
  return !(*this > i_other);
  }

bool bigint::operator>(const bigint& i_other) const
  {
  if (!m_negative && !i_other.m_negative)
    {
    if (m_number.size() > i_other.m_number.size())
      return true;
    if (m_number.size() < i_other.m_number.size())
      return false;
    for (auto i = 0u; i < m_number.size(); ++i)
      if (m_number[i] > i_other.m_number[i])
        return true;
    return false;
    }
  else if (m_negative && i_other.m_negative)
    {
    if (m_number.size() < i_other.m_number.size())
      return true;
    if (m_number.size() > i_other.m_number.size())
      return false;
    for (auto i = 0u; i < m_number.size(); ++i)
      if (m_number[i] < i_other.m_number[i])
        return true;
    return false;
    }
  else if (m_negative)
    return false;
  else
    return true;
  }

bool bigint::operator>=(const bigint& i_other) const
  {
  return !(*this < i_other);
  }

bool bigint::operator==(const bigint& i_other) const
  {
  return (m_negative == i_other.m_negative && m_number == i_other.m_number);
  }

bool bigint::operator!=(const bigint& i_other) const
  {
  return (m_negative != i_other.m_negative || m_number != i_other.m_number);
  }

bigint bigint::operator+(const bigint& i_other) const
  {
  bigint res;
  res.m_number = m_number;
  if (m_negative == i_other.m_negative)
    {
    _Sum(res.m_number, i_other.m_number);
    res.m_negative = m_negative;
    }
  else
    res.m_negative = _Sub(res.m_number, i_other.m_number) ^ m_negative;
  return res;
  }

bigint& bigint::operator+=(const bigint& i_other)
  {
  if (m_negative == i_other.m_negative)
    _Sum(m_number, i_other.m_number);
  else
    m_negative = _Sub(m_number, i_other.m_number) ^ m_negative;
  return *this;
  }

bigint bigint::operator-(const bigint& i_other) const
  {
  bigint res;
  res.m_number = m_number;
  if (m_negative == i_other.m_negative)
    res.m_negative = _Sub(res.m_number, i_other.m_number) ^ m_negative;
  else
    {
    _Sum(res.m_number, i_other.m_number);
    res.m_negative = m_negative;
    }
  return res;
  }

bigint& bigint::operator-=(const bigint& i_other)
  {
  if (!m_negative && !i_other.m_negative)
    m_negative = _Sub(m_number, i_other.m_number);
  else if (m_negative && i_other.m_negative)
    m_negative = !_Sub(m_number, i_other.m_number);
  else if (m_negative)
    _Sum(m_number, i_other.m_number);
  else
    _Sum(m_number, i_other.m_number);
  return *this;
  }

bigint bigint::operator*(const bigint& i_other) const
  {
  bigint res;
  res.m_number = m_number;
  res.m_negative = m_negative ^ i_other.m_negative;
  _Mult(res.m_number, i_other.m_number);
  return res;
  }

bigint& bigint::operator*=(const bigint& i_other)
  {
  _Mult(m_number, i_other.m_number);
  m_negative ^= i_other.m_negative;
  return *this;
  }

bigint bigint::operator/(const bigint& i_other) const
  {
  if (i_other == 0)
    throw std::logic_error("Division by zero");
  if (abs(*this) < abs(i_other))
    return bigint();
  bigint res;
  res.m_number = m_number;
  BigNumber remainder;
  _Divide(res.m_number, remainder, i_other.m_number);
  res.m_negative = m_negative ^ i_other.m_negative;
  return res;
  }

bigint& bigint::operator/=(const bigint& i_other)
  {
  if (i_other == 0)
    throw std::logic_error("Division by zero");
  if (abs(*this) < abs(i_other))
    {
    m_number.clear();
    m_number.push_back(0);
    m_negative = false;
    }
  else
    {
    BigNumber remainder;
    _Divide(m_number, remainder, i_other.m_number);
    m_negative ^= i_other.m_negative;
    }
  return *this;
  }

bigint bigint::operator%(const bigint& i_other) const
  {
  if (i_other.m_negative)
    throw std::logic_error("Modulo base can't be negative");
  if (abs(*this) < i_other)
    return *this;
  BigNumber temp(m_number);
  bigint remainder;
  _Divide(temp, remainder.m_number, i_other.m_number);
  remainder.m_negative = m_negative;
  return remainder;
  }

bigint& bigint::operator%=(const bigint& i_other)
  {
  if (i_other.m_negative)
    throw std::logic_error("Modulo base can't be negative");
  if (abs(*this) < i_other)
    return *this;
  BigNumber temp(m_number);
  _Divide(temp, m_number, i_other.m_number);
  return *this;
  }

bigint bigint::operator^(const bigint& i_other) const
  {
  bigint res(*this);
  for (auto i = 0; i < res.m_number.size(); ++i)
    res.m_number[i] ^= i_other.m_number[i];
  return res;
  }

bigint bigint::operator^=(const bigint& i_other)
  {
  for (auto i = 0; i < m_number.size(); ++i)
    m_number[i] ^= i_other.m_number[i];
  return *this;
  }

std::string bigint::str() const
  {
  const std::string base = std::to_string(g_base);
  std::string mult = "1";
  std::string res = "0";
  std::string temp;
  for (int64_t i = m_number.size() - 1; i >= 0; --i)
    {
    temp = std::to_string(m_number[i]);
    _Mult(temp, mult);
    _Sum(res, temp);
    _Mult(mult, base);
    }
  if (m_negative)
    res = '-' + res;
  return res;
  }

bigint bigint::abs(const bigint& i_other)
  {
  bigint res(i_other);
  res.m_negative = false;
  return res;
  }

bool bigint::_IsValid(const std::string& i_number)
  {
  size_t dots = 0;
  for (size_t i = (i_number[0] == '-'); i < i_number.size(); ++i)
    if (i_number[i] == '.')
      ++dots;
    else if (!std::isdigit(i_number[i]))
      return false;
  if (dots > 1)
    return false;
  return true;
  }

void bigint::_RemoveLeadingZero(std::string& io_res)
  {
  io_res = io_res.substr(std::min(io_res.size() - 1, io_res.find_first_not_of('0')));
  }

void bigint::_RemoveLeadingZero(BigNumber& io_res)
  {
  auto it = io_res.begin();
  for (; it != io_res.end(); ++it)
    if (*it != 0)
      break;
  if (it == io_res.end())
    io_res.erase(io_res.begin(), io_res.end() - 1);
  else
    io_res.erase(io_res.begin(), it);
  }

void bigint::_Sum(std::string& io_res, const std::string& i_add)
  {
  std::reverse(io_res.begin(), io_res.end());
  while (io_res.size() < i_add.size())
    io_res += '0';
  io_res += '0';
  std::reverse(io_res.begin(), io_res.end());
  for (auto i = 0; i < io_res.size(); ++i)
    {
    const auto res_id = static_cast<int64_t>(io_res.size()) - i - 1;
    const auto add_id = static_cast<int64_t>(i_add.size()) - i - 1;
    if (add_id >= 0)
      {
      auto res = io_res[res_id] + i_add[add_id] - 2 * '0';
      io_res[res_id] = res % 10 + '0';
      if (res >= 10)
        ++io_res[res_id - 1];
      }
    else
      {
      auto res = io_res[res_id] - '0';
      io_res[res_id] = res % 10 + '0';
      if (res >= 10)
        ++io_res[res_id - 1];
      else
        break;
      }
    }
  _RemoveLeadingZero(io_res);
  }

void bigint::_Sum(BigNumber& io_res, const BigNumber& i_add)
  {
  std::reverse(io_res.begin(), io_res.end());
  while (io_res.size() < i_add.size())
    io_res.push_back(0);
  io_res.push_back(0);
  std::reverse(io_res.begin(), io_res.end());
  uint64_t carry = 0;
  for (auto i = 0; i < i_add.size() || carry; ++i)
    {
    const auto res_id = static_cast<int64_t>(io_res.size()) - i - 1;
    const auto add_id = static_cast<int64_t>(i_add.size()) - i - 1;
    auto res = carry + io_res[res_id];
    if (add_id >= 0)
      res += i_add[add_id];
    carry = 0;
    if (res >= g_base)
      {
      carry = 1;
      res -= g_base;
      }
    io_res[res_id] = static_cast<uint32_t>(res);
    }
  _RemoveLeadingZero(io_res);
  }

bool bigint::_Sub(std::string& io_res, const std::string& i_sub)
  {
  auto sub = i_sub;
  bool is_negative = (io_res.size() < i_sub.size() || (io_res.size() == i_sub.size() && io_res < i_sub));
  if (is_negative)
    std::swap(io_res, sub);
  for (auto i = 0; i < io_res.size(); ++i)
    {
    const auto res_id = static_cast<int64_t>(io_res.size()) - i - 1;
    const auto add_id = static_cast<int64_t>(sub.size()) - i - 1;
    if (add_id >= 0)
      {
      char res = io_res[res_id] - sub[add_id];
      if (res < 0)
        {
        --io_res[res_id - 1];
        res += 10;
        }
      io_res[res_id] = res + '0';
      }
    else
      {
      auto res = io_res[res_id] - '0';
      if (res < 0)
        {
        --io_res[res_id - 1];
        io_res[res_id] += 10;
        }
      else
        break;
      }
    }
  _RemoveLeadingZero(io_res);
  return is_negative;
  }

bool bigint::_Sub(BigNumber& io_res, const BigNumber& i_sub)
  {
  bool is_negative = io_res.size() < i_sub.size();
  if (io_res.size() == i_sub.size())
    {
    for (auto i = 0; i < io_res.size(); ++i)
      if (io_res[i] == i_sub[i])
        continue;
      else
        {
        is_negative = io_res[i] < i_sub[i];
        break;
        }
    }

  std::reverse(io_res.begin(), io_res.end());
  while (io_res.size() < i_sub.size())
    io_res.push_back(0);
  std::reverse(io_res.begin(), io_res.end());

  int64_t carry = 0;
  for (auto i = 0; i < i_sub.size() || carry; ++i)
    {
    const auto res_id = static_cast<int64_t>(io_res.size()) - i - 1;
    const auto sub_id = static_cast<int64_t>(i_sub.size()) - i - 1;
    auto res = carry;
    res += is_negative ? -1 * static_cast<int64_t>(io_res[res_id]) : io_res[res_id];
    if (sub_id >= 0)
      res += is_negative ? i_sub[sub_id] : -1 * static_cast<int64_t>(i_sub[sub_id]);
    carry = 0;
    if (res < 0)
      {
      carry = -1;
      res += g_base;
      }
    io_res[res_id] = static_cast<uint32_t>(res);
    }
  _RemoveLeadingZero(io_res);
  return is_negative;
  }

void bigint::_Mult(std::string& io_res, const std::string& i_mult)
  {
  std::string sum_res;
  std::string extra_zeros;
  for (int64_t i = i_mult.size() - 1; i >= 0; --i)
    {
    std::string mult_res;
    char carry = 0;
    char mult = i_mult[i] - '0';
    for (int64_t j = io_res.size() - 1; j >= 0; --j)
      {
      char res = (io_res[j] - '0') * mult + carry;
      mult_res += res % 10 + '0';
      carry = res / 10;
      }
    if (carry)
      mult_res += std::to_string(carry);
    std::reverse(mult_res.begin(), mult_res.end());
    mult_res += extra_zeros;
    _Sum(sum_res, mult_res);
    extra_zeros += '0';
    }
  io_res = sum_res;
  }

void bigint::_Mult(BigNumber& io_res, const BigNumber& i_mult)
  {
  BigNumber sum_res((io_res.size() + 1) * (i_mult.size() + 1), 0);
  size_t extra_zeros = 0;
  for (int64_t i = i_mult.size() - 1; i >= 0; --i)
    {
    uint64_t carry = 0;
    uint64_t mult = i_mult[i];
    for (int64_t j = io_res.size() - 1; j >= 0 || carry; --j)
      {
      const auto id = sum_res.size() - extra_zeros - (io_res.size() - j - 1) - 1;
      auto temp = carry + sum_res[id];
      if (j >= 0)
        temp += io_res[j] * mult;
      sum_res[id] = temp % g_base;
      carry = temp / g_base;
      }
    ++extra_zeros;
    }
  _RemoveLeadingZero(sum_res);
  io_res = sum_res;
  }

void bigint::_Divide(std::string& io_res, std::string& io_remainder, const std::string& i_div)
  {
  std::string temp;
  std::string res;
  for (const auto& ch : io_res)
    {
    if (temp == "0")
      temp = "";
    temp += ch;
    char num = 0;
    while (temp.size() > i_div.size() || (temp >= i_div && temp.size() == i_div.size()))
      {
      _Sub(temp, i_div);
      ++num;
      }
    if (num > 0 || temp == "0")
      res += num + '0';
    else if (temp != "0")
      res += '0';
    }
  _RemoveLeadingZero(res);
  io_res = res;
  io_remainder = temp;
  }

void bigint::_Divide(BigNumber& io_res, BigNumber& io_remainder, const BigNumber& i_div)
  {
  io_remainder.clear();
  if (i_div.size() == 1)
    {
    uint64_t carry = 0;
    const auto& div = i_div[0];
    for (auto& n : io_res)
      {
      auto temp = carry * g_base + n;
      n = static_cast<uint32_t>(temp / div);
      carry = temp % div;
      }
    _RemoveLeadingZero(io_res);
    io_remainder.push_back(static_cast<uint32_t>(carry));
    return;
    }
  BigNumber temp;
  BigNumber res;
  BigNumber temp_res(1);
  for (const auto& n : io_res)
    {
    temp.push_back(n);
    if (!((temp.size() > i_div.size() || (temp[0] >= i_div[0] && temp.size() == i_div.size()))))
      continue;
    uint64_t divisor = static_cast<uint64_t>(i_div[0]) * g_base + i_div[1];
    const uint64_t divider = static_cast<uint64_t>(temp[0]) * g_base + temp[1];
    if (divider < divisor)
      divisor = static_cast<uint64_t>(i_div[0]);
    auto res_num = static_cast<uint32_t>(divider / divisor);
    temp_res.resize(1);
    temp_res[0] = res_num;
    _Mult(temp_res, i_div);
    while (!_Sub(temp_res, temp))
      {
      --res_num;
      temp_res.resize(1);
      temp_res[0] = res_num;
      _Mult(temp_res, i_div);
      }
    _RemoveLeadingZero(temp_res);
    temp = temp_res;
    res.push_back(res_num);
    }
  io_res = res;
  io_remainder = temp;
  }

void bigint::_DivideBS(std::string& io_res, std::string& io_remainder, const std::string& i_div)
  {
  std::string l("1"), r(io_res), mid;
  while (l != r)
    {
    mid = l;
    _Sum(mid, r);
    char carry = 0;
    for (auto i = 0; i < mid.size(); ++i)
      {
      char num = mid[i] - '0' + 10 * carry;
      mid[i] = num / 2 + '0';
      carry = num % 2;
      }
    _RemoveLeadingZero(mid);
    auto delta = mid;
    _Mult(delta, i_div);
    if (io_res == delta)
      {
      io_res = mid;
      return;
      }
    if (!_Sub(delta, io_res))
      r = mid;
    else if (!_Sub(delta, i_div))
      {
      l = mid;
      _Sum(l, "1");
      }
    else
      {
      io_res = mid;
      io_remainder = i_div;
      _Sub(io_remainder, delta);
      return;
      }
    }
  }

std::ostream& operator<<(std::ostream& o_stream, const bigint& i_number)
  {
  o_stream << i_number.str();
  return o_stream;
  }
