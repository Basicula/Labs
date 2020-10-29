#include <AES.h>
#include <Kalyna.h>
#include <RC4.h>
#include <Salsa20.h>

#include <SHA256.h>
#include <Kupyna.h>

#include <iostream>
#include <fstream>
#include <functional>
#include <chrono>
#include <map>
#include <set>

namespace
  {
  std::pair<double, std::string> map_time(double i_nanosec)
    {
    const std::vector<std::pair<double, std::string>> units
      {
      {3600e9,  "h "}, // hours
      {60e9,    "m "}, // minutes
      {1e9,     "s "}, // seconds
      {1e6,     "ms"}, // milliseconds
      {1e3,     "us"}, // microseconds
      {1,       "ns"}, // nanoseconds
      };
    std::pair<double, std::string> result{ i_nanosec, "ns" };
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

  std::string random_string()
    {
    const size_t length = rand() % 128;
    static const std::string symbols = "1234567890qwertyuiopasdfghjklzxcvbnm";
    std::string res;
    for (auto i = 0u; i < length; ++i)
      res += symbols[rand() % symbols.size()];
    return res;
    }
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
  std::cout << "Encipher         \tFile      \tEncrypted\tDecrypted" << std::endl;
  results_stream << "Encipher         \tFile      \tEncrypted\tDecrypted" << std::endl;

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
      std::cout << encipher.first << "\t" << file_name_to_print << "\t";
      results_stream << encipher.first << "\t" << file_name_to_print << "\t";

      std::cout << std::fixed;

      auto time = func_time([&]() {encipher.second->Encrypt(file, encrypted_filename); });
      std::cout << std::setprecision(4) << time.first << " " << time.second << "\t";
      results_stream << std::setprecision(4) << time.first << " " << time.second << "\t";

      time = func_time([&]() {encipher.second->Decrypt(encrypted_filename, decrypted_filename); });
      std::cout << std::setprecision(4) << time.first << " " << time.second << std::endl;
      results_stream << std::setprecision(4) << time.first << " " << time.second << std::endl;

      std::filesystem::remove(encrypted_filename);
      std::filesystem::remove(decrypted_filename);
      }
    }
  }

void hash_brute_force_attack()
  {
  std::map<std::string, std::unique_ptr<HashfuncBase>> hash_funcs;
  hash_funcs.emplace("SHA256   ", std::make_unique<SHA256>());
  hash_funcs.emplace("Kupyna256", std::make_unique<Kupyna>(Kupyna::HashSize::Kupyna256));
  hash_funcs.emplace("Kupyna512", std::make_unique<Kupyna>(Kupyna::HashSize::Kupyna512));

  struct CollisionResult
    {
    std::string text1;
    std::string text2;
    std::string hash;
    };

  const size_t max_prefix_len = 8;
  std::vector<std::map<std::string, CollisionResult>> results(max_prefix_len);

  size_t try_id = 0;
  const std::string start_text1("text1"), start_text2("text2");
  std::string text1, text2;
  size_t prefix_len = 1;
  for (auto& prefix_result : results)
    {
    while (prefix_result.size() < hash_funcs.size())
      {
      text1 = start_text1 + ":" + std::to_string(try_id);
      text2 = start_text2 + ":" + std::to_string(try_id);
      for (const auto& hash_func : hash_funcs)
        {
        const auto res1 = (*hash_func.second)(text1);
        const auto res2 = (*hash_func.second)(text2);
        if (res1.substr(0, prefix_len) == res2.substr(0, prefix_len))
          {
          std::cout << "Collision found for " << hash_func.first
            << " with prefix length " << prefix_len
            << " attempt " << try_id << std::endl;
          prefix_result.emplace(hash_func.first, CollisionResult{ text1, text2, res1 });
          }
        }
      ++try_id;
      }
    ++prefix_len;
    }
  prefix_len = 1;
  for (const auto& prefix_result : results)
    {
    std::cout << "\nResults for prefix length " << prefix_len++ << std::endl;
    for (const auto& hash_result : prefix_result)
      std::cout << hash_result.first << ":\n"
      << "\tText1 = \"" << hash_result.second.text1 << "\"\n"
      << "\tText2 = \"" << hash_result.second.text2 << "\"\n"
      << "\tHash  = \"" << hash_result.second.hash << "\"\n";
    }
  }

void hash_birthday_attack()
  {
  std::map<std::string, std::unique_ptr<HashfuncBase>> hash_funcs;
  hash_funcs.emplace("SHA256   ", std::make_unique<SHA256>());
  hash_funcs.emplace("Kupyna256", std::make_unique<Kupyna>(Kupyna::HashSize::Kupyna256));
  hash_funcs.emplace("Kupyna512", std::make_unique<Kupyna>(Kupyna::HashSize::Kupyna512));

  struct CollisionResult
    {
    std::string text1;
    std::string text2;
    std::string hash1;
    std::string hash2;
    size_t avarage_tries;
    };

  const size_t samples = 100;
  const size_t max_prefix_len = 8;
  std::vector<std::map<std::string, CollisionResult>> results(max_prefix_len);

  size_t prefix_len = 1;
  for (auto& prefix_result : results)
    {
    for (const auto& hash_func : hash_funcs)
      {
      std::map<std::string, std::pair<std::string, std::string>> prefixes;
      size_t sum_tries = 0;
      for (auto sample_id = 0u; sample_id < samples; ++sample_id)
        {
        size_t try_id = 0;
        const std::string start_text = random_string();
        while (true)
          {
          const auto text = start_text + ":" + std::to_string(try_id);
          const auto hash = (*hash_func.second)(text);
          const auto prefix = hash.substr(0, prefix_len);
          if (prefixes.find(prefix) != prefixes.end())
            {
            prefix_result.emplace(hash_func.first, CollisionResult{ text, prefixes[prefix].second, hash, prefixes[prefix].first, 0 });
            sum_tries += try_id;
            break;
            }
          prefixes.emplace(prefix, std::pair<std::string, std::string>{ hash, text });
          ++try_id;
          }
        prefixes.clear();
        }
      prefix_result[hash_func.first].avarage_tries = sum_tries / samples;
      }
    std::cout << "Prefix length " << prefix_len << " processed" << std::endl;
    ++prefix_len;
    }
  prefix_len = 1;
  for (const auto& prefix_result : results)
    {
    std::cout << "\nResults for prefix length " << prefix_len++ << std::endl;
    for (const auto& hash_result : prefix_result)
      std::cout << hash_result.first << ":\n"
      << "\tText1                                   = \"" << hash_result.second.text1 << "\"\n"
      << "\tText2                                   = \"" << hash_result.second.text2 << "\"\n"
      << "\tHash1                                   = \"" << hash_result.second.hash1 << "\"\n"
      << "\tHash2                                   = \"" << hash_result.second.hash2 << "\"\n"
      << "\tAvarage tries to get partial collision  = \"" << hash_result.second.avarage_tries << "\"\n";
    }
  }

int main()
  {
  //compare_benchmark();
  //hash_birthday_attack();
  return 0;
  }