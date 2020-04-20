function [K0, w, mu, p_back, p_on, p_off, p, K0_err, p_err]=EMhb_var_mu(t,m,marks,cutoff,emiter,Nmu)
if nargin < 4
   cutoff=100000;
end

if nargin < 5
   emiter=35;
end
% EM estimation of HBTM 
% t is array of event times (sorted increasing order)
% m is array of event binary word arrays
% marks is array of event categories
%
% cutoff is optional parameter to speed up EM, branching probability is
% forced to zero if i-j>cutoff
%
% emiter optional parameter, number of EM iterations

N=max(size(t));
p=zeros(N,N);
T=max(t);
Msize=size(m,2);
Nmarks=max(size(unique(marks)));

K0=.1*ones(Nmarks,Nmarks);
w=.5*ones(Nmarks,Nmarks);
mu=.1*ones(Nmarks,Nmu);

p_back=.1*ones(Nmarks,1);
p_off=.1*ones(Nmarks,Nmarks);
p_on=.1*ones(Nmarks,Nmarks);

% haosha added
K0_err = zeros(emiter);
p_err = zeros(emiter);
K0_prev = K0;
p_prev = p;
%%%%%%%%%%%%%%%%%%%%%%%%%%

% number of iterations
for k=1:emiter

% E-Step
p=updatep_var_mu(mu,p,t,m,K0,w,Msize,p_back,p_on,p_off,marks,cutoff,Nmu,T);   
    
mu=updatemu_var(mu,p,T,marks,t,Nmu);

% M-Step

[K0, w, p_on, p_off, p_back]=updatepar(t,m,p,marks,cutoff);

% Err
K0_err(k) = norm(K0 - K0_prev, 'fro');
K0_prev = K0;
p_err(k) = norm(p - p_prev, 'fro');
p_prev = p;
end


end