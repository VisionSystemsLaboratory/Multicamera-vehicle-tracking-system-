
#include <iostream>
#include <cstdlib>
#include <SFML/Network.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>


#include "sended_struct.hpp"
#include "main_functions.hpp"
#include "TXT_Sender.hpp"



void read_keyboard(int& left_wheel,int& right_wheel,int change);

int main() {
    unsigned short port_udp = 50001;
    unsigned short port_tcp = 50002;
    sf::Clock clock;

    const sf::IpAddress local_address = sf::IpAddress::getLocalAddress();

    // odczyt IP
    std::unique_ptr<sf::UdpSocket> udp_socket = std::make_unique<sf::UdpSocket>();
    udp_socket->setBlocking(false);

    udp_socket->bind(port_udp);
    std::cout << "Odczytwanie IP RPI ..." << std::endl;

    sf::IpAddress ip_rpi;

    // Nawiązywanie komunikacji
    enum class Udp_mode {
        broadcast_ip_and_waiting_to_response,
        send_response
    };
    Udp_mode udp_mode = Udp_mode::broadcast_ip_and_waiting_to_response;

    while (true) {
        sf::Time time = clock.getElapsedTime();
        if (time.asMilliseconds() > 1000) {
            clock.restart();
            if (udp_mode == Udp_mode::broadcast_ip_and_waiting_to_response) {
                // Nadawanie
                sf::Packet packet_sended;
                packet_sended << local_address;

                udp_socket->send(packet_sended, sf::IpAddress::Broadcast, port_udp);

                std::cout << "Wysłano komunikat" << std::endl;

                // Odbieranie
                sf::Packet packet_received;
                sf::IpAddress sender_ip;
                if (udp_socket->receive(packet_received, sender_ip, port_udp) == sf::Socket::Done) {
                    Double_ip_message ip_message_received;
                    packet_received >> ip_message_received;
                    if (ip_message_received.receiver == sf::IpAddress::getLocalAddress() and
                        ip_message_received.sender == sender_ip) {
                        std::cout << "Otrzymano wiadomość zwrotna " << std::endl;
                        ip_rpi = sender_ip;
                        udp_mode = Udp_mode::send_response;
                    }
                }
            } else if (udp_mode == Udp_mode::send_response) {
                std::cout << "Wysylanie odpowiedzi" << std::endl;

                Double_ip_message ip_message_sended = {
                        sf::IpAddress::getLocalAddress(),
                        ip_rpi
                };

                sf::Packet sended_packet;
                sended_packet << ip_message_sended;

                std::cout << "Nadajnik " <<ip_message_sended.sender << std::endl;
                std::cout << "Odbiornik "<<ip_message_sended.receiver << std::endl;

                udp_socket->send(sended_packet, ip_rpi, port_udp);
                std::cout << "Wysłano potwierdzenie  " << std::endl;

                break;
            }
            clock.restart();
        }
    }


    std::cout << "UDP - Procedura nawiązywania kontaktu zakończona" << std::endl;


    sf::TcpSocket tcp_socket;

    while(true){
        sf::Time time = clock.getElapsedTime();

        if(time.asMilliseconds() > 1000){
            auto status = tcp_socket.connect(ip_rpi, port_tcp);
            clock.restart();
            write_comunicate_sockte_status(status);


            if(status == sf::Socket::Status::Done) {
                std::cout << "TCP - Procedura nawiązywania kontaktu zakończona " << std::endl;
                break;
            }

        }
    }
    tcp_socket.setBlocking(false);

    TXT_Reciver txt_reciver("../Recived_txt", "car", "txt", tcp_socket);
    TXT_Sender txt_sender("../Sended_txt", "car", "txt", tcp_socket);

    while(true){
        sf::Time time = clock.getElapsedTime();

        //if(time.asMilliseconds() > 1000){
        if(time.asMilliseconds() > 5){
            clock.restart();
            // Nadawanie
            auto status = txt_sender.check_and_send();
            // Odbieranie
            txt_reciver.check_and_write();
        }
    }


    // Wait until the user presses 'enter' key
    std::cout << "Press enter to exit..." << std::endl;
    std::cin.ignore(10000, '\n');
    std::cin.ignore(10000, '\n');

    return EXIT_SUCCESS;
}
