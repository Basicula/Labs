cmake_minimum_required(VERSION 3.8)

project(Cryptography)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS           "${CMAKE_CXX_FLAGS} /W4 /WX")
set(CMAKE_CXX_FLAGS_RELEASE   "${CMAKE_CXX_FLAGS} /MT /O2 ${INTRINSICS} /Zi /MP /GL /DNDEBUG")
set(CMAKE_CXX_FLAGS_DEBUG     "${CMAKE_CXX_FLAGS} /MTd /Od /Ob0 ${INTRINSICS} /RTC1 /Zi /D_DEBUG")

include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG master)
FetchContent_GetProperties(googletest)
if(NOT googletest_POPULDATED)
  FetchContent_Populate(googletest)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  set(gtest_disable_pthreads ON CACHE BOOL "" FORCE)
  add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})
  if(MSVC)
    foreach(_tgt gtest gtest_main gmock gmock_main)
      target_compile_definitions(${_tgt} PRIVATE "_SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING")
    endforeach()
  endif()
endif()

set(TEST_DIR "${CMAKE_CURRENT_SOURCE_DIR}/test_files/")
set(RESULTS_PATH "${CMAKE_CURRENT_SOURCE_DIR}/results.txt")
add_definitions(-DTEST_FILES_DIR="${TEST_DIR}")
add_definitions(-DRESULTS_PATH="${RESULTS_PATH}")

add_library(
  Crypto 
  
  STATIC
  
  Crypto/CryptoBase.h 
  Crypto/CryptoBase.cpp 
  
  Crypto/AES.cpp 
  Crypto/AES.h 
  
  Crypto/Kalyna.cpp 
  Crypto/Kalyna.h
  
  Crypto/RC4.cpp 
  Crypto/RC4.h
  
  Crypto/Salsa20.cpp
  Crypto/Salsa20.h
)
target_include_directories(Crypto PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/Crypto")

add_library(
  HashFunc
  
  STATIC
  
  HashFunc/HashFuncBase.h
  
  HashFunc/SHA256.h
  HashFunc/SHA256.cpp
  
  HashFunc/Kupyna.h
  HashFunc/Kupyna.cpp
)
target_include_directories(Crypto PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/HashFunc")

add_executable(Main main.cpp)
target_link_libraries(Main PRIVATE Crypto)
target_link_libraries(Main PRIVATE HashFunc)

enable_testing()

add_executable(
  Tests
  
  Tests/AES_tests.cpp
  Tests/Kalyna_tests.cpp
  Tests/RC4_tests.cpp
  Tests/Salsa20_tests.cpp
  Tests/SHA256_tests.cpp
  Tests/Kupyna_tests.cpp
)
target_link_libraries(Tests PRIVATE Crypto)
target_link_libraries(Tests PRIVATE HashFunc)
target_link_libraries(Tests PRIVATE gtest_main)
add_test(
  NAME
  unit
  COMMAND
  ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/Tests
)