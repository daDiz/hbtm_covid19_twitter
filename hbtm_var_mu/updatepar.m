function [K0, w, p_on, p_off, p_back]=updatepar(t,m,p,marks,cutoff)
Nmarks=max(size(unique(marks)));
N=max(size(t));
Msize=size(m,2);

sumP=zeros(Nmarks,Nmarks);

K0=zeros(Nmarks,Nmarks);

w=zeros(Nmarks,Nmarks);

p_back=zeros(Nmarks,1);
p_off=zeros(Nmarks,Nmarks);
p_on=zeros(Nmarks,Nmarks);

sumB=zeros(Nmarks,1);
for i=1:N
    Li=sum(m(i,:));
    mi=marks(i);
    for j=max(1,i-cutoff):(i-1)
        mj=marks(j);
        Lj=sum(m(j,:));
        Lov=sum(m(i,:)==m(j,:)&m(j,:)==ones(size(m(j,:))));
        Loff=Lj-Lov;
        Lon=Li-(Lj-Loff);
        
        sumP(mj,mi)=sumP(mj,mi)+p(j,i);
        w(mj,mi)=w(mj,mi)+p(j,i)*(t(i)-t(j));
        
        p_on(mj,mi)=p_on(mj,mi)+p(j,i)*Lon/(Msize-Lj);
        if(Lj>0)
        p_off(mj,mi)=p_off(mj,mi)+p(j,i)*Loff/Lj;
        end
    end
    p_back(mi)=p_back(mi)+p(i,i)*sum(m(i,:))/Msize;
    sumB(mi)=sumB(mi)+p(i,i);

end


p_back=p_back./sumB;
p_on=p_on./sumP;
p_off=p_off./sumP;
for i=1:Nmarks
    for j=1:Nmarks
    K0(i,j)=sumP(i,j)/sum(marks==i);        
    end
end

w=sumP./w;

end