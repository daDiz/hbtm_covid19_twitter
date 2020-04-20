input=strcat('/Users/haosha/Documents/iupui/research/social_sensing/twitter_politician/stats_kl/allwordmatrix_cutoff0.01.csv');
C = readtable(char(input));


ctab=tabulate(cluster_id);
ccc=unique(cluster_id);
cid=ccc(ctab(:,2)>=0);
hold on
fid=fopen(char(strcat('topic_cluster_',country,'.csv')),'wt');
for i=1:max(size(cid))

    id1=find(ismember(cluster_id,cid(i)));
    U1=Ug(id1,id1);


x=[dates(id1) sts(id1)];

[rows,cols]=size(x);
for j=1:rows
      fprintf(fid,'%f,',i);
      fprintf(fid,'%s,',x{j,1:end-1});
      fprintf(fid,'%f,',marks(id1(j)));
      fprintf(fid,'%s\n',x{j,end});
end

end
fclose(fid);
hold off


fid=fopen(char(strcat('all_cluster_',country,'.csv')),'wt');
for i=1:max(size(cid))
    id1=find(ismember(cluster_id,cid(i)));

   wt=sum(C1(id1,:),1);
   %[~,mw]=max(wt);
   [~,it]=sort(wt,'descend');
   wr=C.Properties.VariableNames(it(1:20));
   
   my=mean(times(id1));
   ms=max(size(id1));
   mm=mode(marks(id1));

      fprintf(fid,'%f,',i);
      fprintf(fid,'%f,',my);
      for ll=1:20
      fprintf(fid,'%s,',char(wr(ll)));
      end
      fprintf(fid,'%f,',ms);
      fprintf(fid,'%f\n',mm);

end
fclose(fid);