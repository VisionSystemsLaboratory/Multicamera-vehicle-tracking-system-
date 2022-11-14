#cmake_minimum_required(VERSION 3.17)
cmake_minimum_required(VERSION 3.16)
project(Inzynierka)

set(CMAKE_CXX_STANDARD 20)

add_executable(Inzynierka
        main.cpp
        sended_struct.hpp sended_struct.cpp
        main_functions.hpp
        TXT_Sender.hpp TXT_Sender.cpp
        )

target_link_libraries(Inzynierka sfml-network sfml-system sfml-window)
