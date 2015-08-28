prologues := 3;

verbatimtex
%&latex
\documentclass[10pt]{article}
\usepackage[english, russian]{babel}
\begin{document}
etex

input boxes;                       

numeric L; L := 8mm;
numeric R; R := 3mm;

def initbox(text t)(expr x, y) =
    t.c = (x * L, y * L);                           
enddef;

def init(text t)(expr x, y) =
    t.c = (x * L, y * L);
    t.n - t.s = (0R, 2R);
    t.e - t.w = (2R, 0R);
enddef;

def simplearrow(text a)(text b) = 
    drawarrow a.c -- b.c cutbefore bpath.a cutafter bpath.b;
enddef;

def angledarrow(text a)(text b) = 
    drawarrow a.c {dir 30} .. {dir 150} b.c cutbefore bpath.a cutafter bpath.b;
enddef;

def boxme(text u)(text v)(text lbl) =
    pair lblcntr; lblcntr := v.c + (v.n - v.s);
    label(lbl, lblcntr);
    pair verytop; verytop := v.n + (v.n - v.s);
    pair verybtm; verybtm := u.s - (0, 0.2R);
    pair wdh; wdh := v.e - v.w;
    draw (verytop - wdh)--(verytop + wdh)--(verybtm + wdh)--(verybtm - wdh)--cycle dashed evenly;
enddef;

beginfig(1);
	boxit.a(btex Оператор мутации etex); initbox(a)(0, 0); 
	boxit.b(btex RL-агент etex); initbox(b)(5, 0);
	drawboxed(a, b); 

	pair A, B, C, D;
	A := a.c + (0, 15); B := b.c + (0, 15);
	C := a.c - (0, 15); D := b.c - (0, 15);
	drawarrow a.c--A--B--b.c cutbefore bpath.a cutafter bpath.b;
	drawarrow b.c--D--C--a.c cutbefore bpath.b cutafter bpath.a;
	label.top(btex состояние и выигрыш etex, 1/2[A, B]);
	label.bot(btex функция приспособленности etex, 1/2[C, D]);
endfig;

beginfig(2)
    circleit.ax(btex 0 etex); init(ax)(0, -1);
    circleit.ay(btex 1 etex); init(ay)(0,  0);
    circleit.az(btex 2 etex); init(az)(0,  1);

    circleit.bx(btex 0 etex); init(bx)(5, -5);
    circleit.by(btex 1 etex); init(by)(5, -4);
    circleit.bz(btex 2 etex); init(bz)(5, -3);

    circleit.cx(btex 0 etex); init(cx)(5, -1);
    circleit.cy(btex 1 etex); init(cy)(5,  0);
    circleit.cz(btex 2 etex); init(cz)(5,  1);

    circleit.dx(btex 0 etex); init(dx)(5, 3);
    circleit.dy(btex 1 etex); init(dy)(5, 4);
    circleit.dz(btex 2 etex); init(dz)(5, 5);

    circleit.ex(btex 0 etex); init(ex)(10, -5);
    circleit.ey(btex 1 etex); init(ey)(10, -4);
    circleit.ez(btex 2 etex); init(ez)(10, -3);

    circleit.fx(btex 0 etex); init(fx)(10, -1);
    circleit.fy(btex 1 etex); init(fy)(10,  0);
    circleit.fz(btex 2 etex); init(fz)(10,  1);

    circleit.gx(btex 0 etex); init(gx)(10, 3);
    circleit.gy(btex 1 etex); init(gy)(10, 4);
    circleit.gz(btex 2 etex); init(gz)(10, 5);

    circleit.hx(btex 0 etex); init(hx)(15, -1);
    circleit.hy(btex 1 etex); init(hy)(15,  0);
    circleit.hz(btex 2 etex); init(hz)(15,  1);

    circleit.ix(btex 3 etex); init(ix)(7.5, 6.5);

    fixsize(ax, ay, az, bx, by, bz, cx, cy, cz, dx, dy, dz,
            ex, ey, ez, fx, fy, fz, gx, gy, gz, hx, hy, hz, ix);
            
    fixpos(ax, ay, az, bx, by, bz, cx, cy, cz, dx, dy, dz,
           ex, ey, ez, fx, fy, fz, gx, gy, gz, hx, hy, hz, ix);
        
    forsuffixes s=bx, cy, dz, ex, ey, fx, fz, gy, gz, hx, hy, hz:
        fill bpath.s withcolor (0.5, 0.5, 0.5);
    endfor
            
    drawboxed(ax, ay, az, bx, by, bz, cx, cy, cz, dx, dy, dz,
              ex, ey, ez, fx, fy, fz, gx, gy, gz, hx, hy, hz, ix);

    boxme(ax)(az)(btex $\{\}$ etex);
    boxme(bx)(bz)(btex $\{0\}$ etex);
    boxme(cx)(cz)(btex $\{1\}$ etex);
    boxme(dx)(dz)(btex $\{2\}$ etex);
    boxme(ex)(ez)(btex $\{0,1\}$ etex);
    boxme(fx)(fz)(btex $\{0,2\}$ etex);
    boxme(gx)(gz)(btex $\{1,2\}$ etex);
    boxme(hx)(hz)(btex $\{0,1,2\}$ etex);

    drawarrow (ix.c - ( 1.5L, 1L)) -- ix.c cutafter bpath.ix;
    drawarrow (ix.c - ( 0.5L, 1L)) -- ix.c cutafter bpath.ix;
    drawarrow (ix.c - (-1.5L, 1L)) -- ix.c cutafter bpath.ix;
    drawarrow (ix.c - (-0.5L, 1L)) -- ix.c cutafter bpath.ix;

    simplearrow(ax)(by);    
    simplearrow(ax)(bz);    
    simplearrow(ay)(cx);    
    simplearrow(ay)(cz);    
    simplearrow(az)(dx);    
    simplearrow(az)(dy);    
    
    simplearrow(bx)(by);
    simplearrow(by)(ex);
    simplearrow(by)(ez);
    simplearrow(bz)(fx);
    simplearrow(bz)(fy);
    
    simplearrow(cx)(ey);
    simplearrow(cx)(ez);
    simplearrow(cy)(cz);
    simplearrow(cz)(gx);
    simplearrow(cz)(gy);

    simplearrow(dx)(fy);
    simplearrow(dx)(fz);
    simplearrow(dy)(gx);
    simplearrow(dy)(gz);
    
    simplearrow(ex)(ey);
    angledarrow(ex)(ez);
    simplearrow(ey)(ez);
    simplearrow(ez)(hx);
    simplearrow(ez)(hy);

    simplearrow(fx)(fy);
    angledarrow(fx)(fz);
    simplearrow(fy)(hx);
    simplearrow(fy)(hz);
    
    simplearrow(gx)(hy);
    simplearrow(gx)(hz);
    simplearrow(gy)(gz);
    
    simplearrow(hx)(hy);
    simplearrow(hy)(hz);
    angledarrow(hx)(hz);
endfig;

beginfig(3)
    circleit.jj(btex 0 etex); init(jj)(0,0);
    circleit.kj(btex 0 etex); init(kj)(2,0);
    circleit.kk(btex 1 etex); init(kk)(2,1);
    circleit.lj(btex 0 etex); init(lj)(4,0);
    circleit.lk(btex 1 etex); init(lk)(4,1);
    circleit.ll(btex 2 etex); init(ll)(4,2);
    circleit.mj(btex 0 etex); init(mj)(6,0);
    circleit.mk(btex 1 etex); init(mk)(6,1);
    circleit.ml(btex 2 etex); init(ml)(6,2);
    circleit.mm(btex 3 etex); init(mm)(6,3);
    circleit.nj(btex 0 etex); init(nj)(8,0);
    circleit.nk(btex 1 etex); init(nk)(8,1);
    circleit.nl(btex 2 etex); init(nl)(8,2);
    circleit.nm(btex 3 etex); init(nm)(8,3);
    circleit.nn(btex 4 etex); init(nn)(8,4);
    circleit.oj(btex 0 etex); init(oj)(10,0);
    circleit.ok(btex 1 etex); init(ok)(10,1);
    circleit.ol(btex 2 etex); init(ol)(10,2);
    circleit.om(btex 3 etex); init(om)(10,3);
    circleit.on(btex 4 etex); init(on)(10,4);
    circleit.oo(btex 5 etex); init(oo)(10,5);

    fixsize(jj, kk, ll, mm, nn, oo,
            kj, lj, lk, mj, mk, ml, nj, nk, nl, nm, oj, ok, ol, om, on);
    fixpos(jj, kk, ll, mm, nn, oo,
           kj, lj, lk, mj, mk, ml, nj, nk, nl, nm, oj, ok, ol, om, on);

    forsuffixes s=kj, lj, lk, mj, mk, ml, nj, nk, nl, nm, oj, ok, ol, om, on:
        fill bpath.s withcolor (0.5, 0.5, 0.5);
    endfor;

    drawboxed(jj, kk, ll, mm, nn, oo,
              kj, lj, lk, mj, mk, ml, nj, nk, nl, nm, oj, ok, ol, om, on);

    simplearrow(jj)(kk);
    
    simplearrow(kj)(kk);
    simplearrow(kk)(lj);
    simplearrow(kk)(ll);
    
    simplearrow(lj)(lk);
    simplearrow(lk)(ll);
    simplearrow(ll)(mj);
    simplearrow(ll)(mk);
    simplearrow(ll)(mm);
    
    simplearrow(mj)(mk);
    simplearrow(mk)(ml);
    simplearrow(ml)(mm);
    simplearrow(mm)(nj);
    simplearrow(mm)(nk);
    simplearrow(mm)(nl);
    simplearrow(mm)(nn);
    
    simplearrow(nj)(nk);
    simplearrow(nk)(nl);
    simplearrow(nl)(nm);
    simplearrow(nm)(nn);
    simplearrow(nn)(oj);
    simplearrow(nn)(ok);
    simplearrow(nn)(ol);
    simplearrow(nn)(om);
    simplearrow(nn)(oo);

    simplearrow(oj)(ok);
    simplearrow(ok)(ol);
    simplearrow(ol)(om);
    simplearrow(om)(on);
    simplearrow(on)(oo);
endfig;

beginfig(4)
	boxit.a(btex 00000000 etex scaled(5));
	a.c  = (0, 0);
	boxit.b(btex 00110101 etex scaled(5));
	b.c = (0, -75);
	boxit.c(btex 11111111 etex scaled(5));
	c.c = (0, -150); 
	drawunboxed(a);
	drawunboxed(b);
	drawunboxed(c);   
	simplearrow(a)(b);
	simplearrow(b)(c);
endfig;


beginfig(5)         
	boxit.a(btex 1 etex scaled(5));
	a.c = (0,0);
	boxit.b(btex 0 etex scaled(5));
	b.c = (120,0);
	boxit.c(btex 1 etex scaled(5));
	c.c = (0,-75);
	boxit.d(btex 1 etex scaled(5));
	d.c = (120,-75);
	drawunboxed(a);
	drawunboxed(b);
	drawunboxed(c);   
	drawunboxed(d);   
	simplearrow(a)(b);
	simplearrow(c)(d);

	label.top(btex $p = \frac{1}{N}$ etex scaled(2), 1/2[a.c, b.c]);
	label.top(btex $p = 1 - \frac{1}{N}$ etex scaled(2), 1/2[c.c, d.c]);	
endfig;

beginfig(6);
	boxit.a(btex \begin{minipage}{2cm} \begin{center} Агент \par Q-learning \end{center} \end{minipage} etex scaled(4)); initbox(a)(0, 0);
	boxit.b(btex $(1+1)$-EA etex scaled(4)); initbox(b)(0, -6); 
	drawboxed(a, b); 

	pair A, B, C, D, E, F;
	A := a.c + (300, 0); B := b.c + (300, 0); 
	C := b.c - (310, 10); D := a.c - (310, -10);
	E := b.c - (290, -10); F := a.c - (290, 10);
	drawarrow a.c--A--B--b.c cutbefore bpath.a cutafter bpath.b;                      
	drawarrow (b.c - (0, 10))--C--D--(a.c + (0, 10)) cutbefore bpath.b cutafter bpath.a;
	drawarrow (b.c + (0, 10))--E--F--(a.c - (0, 10)) cutbefore bpath.b cutafter bpath.a;
	label.lft(btex \begin{minipage}{3.5cm} \begin{center} функция \par приспособленности \par ($f_0$ или $f_1$) \end{center} \end{minipage} etex scaled(2), 1/2[A, B]);
	label.top(btex состояние $f_1(x_t)$ etex scaled(2), D + (90, 0));
	label.bot(btex \begin{minipage}{4cm} \begin{center} выигрыш \par $f_1(x_t) - f_1(x_{t-1})$ \end{center} \end{minipage} etex scaled(2), F + (85, 0));
endfig;

verbatimtex
\end{document}
etex

end.