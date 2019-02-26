#include <iostream>
#include <mutex>
#include <thread>
#include <vector>
#include <string>

const std::vector<std::string> philosofers_data_base = { "Парменид","Аристотель","Марк Аврелий","Ансельм Кентерберийский","Бенедикт Спиноза","Артур Шопенгауэр","Фридрих Ницше","Роман Ингарден","Жан-Поль Сартр","Морис Мерло-Понти" };
std::mutex console_mutex;
const size_t max_time_for_eating = 15;

class Philosopher
  {
  public:
    enum PhilosopherState
      {
      THINKING,
      WAITING_FORK,
      HAS_LEFT_FORK,
      HAS_RIGHT_FORK,
      HAS_TWO_FORKS,
      EATING,
      };

  public:
    Philosopher(const std::string& i_name);

    void GetFork(bool i_is_left);
    void PutFork(bool i_is_left);

    inline void Eat() { m_state = EATING; };
    inline void StopEat() { m_state = HAS_TWO_FORKS; };
    inline PhilosopherState GetState() const { return m_state; };
    inline std::string GetName() const { return m_name; };

  private:
    std::string m_name;
    PhilosopherState m_state;
    bool m_left_fork;
    bool m_right_fork;
  };

Philosopher::Philosopher(const std::string& i_name)
  : m_name(i_name)
  , m_state(THINKING)
  , m_left_fork(false)
  , m_right_fork(false)
  {}

void Philosopher::GetFork(bool i_is_left)
  {
  m_left_fork |= i_is_left;
  m_right_fork |= !i_is_left;
  if (m_left_fork && m_right_fork)
    m_state = HAS_TWO_FORKS;
  else if (m_left_fork)
    m_state = HAS_LEFT_FORK;
  else
    m_state = HAS_RIGHT_FORK;
  std::lock_guard<std::mutex> console_lock(console_mutex);
  std::cout << m_name << " says: I've got a fork" << std::endl;
  }

void Philosopher::PutFork(bool i_is_left)
  {
  m_left_fork &= !i_is_left;
  m_right_fork &= !i_is_left;
  if (m_left_fork)
    m_state = HAS_LEFT_FORK;
  else if (m_right_fork)
    m_state = HAS_RIGHT_FORK;
  else
    m_state = THINKING;
  std::lock_guard<std::mutex> console_lock(console_mutex);
  std::cout << m_name << " says: I've put a fork" << std::endl;
  }

class Semaphore
  {
  public:
    Semaphore(size_t i_size);
    void Simulate();

  private:
    void _WatchPhilosopher(size_t i_philosopher);
    void _PrintInfo();
    void _UpdateInfo();

  private:
    size_t m_time;
    size_t m_size;
    size_t m_used_forks;
    std::vector<Philosopher> m_philosophers;
    std::mutex* m_forks;
    std::vector<size_t> m_eating_times;
  };

Semaphore::Semaphore(size_t i_size)
  : m_time(0)
  , m_size(i_size)
  , m_used_forks(0)
  , m_forks(new std::mutex[i_size])
  , m_eating_times(i_size)
  {
  srand(static_cast<unsigned int>(time(NULL)));
  for (size_t i = 0; i < m_size; ++i)
    m_philosophers.emplace_back(philosofers_data_base[i]);
  }

void Semaphore::_PrintInfo()
  {
  for (size_t i = 0; i < m_size; ++i)
    {
    switch (m_philosophers[i].GetState())
      {
      case Philosopher::THINKING:
        std::cout << m_philosophers[i].GetName() << " is thinking..." << std::endl;
        break;
      case Philosopher::WAITING_FORK:
        std::cout << m_philosophers[i].GetName() << " is waiting for fork..." << std::endl;
        break;
      case Philosopher::EATING:
        std::cout << m_philosophers[i].GetName() << " is eating... Time remaining: " << m_eating_times[i] << std::endl;
        break;
      case Philosopher::HAS_LEFT_FORK:
        std::cout << m_philosophers[i].GetName() << " has left fork..." << std::endl;
        break;
      case Philosopher::HAS_RIGHT_FORK:
        std::cout << m_philosophers[i].GetName() << " has left fork..." << std::endl;
        break;
      case Philosopher::HAS_TWO_FORKS:
        std::cout << m_philosophers[i].GetName() << " has already two forks..." << std::endl;
      default:
        break;
      }
    }
  }

void Semaphore::_UpdateInfo()
  {
  ++m_time;
  for (size_t i = 0; i < m_size; ++i)
    {
    if (m_eating_times[i] > 0)
      --m_eating_times[i];
    }
  }

void Semaphore::_WatchPhilosopher(size_t i_philosopher)
  {
  std::this_thread::sleep_for(std::chrono::seconds(1));
  size_t first_fork, second_fork;
  if (i_philosopher == m_size - 1)
    {
    first_fork = m_size - 1;
    second_fork = m_size - 2;
    }
  else
    {
    first_fork = i_philosopher;
    second_fork = i_philosopher + 1;
    }

  while (m_used_forks > 3);

  m_forks[first_fork].lock();
  m_philosophers[i_philosopher].GetFork(first_fork < second_fork);
  ++m_used_forks;
  m_forks[second_fork].lock();
  m_philosophers[i_philosopher].GetFork(first_fork > second_fork);
  ++m_used_forks;

  m_eating_times[i_philosopher] = rand() % max_time_for_eating + 1;
  m_philosophers[i_philosopher].Eat();
  while (m_eating_times[i_philosopher] > 0);
  m_philosophers[i_philosopher].StopEat();

  m_philosophers[i_philosopher].PutFork(first_fork > second_fork);
  --m_used_forks;
  m_forks[second_fork].unlock();
  m_philosophers[i_philosopher].PutFork(first_fork < second_fork);
  --m_used_forks;
  m_forks[first_fork].unlock();
  }

void Semaphore::Simulate()
  {
  std::vector<std::thread> threads;
  for (size_t i = 0; i < m_size; ++i)
    threads.emplace_back(&Semaphore::_WatchPhilosopher, *this, i);
  while (true)
    {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    _UpdateInfo();
    std::lock_guard<std::mutex> console_lock(console_mutex);
    std::cout << "Time: " << m_time << std::endl;
    _PrintInfo();
    }
  for (auto& thread : threads)
    thread.join();
  }

int main() {
  Semaphore s(5);
  s.Simulate();
  return 0;
  }