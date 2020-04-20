function mu=updatemu(mu,p,T,marks)
mu=zeros(max(size(unique(marks))),1);
N=max(size(p));

for i=1:N    
    mi=marks(i);
    mu(mi)=mu(mi)+p(i,i)/T;
end
end