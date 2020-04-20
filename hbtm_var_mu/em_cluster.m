function [cluster_id,Ug,tdiff,mdiff,td2,mark2]=em_cluster(p,times,scores,marks)
N=max(size(p));
cluster_id=zeros(N,1);
Ug=zeros(N,N);
n_clusters=0;
tdiff=[];
mdiff=[];
td2=[];
mark2=[];
for i=1:N
   ptmp=p(1:i,i);
   Ntmp=max(size(ptmp));
   
   if (sum(isnan(ptmp(:))) == Ntmp)
       ptmp
       j = Ntmp;
   else
       j = randsample(Ntmp,1,true,ptmp);
   end
   
   if(j==Ntmp)
       n_clusters=n_clusters+1;
       cluster_id(i)=n_clusters;
   else
      cluster_id(i)=cluster_id(j);  
      Ug(i,j)=1;
      tdiff=[tdiff; times(i)-times(j);];
      mdiff=[mdiff; scores(i)-scores(j);];
      if(marks(i)==marks(j))
         td2=[td2; times(i)-times(j);];
         mark2=[mark2; marks(i);];
          
      end
   end
end
    


end