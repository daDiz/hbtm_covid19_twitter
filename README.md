This folder contains code and data for the paper:

Sha, H.; Al Hasan, M.; Mohler, G.; and Brantingham, P.J. Dynamic topic modeling of the COVID-19 Twitter narrative among U.S. governors and cabinet executives.


The code is tested in Python 3.7.5. See requirements.txt for the packages required.

./hbtm_var_mu

	Matlab code for HBTM, and intermediate data

./query_results

	raw tweets by politicians using Twitter API 

./data

	preprocessd data (COVID-19 related tweets) and intermediate data

./name_handle_party

	politicians meta data (names, Twitter handles, job titles, party affiliations)
 
./script

	scripts for data preparation and post-analysis

	The following is the step-by-step procedure. 

	1. Keyword expansion:

		keyword_extraction_kl.py 


	2. Collecting COVID-19 tweets:

		get_covid_tweets_kl.py


	3. Sort tweets in time ascending order:

		sort_by_time.py


	4. Prepare data in HBTM input formats

		all topics:

			prepare_data_all.py

		subtopics:

			prepare_data_subtopic.py


	5. Run HBTM on Matlab:

		go to ./hbtm_var_mu and run:
	 
			run_hbtm_var_mu_hs.m


	6. Estimate coherence scores:

		do lda and estimate uci coherence

			lda_coh.py 

		estimate uci coherence for HBTM

			hawkes_coh.py

		plot coh HBTM vs. LDA
	 
			plot_coh.py
	 
	7. Plot cluster (topic) timeline 

		plot_topic_pin.py
		plot_topic_pin_risk.py
		plot_topic_pin_vaccine.py
		plot_topic_pin_testing.py

	8. Show dominant parties in clusters

		get_cluster_most_party.py


	9. Plot influence networks

		get_influence_network.py
		get_influence_network_subtopic.py 

	10. Calculate in-degree and out-degree in influence networks

		get_influence_in_out_degree.py
		get_influence_in_out_degree_subtopic.py

	11. Get user spontaneous and triggering rates

		get_mu_theta_by_users.py

