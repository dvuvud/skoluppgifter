#include <iostream>
#include <string>

void hanoi(int n, std::string src, std::string aux,  std::string dest){

    if (n == 1) {
        std::cout << "Disk 1 moves from " + src + " to " + dest << std::endl;
        return;
    }

    hanoi(n-1, src, dest, aux);

    std::cout << "Disk " + std::to_string(n) + " moves from " + src + " to " + dest << std::endl;

    hanoi(n-1, aux, src, dest);

}

int main(){

    hanoi(4, "Source", "Auxilary", "Destination");

}

