
#ifndef TXT_SENDER_H
#define TXT_SENDER_H


#include <SFML/Network.hpp>

#include <sstream>
#include <fstream>
#include <iostream>
#include "main_functions.hpp"


class TXT_Sender{
	public:
		TXT_Sender(std::string folder_location_, std::string file_prefix_, std::string file_type_, sf::TcpSocket& tcp_socket_);
		bool check_new_file(std::string& readed_str);
		sf::Socket::Status send(std::string& readed_str);
		sf::Socket::Status check_and_send();
		
	private:
		std::string folder_location;	// lokacja folderu zapisana w sposób pozwalający odczytać ją jako przedrostek
		std::string file_prefix;			// standardowy prefix pliku
		std::string file_type;			// końcówka pliku tekstowego np. txt ( bez kropoki )
		
		sf::TcpSocket& tcp_socket;
		
		unsigned int file_nr = 0;
};

class TXT_Reciver{
public:
    TXT_Reciver(std::string folder_location_, std::string file_prefix_, std::string file_type_, sf::TcpSocket& tcp_socket_);
    bool check_new_message(std::string& readed_str);
    void write(std::string& readed_str);
    bool check_and_write();

private:
    std::string folder_location;	// lokacja folderu zapisana w sposób pozwalający odczytać ją jako przedrostek
    std::string file_prefix;			// standardowy prefix pliku
    std::string file_type;			// końcówka pliku tekstowego np. txt ( bez kropoki )

    sf::TcpSocket& tcp_socket;

    unsigned int file_nr = 0;
};


#endif //TXT_SENDER_H
