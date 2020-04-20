mu=[1,2];
k0=[[.5 .1];[.2 .7];];
w=[[.1 1];[.05 .9];];
T=200;
Msize=200;
p_back=[.1 .08];
p_on=[[.05 .1];[.05 .07];];
p_off=[[.2 .1];[.3 .1];];

[times,m,marks]=hawkesbinom_var_mu(mu,k0,w,T,p_back,p_on,p_off,Msize);

% perform EM parameter estimation
Nmu=5;
[K0h wh muh p_backh p_onh p_offh p]=EMhb_var_mu(times,m,marks,10000,10,Nmu);