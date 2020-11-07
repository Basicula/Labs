#include "BigInt.h"

#include <stdexcept>
#include <time.h>

bigint::bigint()
  : m_number("0")
  {
  }

bigint::bigint(const std::string& i_number)
  : m_number("")
  {
  if (_IsValid(i_number))
    m_number = i_number;
  else
    throw std::runtime_error(i_number + " can't be a number");
  }

bigint::bigint(const bigint& i_other)
  : m_number(i_other.m_number)
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
      res.m_number += rand() % 10 + '0';
    _RemoveLeadingZero(res.m_number);
    }
  return res;
  }

bigint bigint::random(const bigint& i_min, const bigint& i_max)
  {
  if (i_min > i_max)
    return bigint();
  return random(i_max - i_min) + i_min;
  }

bigint& bigint::operator=(const std::string& i_number)
  {
  if (_IsValid(i_number))
    m_number = i_number;
  else
    throw std::runtime_error(i_number + " can't be a number");
  return *this;
  }

bigint::operator bool() const
  {
  return m_number != "0";
  }

void bigint::operator++()
  {
  *this += 1;
  }

bigint bigint::operator-() const
  {
  if (m_number[0] == '-')
    return m_number.substr(1);
  else
    return ('-' + m_number);
  }

bool bigint::operator<(const bigint& i_other) const
  {
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    {
    if (m_number.size() < i_other.m_number.size())
      return true;
    if (m_number.size() > i_other.m_number.size())
      return false;
    return m_number < i_other.m_number;
    }
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    if (m_number.size() > i_other.m_number.size())
      return true;
    if (m_number.size() < i_other.m_number.size())
      return false;
    return m_number.substr(1) > i_other.m_number.substr(1);
    }
  else if (m_number[0] == '-')
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
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    {
    if (m_number.size() > i_other.m_number.size())
      return true;
    if (m_number.size() < i_other.m_number.size())
      return false;
    return m_number > i_other.m_number;
    }
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    if (m_number.size() < i_other.m_number.size())
      return true;
    if (m_number.size() > i_other.m_number.size())
      return false;
    return m_number.substr(1) < i_other.m_number.substr(1);
    }
  else if (m_number[0] == '-')
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
  return m_number == i_other.m_number;
  }

bool bigint::operator!=(const bigint& i_other) const
  {
  return m_number != i_other.m_number;
  }

bigint bigint::operator+(const bigint& i_other) const
  {
  std::string res(m_number);
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    _Sum(res, i_other.m_number);
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    res = res.substr(1);
    _Sum(res, i_other.m_number.substr(1));
    res = '-' + res;
    }
  else if (m_number[0] == '-')
    {
    res = i_other.m_number;
    if (_Sub(res, m_number.substr(1)))
      res = '-' + res;
    }
  else
    {
    if (_Sub(res, i_other.m_number.substr(1)))
      res = '-' + res;
    }
  return res;
  }

bigint& bigint::operator+=(const bigint& i_other)
  {
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    _Sum(m_number, i_other.m_number);
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    m_number = m_number.substr(1);
    _Sum(m_number, i_other.m_number.substr(1));
    m_number = '-' + m_number;
    }
  else if (m_number[0] == '-')
    {
    const auto temp = m_number.substr(1);
    m_number = i_other.m_number;
    if (_Sub(m_number, temp))
      m_number = '-' + m_number;
    }
  else
    {
    if (_Sub(m_number, i_other.m_number.substr(1)))
      m_number = '-' + m_number;
    }
  return *this;
  }

bigint bigint::operator-(const bigint& i_other) const
  {
  std::string res(m_number);
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    {
    if (_Sub(res, i_other.m_number))
      res = '-' + res;
    }
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    res = i_other.m_number.substr(1);
    if (_Sub(res, m_number.substr(1)))
      res = '-' + res;
    }
  else if (m_number[0] == '-')
    {
    res = i_other.m_number;
    _Sum(res, m_number.substr(1));
    res = '-' + res;
    }
  else
    _Sum(res, i_other.m_number.substr(1));
  return res;
  }

bigint& bigint::operator-=(const bigint& i_other)
  {
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    {
    if (_Sub(m_number, i_other.m_number))
      m_number = '-' + m_number;
    }
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    const auto temp = m_number.substr(1);
    m_number = i_other.m_number.substr(1);
    if (_Sub(m_number, temp))
      m_number = '-' + m_number;
    }
  else if (m_number[0] == '-')
    {
    const auto temp = m_number.substr(1);
    m_number = i_other.m_number;
    _Sum(m_number, temp);
    m_number = '-' + m_number;
    }
  else
    _Sum(m_number, i_other.m_number.substr(1));
  return *this;
  }

bigint bigint::operator*(const bigint& i_other) const
  {
  std::string res(m_number);
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    _Mult(res, i_other.m_number);
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    res = res.substr(1);
    _Mult(res, i_other.m_number.substr(1));
    }
  else if (m_number[0] == '-')
    {
    res = i_other.m_number;
    _Mult(res, m_number.substr(1));
    res = '-' + res;
    }
  else
    {
    _Mult(res, i_other.m_number.substr(1));
    res = '-' + res;
    }
  return res;
  }

bigint& bigint::operator*=(const bigint& i_other)
  {
  *this = *this * i_other;
  return *this;
  }

bigint bigint::operator/(const bigint& i_other) const
  {
  if (i_other == 0)
    throw std::logic_error("Division by zero");
  std::string res(m_number);
  std::string remainder;
  if (std::isdigit(m_number[0]) && std::isdigit(i_other.m_number[0]))
    {
    if (*this < i_other)
      return bigint();
    _Divide(res, remainder, i_other.m_number);
    }
  else if (m_number[0] == '-' && i_other.m_number[0] == '-')
    {
    if (*this > i_other)
      return bigint();
    res = res.substr(1);
    _Divide(res, remainder, i_other.m_number.substr(1));
    }
  else if (m_number[0] == '-')
    {
    if (-*this < i_other)
      return bigint();
    res = m_number.substr(1);
    _Divide(res, remainder, i_other.m_number);
    res = '-' + res;
    }
  else
    {
    if (*this < -i_other)
      return bigint();
    _Divide(res, remainder, i_other.m_number.substr(1));
    res = '-' + res;
    }
  return res;
  }

bigint& bigint::operator/=(const bigint& i_other)
  {
  *this = *this / i_other;
  return *this;
  }

bigint bigint::operator%(const bigint& i_other) const
  {
  if (*this < i_other)
    return *this;
  std::string temp(m_number);
  std::string remainder;
  _Divide(temp, remainder, i_other.m_number);
  return remainder;
  }

bigint& bigint::operator%=(const bigint& i_other)
  {
  *this = *this % i_other;
  return *this;
  }

std::string bigint::str() const
  {
  return m_number;
  }

bool bigint::_IsValid(const std::string& i_number)
  {
  for (size_t i = (i_number[0] == '-'); i < i_number.size(); ++i)
    if (!std::isdigit(i_number[i]))
      return false;
  return true;
  }

void bigint::_RemoveLeadingZero(std::string& io_res)
  {
  io_res = io_res.substr(std::min(io_res.size() - 1, io_res.find_first_not_of('0')));
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
  o_stream << i_number.m_number;
  return o_stream;
  }
