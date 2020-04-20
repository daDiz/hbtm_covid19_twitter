# htbm_covid19_twitter

## Cite:
This folder contains code and data for the paper:

Sha, H.; Al Hasan, M.; Mohler, G.; and Brantingham, P.J. Dynamic topic modeling of the COVID-19 Twitter narrative among U.S. governors and cabinet executives.

## Note:
The code is tested in Python 3.7.5. See requirements.txt for the packages required.

## Layout:

./hbtm_var_mu -- Matlab code for HBTM (HBTM_var_mu), and intermediate data

./query_results -- raw tweets by politicians using Twitter API 

./data -- preprocessd data (COVID-19 related tweets) and intermediate data

./name_handle_party -- politicians meta data (names, Twitter handles, job titles, party affiliations)
 
./script -- scripts for data preparation and post-analysis

## Run: 

1. Keyword expansion:

	```script/keyword_extraction_kl.py``` 

2. Collecting COVID-19 tweets:

	```script/get_covid_tweets_kl.py```

3. Sort tweets in time ascending order:

	```script/sort_by_time.py```


4. Prepare data in HBTM input formats

   - all topics:

	```script/prepare_data_all.py```

   - subtopics:

	```script/prepare_data_subtopic.py```


5. Run HBTM on Matlab:
 
	```hbtm_var_mu/run_hbtm_var_mu_hs.m```

6. Estimate coherence scores:

   - do lda and estimate uci coherence

	```script/lda_coh.py``` 

   - estimate uci coherence for HBTM

	```script/hawkes_coh.py```

   - plot coh HBTM vs. LDA
	 
	```script/plot_coh.py```
	 
7. Plot cluster (topic) timeline

	```
	script/plot_topic_pin.py
	script/plot_topic_pin_risk.py
	script/plot_topic_pin_vaccine.py
	script/plot_topic_pin_testing.py
	```
8. Show dominant parties in clusters

	```script/get_cluster_most_party.py```

9. Plot influence networks

	```
	script/get_influence_network.py
	script/get_influence_network_subtopic.py 
	```
	
10. Calculate in-degree and out-degree in influence networks

	```
	script/get_influence_in_out_degree.py
	script/get_influence_in_out_degree_subtopic.py
	```
	
11. Get user spontaneous and triggering rates

	```script/get_mu_theta_by_users.py```

