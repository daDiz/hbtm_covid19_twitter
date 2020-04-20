clear;
rng(123);

data_cutoff = '0.01';

input=sprintf('/Users/haosha/Documents/iupui/research/social_sensing/twitter_politician/stats_kl/testing/time_marks_cutoff%s.csv', data_cutoff);
data = fopen(char(input), 'rt');

a = textscan(data, '%f %f', ...
      'Delimiter',',', 'HeaderLines',1);
fclose(data);


times=a{1};
marks=a{2};

input=sprintf('/Users/haosha/Documents/iupui/research/social_sensing/twitter_politician/stats_kl/testing/text_cutoff%s.csv', data_cutoff);
data = fopen(char(input), 'rt');
a = textscan(data, '%s', ...
      'Delimiter','\n', 'HeaderLines',1);
fclose(data);

sts=a{1};


input=sprintf('/Users/haosha/Documents/iupui/research/social_sensing/twitter_politician/stats_kl/testing/date_cutoff%s.csv', data_cutoff);
data = fopen(char(input), 'rt');

a = textscan(data, '%s', ...
      'Delimiter','\n', 'HeaderLines',1);
fclose(data);
dates=a{1};

input=sprintf('/Users/haosha/Documents/iupui/research/social_sensing/twitter_politician/stats_kl/testing/allwordmatrix_cutoff%s.csv', data_cutoff);
C1 = csvread(char(input),1,0);

cutoff=200;
emiter = 10;
Nmu=20;

% theta is K0
[theta, w, mu, p_back, p_on, p_off, p, theta_err, p_err]=EMhb_var_mu(times,C1,marks,cutoff,emiter,Nmu);

[coeff,score] = pca(C1); 

[cluster_id,Ug,tdiff,mdiff,td2,mrk2]=em_cluster(p,times,score(:,1),marks);

%dlmwrite(char(strcat('offspring_points',country,'.csv')),[tdiff mdiff],'precision',5);
dlmwrite(sprintf('offspring_points_cutoff%s_testing.csv',data_cutoff),[td2 mrk2],'precision',5);


% plot err
figure
plot(1:emiter, theta_err);
title('Theta Err');

figure
plot(1:emiter, p_err);
title('P Err');

tdr=round(tdiff/2);
mdr=round(mdiff);

[table,chi2,pv] = crosstab(tdr,mdr);

figure
plot(tdiff,mdiff,'.'); axis([0 5 -1.5 1.5]);

[xt,yt]=hist(tdiff,100);

wt=mean(tdiff)^-1;
%wt=1.2
yt=yt(1:20);
xt=xt(1:20);
zt=wt*exp(-wt*yt);
zt=zt*sum(xt)/sum(zt);
figure
plot(yt,log(xt),'o',yt,log(zt),'r');

M=max(size(unique(marks))); % num of users
theta_eff=zeros(M,M);
[Nevents,~]=hist(marks,M); % num of tweets per user
for i=1:M
    for j=1:M
        theta_eff(i,j)=theta(i,j)*Nevents(i);
    end
end

dlmwrite(sprintf('adj_matrix_topic_cutoff%s_testing.csv',data_cutoff),theta_eff,'precision',5)
dlmwrite(sprintf('theta_topic_cutoff%s_testing.csv',data_cutoff),theta,'precision',5)
dlmwrite(sprintf('mu_topic_cutoff%s_testing.csv',data_cutoff),mu','precision',5)
dlmwrite(sprintf('w_topic_cutoff%s_testing.csv',data_cutoff),w,'precision',5)
dlmwrite(sprintf('p_back_cutoff%s_testing.csv',data_cutoff),p_back,'precision',5)
dlmwrite(sprintf('p_on_cutoff%s_testing.csv',data_cutoff),p_on,'precision',5)
dlmwrite(sprintf('p_off_cutoff%s_testing.csv',data_cutoff),p_off,'precision',5)
dlmwrite(sprintf('branching_cutoff%s_testing.csv',data_cutoff),p,'precision',5)
dlmwrite(sprintf('p_cutoff%s_testing.csv',data_cutoff),p,'precision',5)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% topic clusters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
input=sprintf('/Users/haosha/Documents/iupui/research/social_sensing/twitter_politician/stats_kl/testing/allwordmatrix_cutoff%s.csv',data_cutoff);
C = readtable(char(input));

ctab=tabulate(cluster_id);
ccc=unique(cluster_id);
cid=ccc(ctab(:,2)>=0);
hold on
fid=fopen(char(sprintf('topic_cluster_cutoff%s_testing.csv',data_cutoff)),'wt');
for i=1:max(size(cid))

    id1=find(ismember(cluster_id,cid(i)));
    U1=Ug(id1,id1);


    x=[dates(id1) sts(id1)];

    [rows,cols]=size(x);
    for j=1:rows
        fprintf(fid,'%d,',i);
        fprintf(fid,'%s,',x{j,1:end-1});
        fprintf(fid,'%d,',marks(id1(j)));
        fprintf(fid,'%s\n',x{j,end});
    end
    
end
fclose(fid);
hold off


fid=fopen(char(sprintf('all_cluster_cutoff%s_testing.csv',data_cutoff)),'wt');
for i=1:max(size(cid))
    id1=find(ismember(cluster_id,cid(i)));

    wt=sum(C1(id1,:),1);
    %[~,mw]=max(wt);
    [~,it]=sort(wt,'descend');
    wr=C.Properties.VariableNames(it(1:10));
   
    my=mean(times(id1));
    ms=max(size(id1));
    mm=mode(marks(id1));

    fprintf(fid,'%d,',i);
    fprintf(fid,'%f,',my);
    for ll=1:10
        fprintf(fid,'%s,',char(wr(ll)));
    end
    fprintf(fid,'%d,',ms);
    fprintf(fid,'%d\n',mm);

end
fclose(fid);


