cmake_minimum_required(VERSION 3.8)

project(Sockets)

add_definitions(-DSOCKET_FILE="ocket")

add_executable(
  Server
  
  common.h
  common.c
  server.c
)

add_executable(
  Client
  
  common.h
  common.c
  client.c
)