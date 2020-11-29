cmake_minimum_required(VERSION 3.8)

project(CommunicationTests)

#add_executable(
#  CommunicationTests
#  
#  #main.cpp
#  
#  Common.h
#  
#  FileTester.cpp
#  MMapTester.cpp
#  SharedTester.cpp
#)

add_executable(
  FileTester
  
  Common.h
  
  FileTester.cpp
)

add_executable(
  MMapTester
  
  Common.h
  
  MMapTester.cpp
)

add_executable(
  SharedTester
  
  Common.h
  
  SharedTester.cpp
)