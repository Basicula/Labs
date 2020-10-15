#include <AES.h>
#include <Kalyna.h>
#include <RC4.h>

#include <iostream>
#include <fstream>
#include <functional>
#include <chrono>
#include <map>

std::pair<double, std::string> map_time(double i_nanosec)
  {
  const std::vector<std::pair<double, std::string>> units
    {
    {3600e9,  "hours"},
    {60e9,    "minutes"},
    {1e9,     "seconds"},
    {1e6,     "milliseconds"},
    {1e3,     "microseconds"},
    };
  std::pair<double, std::string> result{ i_nanosec, "nanoseconds" };
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
  enciphers.emplace("AES128", std::make_unique<AES>(AES::KeySize::AES128));
  enciphers.emplace("AES192", std::make_unique<AES>(AES::KeySize::AES192));
  enciphers.emplace("AES256", std::make_unique<AES>(AES::KeySize::AES256));
  enciphers.emplace("Kalyna128x128", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey128));
  enciphers.emplace("Kalyna128x256", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock128, Kalyna::KeySize::kKey256));
  enciphers.emplace("Kalyna256x256", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey256));
  enciphers.emplace("Kalyna256x512", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock256, Kalyna::KeySize::kKey512));
  enciphers.emplace("Kalyna512x512", std::make_unique<Kalyna>(Kalyna::BlockSize::kBlock512, Kalyna::KeySize::kKey512));


  const std::string key = "qwertyuioplkjhfm";
  for (auto& encipher : enciphers)
    encipher.second->SetKey(key);

  std::filesystem::path test_dir(TEST_FILES_DIR);
  std::ofstream results_stream(RESULTS_PATH);
  for (const auto& file : std::filesystem::directory_iterator(test_dir))
    {
    const auto original_file = file.path();
    auto encrypted_filename = original_file;
    encrypted_filename.replace_filename(original_file.stem().native() + L"_encoded.txt");
    auto decrypted_filename = original_file;
    decrypted_filename.replace_filename(original_file.stem().native() + L"_decoded.txt");
      
    for (const auto& encipher : enciphers)
      {
      std::cout << "Encipher: " << encipher.first << ", file: " << original_file.stem();
      results_stream << "Encipher: " << encipher.first << ", file: " << original_file.stem();

      auto time = func_time([&]() {encipher.second->Encrypt(file, encrypted_filename); });
      std::cout << " encrypted in " << time.first << " " << time.second;
      results_stream << " encrypted in " << time.first << " " << time.second;

      time = func_time([&]() {encipher.second->Decrypt(encrypted_filename, decrypted_filename); });
      results_stream << " decrypted in " << time.first << " " << time.second << std::endl;

      std::filesystem::remove(encrypted_filename);
      std::filesystem::remove(decrypted_filename);
      }
    }
  }

int main()
  {
  //compare_benchmark();

  std::string text = "qwertyuhbgvdsa";
  RC4 rc4;
  rc4.SetKey("key");
  auto enc = rc4.EncryptString(text);
  auto dec = rc4.DecryptString(enc);
  std::cout << text << " " << enc << " " << dec << std::endl;
  return 0;
  }