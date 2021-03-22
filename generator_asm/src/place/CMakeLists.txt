cmake_minimum_required(VERSION 3.11.1)

project(Graph)

FIND_PACKAGE( Boost 1.58 COMPONENTS program_options REQUIRED regex date_time system filesystem thread graph )

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fopenmp -O3")

include_directories(${Boost_INCLUDE_DIR} ${CMAKE_SOURCE_DIR}/include)

file(GLOB_RECURSE H_SRCS ${CMAKE_SOURCE_DIR}/include/*.h)
file(GLOB_RECURSE CXX_SRCS 
    ${CMAKE_SOURCE_DIR}/src/Graph.cpp
)
file(GLOB_RECURSE MAIN_SRCS ${CMAKE_SOURCE_DIR}/src/main.cpp)

add_library(Graph SHARED ${CXX_SRCS})

add_executable(place ${MAIN_SRCS})

target_link_libraries(Graph ${Boost_LIBRARIES})

target_link_libraries(place Graph)
