#include "common.h"

struct FileTester {
  std::fstream file;
  bool closed = false;
  int sender = 0;

  FileTester(const std::string& filename, int sender) : sender(sender) {
    file.open(filename, std::fstream::in | std::fstream::out);
    int temp = 0;
    file.seekp(0);
    file.write((char*)(&sender), sizeof(int));
    file.write((char*)(&temp), sizeof(int));
    file.flush();
    }

  void WriteData(const std::vector<uint8_t>& bytes) {
    if (closed) {
      return;
      }
    int other = 0;
    int prev = 0;
    do {
      file.seekg(0);
      file.read((char*)(&other), sizeof(int));
      file.read((char*)(&prev), sizeof(int));
      if (prev == -1) {
        closed = true;
        return;
        }
      } while (prev != 0);

      file.seekp(2 * sizeof(int));
      file.write((char*)(bytes.data()), bytes.size());
      int size = bytes.size();
      file.seekp(0);
      file.write((char*)(&sender), sizeof(int));
      file.write((char*)(&size), sizeof(int));
      file.flush();
    }

  void Close() {
    closed = true;
    int temp = -1;
    file.seekp(0);
    file.write((char*)(&sender), sizeof(int));
    file.write((char*)(&temp), sizeof(int));
    file.flush();
    }

  std::vector<uint8_t> ReadData() {
    if (closed) {
      return std::vector<uint8_t>();;
      }
    int size = 0;
    int other = 0;
    while (!size || other == sender) {
      file.flush();
      file.seekg(0);
      file.read((char*)(&other), sizeof(int));
      file.read((char*)(&size), sizeof(int));
      }
    if (size == -1) {
      closed = true;
      return std::vector<uint8_t>();
      }
    std::vector<uint8_t> data(size);
    file.seekg(sizeof(int) * 2);
    file.read((char*)(data.data()), size);

    int temp = 0;
    file.seekp(0);
    file.write((char*)(&sender), sizeof(int));
    file.write((char*)(&temp), sizeof(int));
    file.flush();

    return data;
    }

  void PrintStats() {
    std::vector<uint8_t> data(PACKET_SIZE);
    for (unsigned char& a : data) a = rand();

    {
    uint64_t repeats = 10;
    double total_latency = 0;
    std::cout << "Computing latency..." << std::endl;
    for (uint64_t k = 0; k < repeats; k++) {
      ResetTimer();
      WriteData(data);
      auto response = ReadData();
      total_latency += GetTime() / 2;
      }
    std::cout << total_latency / repeats << " s" << std::endl;
    }
    {
    ResetTimer();
    std::cout << "Computing throughput..." << std::endl;
    uint64_t blocks = 128;
    for (uint64_t k = 0; k < blocks * (1ull << 20u) / PACKET_SIZE; k++) {
      WriteData(data);
      auto response = ReadData();
      }
    double time = GetTime();
    double throughput = blocks / time * 2;
    std::cout << throughput << " MB/s" << std::endl;
    }
    {
    std::cout << "Computing capacity..." << std::endl;
    double max_throughput = 0;
    for (int kk = 0; kk < 16; kk++) {
      ResetTimer();
      uint64_t blocks = 16;
      for (uint64_t k = 0; k < 16 * (1ull << 20u) / PACKET_SIZE; k++) {
        WriteData(data);
        auto response = ReadData();
        }
      double throughput = blocks / GetTime() * 2;
      max_throughput = std::max(max_throughput, throughput);
      }
    std::cout << max_throughput << " MB/s" << std::endl;
    }
    }
  };

int main() {
   {
   std::ofstream f("file");
   std::vector<uint8_t> data(PACKET_SIZE);
   for (unsigned char& a : data) a = rand();
   f.write(reinterpret_cast<char*>(data.data()), data.size());
   }

   auto process_first = new FileTester("file", 0);
   auto process_second = new FileTester("file", 1);

   std::cout << "Benchmark for [File]" << std::endl;
   if (fork() == 0) {
     // child
     std::vector<uint8_t> data;
     do {
       data = process_second->ReadData();
       if (!data.empty()) {
         process_second->WriteData(data);
         }
       } while (!data.empty());
     }

   process_first->PrintStats();
   process_first->Close();

   delete process_first;
   delete process_second;
  }
