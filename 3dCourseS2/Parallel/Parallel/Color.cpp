#include "Color.h"

Color::Color()
  : m_red(0)
  , m_green(0)
  , m_blue(0)
  {};

Color::Color(unsigned char i_red, unsigned char i_green, unsigned char i_blue)
  : m_red(i_red)
  , m_green(i_green)
  , m_blue(i_blue)
  {};

Color::Color(const Color& i_other)
  : m_red(i_other.m_red)
  , m_green(i_other.m_green)
  , m_blue(i_other.m_blue)
  {};

bool Color::operator==(const Color& i_other) const
  {
  return m_red == i_other.m_red && m_green == i_other.m_green && m_blue == i_other.m_blue;
  }

unsigned char* Color::RGB() const
  {
  return new unsigned char[3]{ m_red, m_green, m_blue };
  };

unsigned char* Color::BGR() const
  {
  return new unsigned char[3]{ m_blue, m_green, m_red };
  };

Color Color::operator*(double i_factor) const
  {
  return Color(m_red * i_factor, m_green * i_factor, m_blue * i_factor);
  }

Color Color::operator+(const Color & i_other) const
  {
  return Color(int(m_red)+int(i_other.m_red), int(m_green) + int(i_other.m_green), int(m_blue) + int(i_other.m_blue));
  }
