#include <iostream>
#include <chrono>
#include <mpi.h>

#include "BMPWriter.h"

void LabMandelbrot(int mode)
  {
  const size_t width = 3840, height = 2160;
  auto t1 = std::chrono::system_clock::now();
  auto t2 = std::chrono::system_clock::now();
  Picture mand;
  BMPWriter writer(width, height);
  int rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  if (mode == 0)
    {
    t1 = std::chrono::system_clock::now();
    mand = MandelbrotSet(width, height);
    t2 = std::chrono::system_clock::now();
    std::cout << "Default time: " << std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count() << std::endl;
    }
  else if (mode == 1)
    {
    t1 = std::chrono::system_clock::now();
    mand = MandelbrotSet(width, height, OMP);
    t2 = std::chrono::system_clock::now();
    std::cout << "OMP time: " << std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count() << std::endl;
    }
  else
    {
    t1 = std::chrono::system_clock::now();
    mand = MandelbrotSet(width, height, MPI);
    t2 = std::chrono::system_clock::now();
    std::cout << "MPI "<<rank<<" time: " << std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count() << std::endl;
    }
  writer.SetPicture(mand);
  writer.Write("D:\\Study\\RayTracing\\ResultsOutputs\\test.bmp");
  }

int main(int argc, char **argv)
  {
  MPI_Init(NULL, NULL);
  int rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  int mode = 0;
  if (rank == 0)
    {
    std::cout << "Enter mode: 0 - default, 1 - OMP, 2 - MPI" << std::endl;
    std::cin >> mode;
    }
  MPI_Bcast(&mode, 1, MPI_INT, 0, MPI_COMM_WORLD);
  if (mode != 2 && rank!=0)
    {
    std::cout << rank << " finalize" << std::endl;
    MPI_Finalize();
    return 0;
    }
  LabMandelbrot(mode);
  MPI_Finalize();
  return 0;
  }