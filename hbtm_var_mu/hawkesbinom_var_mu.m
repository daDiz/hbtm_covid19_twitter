function [times,m,marks]=hawkesbinom_var_mu(mu,k0,w,T,p_back,p_on,p_off,Msize)

%simulate HBTM process

times=zeros(5000,1);
m=zeros(5000,Msize);
marks=zeros(5000,1);

Nmarks=max(size(mu));
%first simulate "background" events which are constant rate
%Poisson and their magnitudes which are exponential

p=0;
for i=1:Nmarks
    p0=p;
    p=p+pois(mu(i)*T);
    marks(p0+1:p)=i;
end

times(1:p)=rand(p,1).^.25*T;
    
    



for i=1:p
    for j=1:Msize
    m(i,j)=rand()<p_back(marks(i));
    end
end

counts=1;
countf=p;

%Next loop through every event and simulate the "offspring"
%even the offspring events can generate their own offspring

while((countf-counts)>-1)
for mm=1:Nmarks
p=pois(k0(marks(counts),mm)); %each event generates p offspring according to a Poisson r.v. with parameter k0
for j=1:p
    temp=times(counts)-log(rand())/w(marks(counts),mm);
     if(temp<T)
        countf=countf+1;
        times(countf)=temp;
        marks(countf)=mm;
        for l=1:Msize
            if(m(counts,l)==1)
                m(countf,l)=rand()>p_off(marks(counts),mm);
            else
                m(countf,l)=rand()<p_on(marks(counts),mm);
            end
        end
    else
    end
end
end
counts=counts+1;
end
times=times(1:countf);
m=m(1:countf,:);
[times it]=sort(times);
m=m(it,:);
marks=marks(it);

return
end


function p=pois(S)

if(S<=100)
temp=-S;
L=exp(temp);
k=0;
p=1; 
while(p > L)
k=k+1;
p=p*rand();
end
p=k-1;
else
p=floor(S+S^.5*randn());
end
end
