#include <AES.h>
#include <Kalyna.h>
#include <RC4.h>
#include <Salsa20.h>

#include <iostream>
#include <fstream>
#include <functional>
#include <chrono>
#include <map>

std::pair<double, std::string> map_time(double i_nanosec)
  {
  const std::vector<std::pair<double, std::string>> units
    {
    {3600e9,  "hours       "},
    {60e9,    "minutes     "},
    {1e9,     "seconds     "},
    {1e6,     "milliseconds"},
    {1e3,     "microseconds"},
    };
  std::pair<double, std::string> result{ i_nanosec, "nanoseconds " };
  for (const auto& unit : units)
    if (result.first > unit.first)
      {
      result.first /= unit.first;
      result.second = unit.second;
      break;
      }
  return result;

  }

std::pair<double, std::string> func_time(std::function<void()> i_func)
  {
  auto start_time = std::chrono::system_clock::now();
  i_func();
  auto end_time = std::chrono::system_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();
  return map_time(static_cast<double>(elapsed));
  }

void compare_benchmark()
  {
  std::map<std::string, std::unique_ptr<CryptoBase>> enciphers;
  enciphers.emplace("AES_ECB_128     ", std::make_unique<AES>(AES::KeySize::AES128));
  enciphers.emplace("AES_ECB_192     ", std::make_unique<AES>(AES::KeySize::AES192));
  enciphers.emplace("AES_ECB_256     ", std::make_unique<AES>(AES::KeySize::AES256));
  enciphers.emplace("AES_CBC_128     ", std::make_unique<AES>(AES::KeySize::AES128, AES::Mode::CBC));
  enciphers.emplace("AES_CBC_192     ", std::make_unique<AES>(AES::KeySize::AES192, AES::Mode::CBC));
  enciphers.emplace("AES_CBC_256     ", std::make_unique<AES>(AES::KeySize::AES256, AES::Mode::CBC));
  enciphers.emplace("AES_CFB_128     ", std::make_unique<AES>(AES::KeySize::AES128, AES::Mode::CFB));
  enciphers.emplace("AES_CFB_192     ", std::make_unique<AES>(AES::KeySize::AES192, AES::Mode::CFB));
  enciphers.emplace("AES_CFB_256     ", std::make_unique<AES>(AES::KeySize::AES256, AES::Mode::CFB));
  enciphers.emplace("AES_OFB_128     ", std::make_unique<AES>(AES::KeySize::AES128, AES::Mode::OFB));
  enciphers.emplace("AES_OFB_192     ", std::make_unique<AES>(AES::KeySize::AES192, AES::Mode::OFB));
  enciphers.emplace("AES_OFB_256     ", std::make_unique<AES>(AES::KeySize::AES256, AES::Mode::OFB));
  enciphers.emplace("AES_CTR_128     ", std::make_unique<AES>(AES::KeySize::AES128, AES::Mode::CTR));
  enciphers.emplace("AES_CTR_192     ", std::make_unique<AES>(AES::KeySize::AES192, AES::Mode::CTR));
  enciphers.emplace("AES_CTR_256     ", std::make_unique<AES>(AES::KeySize::AES256, AES::Mode::CTR));
  enciphers.emplace("Kalyna_128x128  ", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128));
  enciphers.emplace("Kalyna_128x256  ", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256));
  enciphers.emplace("Kalyna_256x256  ", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256));
  enciphers.emplace("Kalyna_256x512  ", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512));
  enciphers.emplace("Kalyna_512x512  ", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock512, Kalyna::KeySize::kKey512));
  enciphers.emplace("RC4             ", std::make_unique<RC4>());
  enciphers.emplace("Salsa20_128     ", std::make_unique<Salsa20>(Salsa20::KeyLength::Key128));
  enciphers.emplace("Salsa20_256     ", std::make_unique<Salsa20>(Salsa20::KeyLength::Key256));

  const std::string key = "qwertyuioplkjhfm";
  for (auto& encipher : enciphers)
    encipher.second->SetKey(key);

  std::filesystem::path test_dir(TEST_FILES_DIR);
  std::ofstream results_stream(RESULTS_PATH);
  for (const auto& file : std::filesystem::directory_iterator(test_dir))
    {
    const auto original_file = file.path();
    auto file_name_to_print = original_file.stem().string();
    while (file_name_to_print.size() < 10)
      file_name_to_print += " ";
    auto encrypted_filename = original_file;
    encrypted_filename.replace_filename(original_file.stem().native() + L"_encoded.txt");
    auto decrypted_filename = original_file;
    decrypted_filename.replace_filename(original_file.stem().native() + L"_decoded.txt");

    for (const auto& encipher : enciphers)
      {
      std::cout << "Encipher: " << encipher.first << " file: " << file_name_to_print;
      results_stream << "Encipher: " << encipher.first << " file: " << file_name_to_print;

      auto time = func_time([&]() {encipher.second->Encrypt(file, encrypted_filename); });
      std::cout << std::fixed << std::setprecision(4) << "\t encrypted in " << time.first << " " << time.second;
      results_stream << std::fixed << std::setprecision(4) << "\t encrypted in " << time.first << " " << time.second;

      time = func_time([&]() {encipher.second->Decrypt(encrypted_filename, decrypted_filename); });
      std::cout << std::fixed << std::setprecision(4) << "\t decrypted in " << time.first << " " << time.second << std::endl;
      results_stream << std::fixed << std::setprecision(4) << "\t decrypted in " << time.first << " " << time.second << std::endl;

      std::filesystem::remove(encrypted_filename);
      std::filesystem::remove(decrypted_filename);
      }
    }
  }

int main()
  {
  compare_benchmark();
  return 0;
  }