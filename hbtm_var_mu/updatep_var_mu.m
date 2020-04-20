function p=updatep_var_mu(mu,p,t,m,K0,w,Msize,p_back,p_on,p_off,marks,cutoff,Nmu,T)

N=max(size(t));
for i=1:N
    Li=sum(m(i,:));
    mi=marks(i);
    for j=max(1,i-cutoff):(i-1)
        mj=marks(j);
        Lj=sum(m(j,:));
        Lov=sum(m(i,:)==m(j,:)&m(j,:)==ones(size(m(j,:))));
        Loff=Lj-Lov;
        Lon=Li-(Lj-Loff);
        p(j,i)=K0(mj,mi)*w(mj,mi)*exp(-w(mj,mi)*(t(i)-t(j)))*p_on(mj,mi)^Lon*(1-p_on(mj,mi))^(Msize-Lj-Lon)*p_off(mj,mi)^Loff*(1-p_off(mj,mi))^(Lj-Loff);
    end
    j=ceil(t(i)/T*Nmu);
    
    % haosha added
    if j <= 0
        j = 1;
    end
    
    p(i,i)=mu(mi,j)*p_back(mi)^(Li)*(1-p_back(mi))^(Msize-Li);%binopdf(sum(m(i,:)),Msize,p_back);

    p(1:i,i)=p(1:i,i)/sum(p(1:i,i));

end
p(p<0) = 0; % haosha
end