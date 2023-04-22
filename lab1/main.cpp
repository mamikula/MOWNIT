#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;
//typy zmieniałem ręcznie

float w(float x, float y){
    return min(abs(x), abs(y));
}

float v(float x, float y){
    return max(abs(x), abs(y));
}
float z1(float x, float y){
    cout <<  std::setprecision(20) <<
         sqrt(x*x + y*y) << endl;
    return sqrt(x*x + y*y);
}

float z2(float x, float y){
    cout <<  std::setprecision(20) <<
         v(x, y)*pow((1 + pow((w(x,y)/v(x,y)),2) ),0.5) << endl;
    return v(x, y)*pow((1 + pow((w(x,y)/v(x,y)),2) ),0.5);
}

float z3(float x, float y){
    cout<<  std::setprecision(20) <<
        (float)2*v(x, y)*pow((0.25 + pow(w(x,y)/((float)2*v(x, y)), 2)), 0.5) << endl;
    return (float)2*v(x, y)*pow((0.25 + pow(w(x,y)/((float)2*v(x, y)), 2)), 0.5);
}

void print(float i, float j){
    z1(i, j);
    z2(i,j);
    z3(i, j);
    cout << endl;
}

int main() {
//        for(int j = 20174; j < 21000; j++){
//
//            if(z1(j, 0.00011223) != z2(j,0.00011223 )){
//                cout << j <<" "<< 0.00011223 <<endl;
//                break;
//            }
//            cout<<endl;
//        }

//    print(1, 6);
//    print(30, 5);
//    print(10, 1000);
//    print(2000, 2015);
//    print(2, 7);
//    print(1234.121, 1.1010);
//    print(101, 20022);
//    print(12345, 200023);
//    print(0.55, 0.0000001);
//    print(20174, 0.00011223);


    return 0;
}
