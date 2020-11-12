#pragma once
#include <vector>
#include <string>
#include <iostream>

class bigint
  {
  public:
    using BigNumber = std::vector<uint32_t>;

  public:
    bigint();
    bigint(const std::string& i_number);
    bigint(const bigint& i_other);
    bigint(bigint&& i_other);
    ~bigint() = default;

    static bigint random(const bigint& i_max = std::string("99999999999999999999999999999999"));
    static bigint random(const bigint& i_min, const bigint& i_max);

    bigint& operator=(const bigint& i_number);
    bigint& operator=(const std::string& i_number);
    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint& operator=(T i_number)
      {
      *this = bigint(std::to_string(i_number));
      return *this;
      }

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint(T i_number)
      : bigint(std::to_string(i_number))
      {
      }

    explicit operator bool() const;

    void operator++();
    bigint operator-() const;

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bool operator<(T i_other) const
      {
      return *this < bigint(i_other);
      }
    bool operator<(const bigint& i_other) const;

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bool operator<=(T i_other) const
      {
      return *this <= bigint(i_other);
      }
    bool operator<=(const bigint& i_other) const;

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bool operator>(T i_other) const
      {
      return *this > bigint(i_other);
      }
    bool operator>(const bigint& i_other) const;

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bool operator>=(T i_other) const
      {
      return *this >= bigint(i_other);
      }
    bool operator>=(const bigint& i_other) const;

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bool operator==(T i_other) const
      {
      return *this == bigint(i_other);
      }
    bool operator==(const bigint& i_other) const;

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bool operator!=(T i_other) const
      {
      return *this != bigint(i_other);
      }
    bool operator!=(const bigint& i_other) const;


    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint operator+(T i_other) const
      {
      return *this + bigint(i_other);
      }
    bigint operator+(const bigint& i_other) const;
    bigint& operator+=(const bigint& i_other);

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint operator-(T i_other) const
      {
      return *this - bigint(i_other);
      }
    bigint operator-(const bigint& i_other) const;
    bigint& operator-=(const bigint& i_other);

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint operator*(T i_other) const
      {
      return *this * bigint(i_other);
      }
    bigint operator*(const bigint& i_other) const;
    bigint& operator*=(const bigint& i_other);

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint operator/(T i_other) const
      {
      return *this / bigint(i_other);
      }
    bigint operator/(const bigint& i_other) const;
    bigint& operator/=(const bigint& i_other);

    template<class T, typename = typename std::enable_if<std::is_fundamental<T>::value>::type>
    bigint operator%(T i_other) const
      {
      return *this % bigint(i_other);
      }
    bigint operator%(const bigint& i_other) const;
    bigint& operator%=(const bigint& i_other);

    bigint operator^(const bigint& i_other) const;
    bigint operator^=(const bigint& i_other);

    std::string str() const;

    static bigint abs(const bigint& i_other);

    friend std::ostream& operator<<(std::ostream& o_stream, const bigint& i_number);

  private:
    static bool _IsValid(const std::string& i_number);

    // arithmetic operations on strings that represent numbers greater 0
    // io_res += i_add, i.e. 1241667234 += 12465323
    static void _Sum(std::string& io_res, const std::string& i_add);
    static void _Sum(BigNumber& io_res, const BigNumber& i_add);
    // return true if result is negative otherwise false
    // io_res -= i_sub, i.e. false 1245357452 -= 124, true 12412 -= 4531426542
    static bool _Sub(std::string& io_res, const std::string& i_sub);
    static bool _Sub(BigNumber& io_res, const BigNumber& i_sub);
    // io_res *= i_mult, i.e. 1244125 *= 512421
    static void _Mult(std::string& io_res, const std::string& i_mult);
    static void _Mult(BigNumber& io_res, const BigNumber& i_mult);
    // io_res /= i_div, i.e. 6524124 /= 1231
    static void _Divide(std::string& io_res, std::string& io_remainder, const std::string& i_div);
    static void _Divide(BigNumber& io_res, BigNumber& io_remainder, const BigNumber& i_div);
    static void _DivideBS(std::string& io_res, std::string& io_remainder, const std::string& i_div);

    static void _RemoveLeadingZero(std::string& io_res);
    static void _RemoveLeadingZero(BigNumber& io_res);

  private:
    static const uint32_t g_base;

    BigNumber m_number;
    bool m_negative;
  };