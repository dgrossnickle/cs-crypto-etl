# CS Project

## Assumptions / Considerations
1. Trading / account fees are ignored.
2. Trading execution times (likliness of executing desired price) are ignored.
3. Pricing from Coinbase and Binance is always sorted best-to-worst
   1. Easy fix to add order-by/sort in pandas dataframe if required
4. 100K spend requirement was ballpark figure
   1. Should incorporate intelligent-monte-carlo algo to select order combination with best mid-price within +-10% of 100K
5. Market liquidity/inventory handling needs to be improved
   1. Should incoporate minimum required orders - if not reached, immediately re-hit the API
6. Ignored any limitations between US/EU crypto trading
7. Lower bid price is better
8. Higher ask price is better
9. Should alternate api retrieval sequence (coinbase before binance vs binance before coinbase) to account for trends


## Quick Analysis
*~10%-15% outliers removed due to 403 errors, liquidity, edge-cases, etc. Roughly 580-620 minute-interval data points used in analysis*
### OVERALL: Use Coinbase to sell and Binance to buy (for BTC ETH)
1. BTC Bids - Binance Wins (65% of sample, average var of $1.05)
2. BTC Asks - Coinbase Wins (93% of sample, average var of $5.61)
3. ETH Bids - Binance Wins (79% of sample, average var of $0.16)
4. ETH Asks - Coinbase Wins (97% of sample, average var of $0.47)


## Worker run steps (locally)
1. Install `requirements.txt`
2. Run `run_local.py`
3. Run `test_send_post_request.py` or send post request to `127.0.0.1:5001/run_etl` via Postman


## Worker Architecture (main parts)
1. `app/home/views.py`
   1. Receives the post request and kicks off an endless loop
      1. Runs coinbase etl script, calculates metrics, writes to static CSV
      2. Runs binance etl script, calculates metrics, writes to static CSV
   2. Waits 60 seconds

2. `app/home/tools/home/main.py`
   1. `def run_coinbase`
      1. For each product/ticker retrieve level3 order book data (non aggregated)
            1. For each order type (bid/ask)
               1. Load into pandas dataframe 
               2. Grab top 200 
               3. Calculate usd_value of each trade 
               4. Calculate cumsum (top to bottom)
               5. Find closest cumsum row to 100K (abs)
               6. Remove any additional rows 
               7. Send to CSV writer function
   2. `def run_binance`
      1. For each product/ticker retrieve order book data (limit 300)
         1. For each order type (bid/ask)
            1. Load into pandas dataframe
            2. Calculate usd_value of each trade 
            3. Calculate cumsum (top to bottom)
            4. Find closest cumsum row to 100K (abs)
            5. Remove any additional rows 
            6. Send to CSV writer function
   3. `def write_results_to_csv`
      1. Calculate metrics
         1. Calculate usd_value sum
         2. Calculate size sum
         3. Calcualte mid_price 
         4. Count num_orders 
      2. Write/append data to CSV
      
## Steps for production/deployment

*Estimated time: 4-8 hours depending on BI/Webapp solution and database cleanliness (schema/permissions)

1. Create cloud instance on GCP
2. Create `Source Repository` `cs-crypto-etl` and push all worker code
3. Build `Cloud Build` trigger to automatically run DockerFile build and save container in `Container Registry`
4. Create `Kubernetes Engine` (GKE) with 1-3 nodes and low-memory and stackdriver logging
5. Install Nginx on newly created cluster
6. Modify DNS records for an existing website to point to cloud instance
   1. e.g. add subdomain to hypothetical `dgrossnickle.com` to `cs.dgrossnickle.com`
   2. Add NS records and point to ns-cloud google domain servers
7. Setup `Cloud DNS` to route `cs.dgrossnickle.com` to kubernetes cluster IP
8. Create `Cloud SQL` instance using postgres
   1. Because not writing results to a database is criminal
9. Create flat table which matches CSV format (improve with indexed/performant star schema later)
10. Adjust this worker to account for production
    1. Only run once - no longer loop every 60 seconds
    2. Write results to postgres table instead of static csv
11. Create and Deploy GKE workload `cs-crypto-etl-workload` using `cs-crypto-etl` repo container (include postgres sql database connectivity)
12. Modify GKE nginx-ingress to route `etl.cs.dgrossnickle.com` requests to `cs-crypto-etl-workload` service
13. Test: send post request to `etl.cs.dgrossnickle.com/run_etl` and monitor logs
14. Create `Cloud Scheduler` (CRON) which sends a post request to `etl.cs.dgrossnickle.com/run_etl` every minute on the minute
15. BI - With data continuously flowing into postgres, possibilities are endless
    1. Create postgres views which pivot/aggregate data - use tableau/looker to read
    2. I'd spin up a quick web-application which users would access `app.cs.dgrossnickle.com`
       1. Read from postgres and display most  recent, bid-ask mid-prices along with a sortable/downloadable pricing history table