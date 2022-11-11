
#include "TXT_Sender.hpp"

#include <utility>

TXT_Sender::TXT_Sender(std::string folder_location_, std::string file_prefix_, std::string file_type_, sf::TcpSocket& tcp_socket_):
folder_location(std::move(folder_location_)),
file_prefix(std::move(file_prefix_)),
file_type(std::move(file_type_)),
tcp_socket(tcp_socket_){}


bool TXT_Sender::check_new_file(std::string& readed_str){
	std::string file_name = folder_location + "/" + file_prefix + std::to_string(file_nr + 1) + "." + file_type;
	std::cout<<file_name<<std::endl;
	
	std::fstream file(file_name);
	if(file.is_open()){
		file_nr ++;
		
		std::stringstream buffer;
		buffer << file.rdbuf();

		readed_str = buffer.str();
		std::cout<<"elo 2"<<std::endl;
		return true;
	}else{
		return false;
	}
}
sf::Socket::Status TXT_Sender::send(std::string& readed_str){
	sf::Packet sended_packet;
	sended_packet << readed_str;
	auto send_status = tcp_socket.send(sended_packet);
	//write_comunicate_sockte_status(send_status);
	return send_status;
}

sf::Socket::Status TXT_Sender::check_and_send(){
	std::string readed_str;
	bool is_new_file = check_new_file(readed_str);
	if (not is_new_file){
		return sf::Socket::Status::NotReady;
	}else{
		std::cout<<readed_str<<std::endl;
		return send(readed_str);
	}
}


TXT_Reciver::TXT_Reciver(std::string folder_location_, std::string file_prefix_, std::string file_type_, sf::TcpSocket& tcp_socket_):
        folder_location(std::move(folder_location_)),
        file_prefix(std::move(file_prefix_)),
        file_type(std::move(file_type_)),
        tcp_socket(tcp_socket_){}


bool TXT_Reciver::check_new_message(std::string& readed_str){
    sf::Packet recived_packet;

    auto recived_status = tcp_socket.receive(recived_packet);

    if(recived_status != sf::Socket::NotReady){
        write_comunicate_sockte_status(recived_status);

        if(recived_status == sf::Socket::Status::Done){
            recived_packet >> readed_str;
            std::cout<<readed_str<<std::endl;
            return true;
        }
    }
    return false;
}

void TXT_Reciver::write(std::string &readed_str){
    std::cout<<"Writed file location"<<std::endl;
    std::string file_name = folder_location + "/" + file_prefix + std::to_string(file_nr + 1) + "." + file_type;
    std::cout<<file_name<<std::endl;
    std::ofstream file(file_name);
	std::cout<<"Reade str"<<std::endl;
    std::cout<<readed_str<<std::endl;
    file << readed_str;
    file.close();
    file_nr ++;
}

bool TXT_Reciver::check_and_write() {
    std::string readed_str;
    bool is_new_msg = check_new_message(readed_str);
    if(is_new_msg){
        write(readed_str);
    }
    return is_new_msg;
}
