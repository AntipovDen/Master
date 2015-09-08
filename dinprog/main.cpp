#include <iostream>
#include <fstream>
#include <cmath>

#define V2 400
#define V 20

int main()
{
    //calculate combination n of k for n = 0..400, k = 0..n
    double** comb = new double*[V2 + 1];
    for (int n = 0; n <= V2; n++)
    {
        comb[n] = new double[n + 1];
        comb[n][0] = comb[n][n] = 1;
        for (int k = 1; k < n; k++)
        {
            comb[n][k] = comb[n][k - 1] * (n - k + 1) / k;
        }
    }

    //calculate k!S(n,k) for n = 0..400, k = 0..n
    long double** stirling = new long double*[V2 + 1];
    stirling[0] = new long double[1];
    stirling[0][0] = 1.0;
    for (int n = 1; n <= V2; n++)
    {
        stirling[n] = new long double[n + 1];
        stirling[n][0] = 0.0;
        stirling[n][1] = 1.0;
        for (int k = 2; k <= n; k++)
        {
            stirling[n][k] = 0.0;
            for (int i = k - 1; i < n; i++)
            {
                 stirling[n][k] += comb[n - 1][i] * stirling[i][k - 1];
            }
        }
    }

    long double k_factorial = 1;

    for (int k = 2; k <= V2; k++)
    {
        k_factorial *= k;
        for (int n = k; n <= V2; n++)
        {
            stirling[n][k] *= k_factorial;
        }
    }

    //calculate the sum of stirling numbers for v = 1..20, l = 1..v, e_0 = l..v^2, m = 1..v - l
    long double**** s = new long double***[V2 + 1];
    for (int v = 0; v <= V; v++)
    {
        s[v] = new long double**[v + 1];
        for (int l = 0; l <= v; l++)
        {
            int lv = l * v;
            s[v][l] = new long double*[v - l + 1];
            for (int m = 0; m <= v - l; m++)
            {
                s[v][l][m] = new long double[v * v  - l + 1];
                for (int e0 = l; e0 <= v * v; e0++)
                {
                    s[v][l][m][e0 - l] = 0.0;
                    long double m_pow = pow(m, l);
                    long double lv_pow = pow(lv, e0 - l);
                    for (int ef = l; ef <= e0; ef++)
                    {
                        s[v][l][m][e0 - l] += lv_pow * m_pow * comb[e0][ef] * stirling[ef][l];
                        m_pow *= m;
                        lv_pow /= lv;
                    }
                }
            }
        }
    }

    //delete stirling numbers
    for (int n = 0; n <= V2; n++)
    {
        delete(stirling[n]);
    }
    delete(stirling);

    //calculate A(vg, i, v, e, l) for vg = 1..20, v = 1..vg, i = 1..v, l = 1..v-i, e = 1..vg^2
    long double***** a = new long double****[V + 1];
    for (int vg = 1; vg <= V; vg++)
    {
        a[vg] = new long double***[vg + 1];
        for (int v = 1; v <= vg; v++)
        {
            a[vg][v] = new long double**[v];
            a[vg][v][0] = new long double*[v + 1];
            for (int l = 1; l < v )
            for (int i = 0; i < v; i++)
            {
                a[vg][v][i] = new long double*[v - i  + 1];
                for (int l = 1; l <= v - i; l++)
                {
                    a[vg][v][i][l] = new long double[V2 + 1];
                    for (int e = 1; e <= V2; e++) {
                        a[vg][v][i][l][e] = 0.0;
                        for
                    }
                }
            }
        }
    }


//    for (int i = 0; i <= V2; i++)
//    {
//        for (int j = 0; j <= i; j++)
//        {
//            std::cout << stirling[i][j] << " ";
//        }
//        std::cout << "\n";
//    }

    return 0;
}