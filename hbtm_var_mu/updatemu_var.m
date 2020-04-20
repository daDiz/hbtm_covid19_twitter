function mu=updatemu_var(mu,p,T,marks,t,Nmu)
mu=zeros(max(size(unique(marks))),Nmu);
N=max(size(p));

for i=1:N
    j=ceil(t(i)/T*Nmu);
    % haosha added
    if j <= 0
        j = 1;
    end
    mi=marks(i);
    mu(mi,j)=mu(mi,j)+p(i,i)/(T/Nmu);
end
end