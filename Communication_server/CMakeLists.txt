cmake_minimum_required(VERSION 3.13)
project(Inzynierka)

set(CMAKE_CXX_STANDARD 20)



add_executable(Inzynierka main.cpp
		main_functions.hpp
		Sended_struct.cpp Sended_struct.hpp
		TXT_Sender.cpp  TXT_Sender.hpp 
		)
        
		target_link_libraries(Inzynierka sfml-network sfml-system sfml-window 
) 
