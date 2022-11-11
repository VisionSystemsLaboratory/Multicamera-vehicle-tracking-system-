#ifndef MF_H
#define MF_H



#include<SFML/System.hpp>

inline void write_comunicate_sockte_status(sf::Socket::Status status){
    switch (status){
        case sf::Socket::Disconnected:
            std::cout<<"Nie polaczono"<<std::endl;
            break;
        case sf::Socket::Error :
            std::cout<<"Blad"<<std::endl;
            break;
        case sf::Socket::NotReady :
            std::cout<<"Nie gotowy"<<std::endl;
            break;
        case sf::Socket::Partial :
            std::cout<<"Czesciowo polaczony"<<std::endl;
            break;
        case sf::Socket::Done:
            std::cout<<"Polacznie poprawne"<<std::endl;
            break;
    }
}


#endif
