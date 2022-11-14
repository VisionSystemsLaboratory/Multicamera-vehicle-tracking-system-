#pragma once

#include <SFML/Network.hpp>

struct Control_message{
    sf::Int16 left_engine;
    sf::Int16 right_engine;
};

struct Double_ip_message{
    sf::IpAddress sender;
    sf::IpAddress receiver;
};


sf::Packet& operator <<(sf::Packet& packet, const Control_message& directions);
sf::Packet& operator >>(sf::Packet& packet, Control_message& directions);

sf::Packet& operator <<(sf::Packet& packet, const Double_ip_message& ips);
sf::Packet& operator >>(sf::Packet& packet, Double_ip_message& ips);

sf::Packet& operator <<(sf::Packet& packet, const sf::IpAddress& ip);


sf::IpAddress get_ip(sf::Packet& packet);
