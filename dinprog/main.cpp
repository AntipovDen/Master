#include <iostream>
#include <fstream>
#include <cmath>

int main()
{
    //calculate combination n of k for n = 0..400, k = 0..n
    double** comb = new double*[401];
    for (int i = 0; i <= 400; i++)
    {
        comb[i] = new double[i + 1];
        comb[i][0] = comb[i][i] = 1;
        for (int j = 1; j < i; j++)
        {
            comb[i][j] = comb[i][j - 1] * (i - j + 1) / j;
        }
    }

    return 0;
}