#include<iostream>


int main()
{
    //we are counting functions for V = 1..20, E = 1..V^2  
    
    for (int V = 1; V <= 20; V++)
        for (int E = 1; E <= V^2; E++)
        {
            long long stirling;
            stirling = 1000000000;
            stirling *= 1000000000;
            stirling *= 1000000000;
            std::cout << stirling << "\n";
            return 0;
        }
            
/*
    int n;
    in >> n;
    int a[n];
    for (int i = 0; i < n; i++)
    {
        a[i] = i;
    }
   
    for (int i = 0; i < n; i++)
    {
        out << a[i] << " ";
    }
    out << "\n";
    out.close();

    return 0;
*/
}
