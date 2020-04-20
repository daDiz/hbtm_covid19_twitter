% runs 100 simulations of the Hawkes Binomial Topic Model and performs EM
% parameter estimation

% ground truth parameters
mu=[1,2];
k0=[[.5 .1];[.2 .7];];
w=[[.1 1];[.05 .9];];
T=200;
Msize=200;
p_back=[.1 .08];
p_on=[[.05 .1];[.05 .07];];
p_off=[[.2 .1];[.3 .1];];

k1=zeros(100,1);
k2=zeros(100,1);
k3=zeros(100,1);
k4=zeros(100,1);

w1=zeros(100,1);
w2=zeros(100,1);
w3=zeros(100,1);
w4=zeros(100,1);

mu1=zeros(100,1);
mu2=zeros(100,1);

pb1=zeros(100,1);
pb2=zeros(100,1);

pon1=zeros(100,1);
pon2=zeros(100,1);
pon3=zeros(100,1);
pon4=zeros(100,1);

poff1=zeros(100,1);
poff2=zeros(100,1);
poff3=zeros(100,1);
poff4=zeros(100,1);

rng(124);

% do 100 simulations
for i=1:100

% simulate process
[times,m,marks]=hawkesbinom(mu,k0,w,T,p_back,p_on,p_off,Msize);

% perform EM parameter estimation
[K0h wh muh p_backh p_onh p_offh p]=EMhb(times,m,marks,10000,10);

k1(i)=K0h(1,1);
k2(i)=K0h(1,2);
k3(i)=K0h(2,1);
k4(i)=K0h(2,2);

w1(i)=wh(1,1);
w2(i)=wh(1,2);
w3(i)=wh(2,1);
w4(i)=wh(2,2);

mu1(i)=muh(1);
mu2(i)=muh(2);

pb1(i)=p_backh(1);
pb2(i)=p_backh(2);

pon1(i)=p_onh(1,1);
pon2(i)=p_onh(1,2);
pon3(i)=p_onh(2,1);
pon4(i)=p_onh(2,2);

poff1(i)=p_offh(1,1);
poff2(i)=p_offh(1,2);
poff3(i)=p_offh(2,1);
poff4(i)=p_offh(2,2);

subplot(5,4,1);
[nb,xb]=hist(k1(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*k0(1,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,2);
[nb,xb]=hist(k2(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*k0(1,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,3);
[nb,xb]=hist(k3(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*k0(2,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,4);
[nb,xb]=hist(k4(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*k0(2,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,5);
[nb,xb]=hist(w1(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*w(1,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,6);
[nb,xb]=hist(w2(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*w(1,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,7);
[nb,xb]=hist(w3(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*w(2,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,8);
[nb,xb]=hist(w4(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*w(2,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,9);
[nb,xb]=hist(mu1(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*mu(1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,10);
[nb,xb]=hist(mu2(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*mu(2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,11);
[nb,xb]=hist(pb1(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_back(1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,12);
[nb,xb]=hist(pb2(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_back(2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,13);
[nb,xb]=hist(pon1(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_on(1,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,14);
[nb,xb]=hist(pon2(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_on(1,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,15);
[nb,xb]=hist(pon3(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_on(2,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,16);
[nb,xb]=hist(pon4(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_on(2,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,17);
[nb,xb]=hist(poff1(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_off(1,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,18);
[nb,xb]=hist(poff2(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_off(1,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,19);
[nb,xb]=hist(poff3(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_off(2,1),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);

subplot(5,4,20);
[nb,xb]=hist(poff4(1:i));
bh=bar(xb,nb);
set(bh,'facecolor',[1 1 1]);
set(bh,'edgecolor',[0 0 0]);
set(bh,'LineWidth',1);
hold on
nm=ceil(max(nb));
plot(ones(100,1)*p_off(2,2),[nm/100:nm/100:nm],'r','LineWidth',2)
hold off
axis([min(xb) max(xb) 0 nm]);
drawnow

saveas(gcf,'SynthPlot','epsc');

i
end
