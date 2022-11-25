////////////////////////////////////////////////////////////
#include <iostream>
#include <cstdlib>
#include <string>



#include <ctime>
#include <fstream>


#include <thread>
#include <chrono>

#include <SFML/Network.hpp>
#include <SFML/System.hpp>


#include <string>


#include "main_functions.hpp" // tymczasowo zakmoentowane
#include "Sended_struct.hpp"

// Send TXT
#include "TXT_Sender.hpp"




using namespace std;

sf::Vector2i get_wheel_speed(std::string text);
void slow_down(int& l_wheel,int& r_wheel,int diffrent);


float getParamVal ( string id,int argc,char **argv,float defvalue ) {
    for ( int i=0; i<argc; i++ )
        if ( id== argv[i] )
            return atof ( argv[i+1] );
    return defvalue;
}

int main()
{
    /// GPIO
    const int pwm_l = 23;
    const int pwm_r = 27;
    
    const int direction_l1 = 24;
    const int direction_l2 = 25;
    
    const int direction_r1 = 28;
    const int direction_r2 = 29;
    
    const int signal_led = 26;
    

    unsigned short port_udp = 50001;
    unsigned short port_tcp = 50002;

    ///WHEEL
    int right_wheel = 0;
    int left_wheel  = 0;

    sf::Clock clock;

    const sf::IpAddress local_address = sf::IpAddress::getLocalAddress();

    std::cout<<"Lokalne IP to :"<<local_address.toString()<<std::endl;
    
    std::unique_ptr<sf::UdpSocket> udp_socket = std::make_unique<sf::UdpSocket>();
    udp_socket->setBlocking(false);
    udp_socket->bind(port_udp);
    
    sf::IpAddress ip_controller;
      
    // Nawiązywanie komunikacji
    enum class Udp_mode{
        waiting_to_first_conntact,
        send_response_and_waiting_to_second_conntact,
    };

    auto udp_mode = Udp_mode::waiting_to_first_conntact;


    while(true){
        sf::Time time = clock.getElapsedTime();
        if(time.asMilliseconds() > 1000)
        {

            if(udp_mode == Udp_mode::waiting_to_first_conntact){
                sf::Packet packet_received;
                //std::cout << " A1 "<< std::endl;
                sf::Socket::Status status = udp_socket->receive(packet_received, ip_controller, port_udp);
                write_comunicate_sockte_status(status);
                if (status == sf::Socket::Done) {
                    if (ip_controller.toInteger() == get_ip(packet_received).toInteger() and ip_controller.toInteger() != 0) {
                        std::cout << "IP RPI : " << ip_controller.toString() << std::endl;
                        udp_mode = Udp_mode::send_response_and_waiting_to_second_conntact;
                    }
                }
            }else if(udp_mode == Udp_mode::send_response_and_waiting_to_second_conntact){
                Double_ip_message ip_message_sended = {
                    sf::IpAddress::getLocalAddress(),
                    ip_controller
                };
                // Wysłanie wiadmości
                sf::Packet sended_packet;
                sended_packet << ip_message_sended;

                udp_socket->send(sended_packet, ip_controller, port_udp);
                std::cout << "Wyslano potwierdzenie"<< std::endl;

                // Odbieranie wiadomości
                sf::Packet received_packet;
                sf::IpAddress sender_ip;
                if (udp_socket->receive(received_packet, sender_ip, port_udp) == sf::Socket::Done) {
                    
                    Double_ip_message ip_message_received;
                    received_packet >> ip_message_received;
                    
                    std::cout << "Odebrano potwiedzenie"<< std::endl;
                    
                    std::cout << "Odbiornik : "<< ip_message_received.receiver.toString() << std::endl;
                    std::cout << "Nadajnik :  "<< ip_message_received.sender.toString() << std::endl;
                    
                    
                     if(sf::IpAddress::getLocalAddress() == ip_message_received.receiver and
                        ip_controller == ip_message_received.sender
                     ){
                         std::cout << "A2"<< std::endl;
                         std::cout << "Komunikacja potwierdzona "<< std::endl;
                         break;
                     }
                }
            }else{
                throw std::runtime_error("Nieprawidłowy tryb pracy wyszukiwania połączenia");
            }
            clock.restart();
        }
    }

    std::cout << "UDP - Procedura nawiązywania kontaktu zakończona"<< std::endl;



    sf::TcpListener tcp_listener;
    auto listen_status = tcp_listener.listen(port_tcp);
    
    std::cout<<"TCP - listener status: \n";
    write_comunicate_sockte_status(listen_status);
    

    sf::TcpSocket tcp_client;

    
    while(true){
        sf::Time time = clock.getElapsedTime();

        if(time.asMilliseconds() > 1000){
            
            
            auto status = tcp_listener.accept(tcp_client);

            clock.restart();
            std::cout<<"TCP - status połączenia: \n";
            write_comunicate_sockte_status(status);

            if(status == sf::Socket::Status::Done) {
                std::cout<<"TCP - Połączenie poprawne  \n";
                break;
            }
        }
    }
 
    tcp_client.setBlocking(false);
    
    TXT_Sender txt_sender("../Sended_txt", "car", "txt", tcp_client);
    TXT_Reciver txt_reciver("../Recived_txt", "car", "txt", tcp_client);
    
    
    
    
    while(true){
        sf::Time time = clock.getElapsedTime();

        //if(time.asMilliseconds() > 1000){
        if(time.asMilliseconds() > 5){
            clock.restart();

            // Nadawanie
            auto status = txt_sender.check_and_send();
            if (status != sf::Socket::Status::NotReady) 
                write_comunicate_sockte_status(status);
            
            
            
            // Odbieranie:
            txt_reciver.check_and_write();
            
            static int itr = 0;
            itr ++;
        }
     
    }
 
    
    // Wait until the user presses 'enter' key
    std::cout << "Press enter to exit..." << std::endl;
    std::cin.ignore(10000, '\n');

    return EXIT_SUCCESS;
}


