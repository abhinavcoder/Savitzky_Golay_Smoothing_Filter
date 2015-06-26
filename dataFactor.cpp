#include <iostream>
#include <fstream>

using namespace std ;

int main()
{
double dt ,t = 0.0 ; 

ifstream file("ballData_2.txt");
ofstream file1("DataNew.txt") ;
  while(!file.eof()) {
       file>>dt ;
       file1<<dt<<" ";
       file>>dt ;
       file1<<dt<<" ";
       file>>dt ;
       file1<<dt<<" ";
       file>>dt ;
       file1<<t+dt<<endl ;
       t = t + dt ;
    }
 file1.close();
 file.close();

return 0 ;	
}