#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>

int main(int argc, char* argv[])
{
    int V;
    if (argc == 1)
    {
        V = 20;
    }
    else if (argc == 2)
    {
        V = atoi(argv[1]);
        if (V == 0)
        {
            std::cout << "Usage: " << argv[0] << " [number of vertices = 20]\n";
        }
    }
    else
    {
        std::cout << "Usage: " << argv[0] << " [number of vertices = 20]\n";
        return 0;
    }
    int V2 = V * V;

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
    long double**** s = new long double***[V + 1];
    for (int v = 0; v <= V; v++)
    {
        s[v] = new long double**[v + 1];
        for (int l = 0; l <= v; l++)
        {
            int lv = l * v;
            s[v][l] = new long double*[v - l + 1];
            for (int m = 0; m <= v - l; m++)
            {
                s[v][l][m] = new long double[V2  - l + 1];
                for (int e0 = l; e0 <= V2; e0++)
                {
                    s[v][l][m][e0 - l] = 0.0;
                    long double m_pow = powl(m, l);
                    long double lv_pow = powl(lv, e0 - l);
                    for (int ef = l; ef <= e0; ef++)
                    {
                        s[v][l][m][e0 - l] += lv_pow * m_pow;// * comb[e0][ef] * stirling[ef][l];
                        m_pow *= m;
                        lv_pow /= lv;
                    }
                }
            }
        }
    }

    std::ofstream s_file("data/s.out");
    for (int v = 0; v <= V; v++)
        for (int l = 0; l <= v; l++)
            for (int m = 0; m <= v - l; m++) {
                for (int e = l; e <= V2; e++)
                    s_file << s[v][l][m][e - l] << ' ';
                s_file << '\n';
            }
    s_file.close();
    return 0;

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
        int eg = vg * vg;
        a[vg] = new long double***[vg + 1];

        //a(vg, 1, 0, 1, e) = 1

        a[vg][1] = new long double**[1];
        a[vg][1][0] = new long double*[2];
        a[vg][1][0][1] = new long double[eg + 1];
        for (int e = 0; e <= eg; e++)
        {
            a[vg][1][0][1][e] = 1.0;
        }

        for (int v = 2; v <= vg; v++)
        {
            a[vg][v] = new long double**[v];

            //a(vg, v, 0, l, e) = 0, if v != 1
            a[vg][v][0] = new long double*[v + 1];
            for (int l = 1; l <= v; l++)
            {
                a[vg][v][0][l] = new long double[eg + 1];
                for (int e = 0; e <= eg; e++)
                {
                    a[vg][v][0][l][e] = 0.0;
                }
            }

            //rest a(vg, v, i, l, e) = sum(m=1..v-l-1)sum(e0=l..e) a(vg, v-l, i-1, m, e-e0) * comb(vg-v+l, l) * comb(e, e0) * s(v,l,m,e0-l)
            for (int i = 1; i < v; i++)
            {
                a[vg][v][i] = new long double*[v - i  + 1];
                for (int l = 1; l <= v - i; l++)
                {
                    a[vg][v][i][l] = new long double[eg + 1];
                    for (int e = 0; e <= eg; e++) {
                        a[vg][v][i][l][e] = 0.0;
                        for (int m = 1; m <= v - l - i + 1; m++)
                        {
                            for (int e0 = l; e0 <= e; e0++) {
                                a[vg][v][i][l][e] +=
                                        a[vg][v - l][i - 1][m][e - e0] * comb[vg - v + l][l] * comb[e][e0] *
                                        s[v][l][m][e0 - l];

                            }
                        }
                    }
                }
            }
        }
    }
    //seems like i did it!

//    std::ofstream a_file("data/a.out");
//    for (int v = 0; v <= V; v++)
//        for (int i = 0; i < v; i++)
//            for (int l = 1; l <= v - i; l++) {
//                for (int e = 0; e <= V * V; e++)
//                    a_file << a[V][v][i][l][e] << ' ';
//                a_file << '\n';
//            }
//    a_file.close();
//    return 0;

    
    //delete s
    for (int v = 0; v <= V; v++)
    {
        for (int l = 0; l <= v; l++)
        {
            for (int m = 0; m <= v - l; m++)
            {
                delete(s[v][l][m]);
            }
            delete(s[v][l]);
        }
        delete(s[v]);
    }
    delete(s);

    //open file for C
    std::ofstream c_file("data/c.out");

    //calculate C(vg, eg, i, l)
    long double**** c = new long double***[V + 1];
    for (int vg = 1; vg <= V; vg++) {
        c[vg] = new long double**[vg * vg + 1];
        for (int eg = 0; eg <= vg * vg; eg++)
        {
            c[vg][eg] = new long double*[vg];
            for (int i = 0; i < vg; i++)
            {
                c[vg][eg][i] = new long double[vg - i + 1];
                for (int l = 1; l <= vg - i; l++)
                {
                    c[vg][eg][i][l] = 0.0;
                    for (int v = l + i; v < vg; v++)
                    {
                        long double vvvl = (vg - v) * (vg + l);
                        long double vvvl_ee = powl(vvvl, eg);
                        for (int e = 0; e <= eg; e++) {
                            c[vg][eg][i][l] += a[vg][v][i][l][e] * vvvl_ee * comb[eg][e];
                            vvvl_ee /= vvvl;
                        }
                    }
                    c[vg][eg][i][l] += a[vg][vg][i][l][eg];
                    c_file << c[vg][eg][i][l] << " ";
                }
                c_file << std::endl;
            }
        }
    }
    c_file.close();
    
    //delete a
    for (int vg = 1; vg <= V; vg++)
    {
        for (int v = 1; v <= vg; v++)
        {
            for (int i = 0; i < v; i++)
            {
                for (int l = 1; l <= v - i; l++)
                {
                    delete(a[vg][v][i][l]);
                }
                delete(a[vg][v][i]);
            }
            delete(a[vg][v]);
        }
        delete(a[vg]);
    }
    delete(a);

    //delete combinations
    for (int n = 0; n <= V2; n++)
    {
        delete(comb[n]);
    }
    delete(comb);

    //open file for E
    std::ofstream e_file("data/e.out");

    //calculate E(i)

    long double*** e = new long double**[V + 1];
    for (int vg = 1; vg <= V; vg++)
    {
        e[vg] = new long double*[vg * vg + 1];
        long double v_2e = 1.0;
        for (int eg = 0; eg <= vg * vg; eg++)
        {
            e[vg][eg] = new long double[vg];
            for (int i = 0; i < vg; i++)
            {
                e[vg][eg][i] = 0.0;
                for (int l = 1; l <= vg - i; l++)
                {
                    e[vg][eg][i] += c[vg][eg][i][l] * l;
                }
                e[vg][eg][i] /= v_2e;
                e_file << e[vg][eg][i] << " ";
            }
            e_file << "\n";
            v_2e *= vg * vg;
        }
    }
    e_file.close();
    
    // delete c

    for (int vg = 1; vg <= V; vg++)
    {
        for (int eg = 0; eg <= vg * vg; eg++)
        {
            for (int i = 0; i < vg; i++) {
                delete(c[vg][eg][i]);
            }
            delete(c[vg][eg]);
        }
        delete(c[vg]);
    }
    delete(c);

    
    //calculate the final result

//    long double** reachable = new long double*[V + 1];
//    for (int vg = 1; vg <= V; vg++)
//    {
//        reachable[vg] = new long double[vg * vg + 1];
//        for (int eg = 0; eg <= vg * vg; eg++)
//        {
//            reachable[vg][eg] = 0.0;
//            for (int i = 0; i < vg; i++)
//            {
//                reachable[vg][eg] += e[vg][eg][i];
//            }
//        }
//    }

    
    //delete e and reachable
    for (int vg = 1; vg <= V; vg++)
    {
        for (int eg = 0; eg <= vg * vg; eg++)
        {
            delete(e[vg][eg]);
        }
        delete(e[vg]);
//        delete(reachable[vg]);
    }
    delete(e);
//    delete(reachable);

    
    return 0;
}