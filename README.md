# **TopTokens**
★ TopTokens is an API that provides analytic screener that sends market recommendations about sell or buy cryptocurrencies that are backed by tier 1 hedge funds based on market situation that is explained by CNN SPX Fear & Greed Index and Crypto Fear & Greed Index. Processing only reliable tokens that are having at least $100,000,000 market cap.

<a name="readme-top"></a>

  <h3 align="center">TopTokens API</h3>

  <p align="center">
    Documentation for TopTokens API Rest protocol
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
      <li><a href="#system-design-overview">System Design Overview</a></li>
      <li><a href="#system-design-in-depth">System Design In Depth</a></li>
       <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

TopTokens is an API that provides analytic screener that sends market recommendations about sell or buy cryptocurrencies that are backed by tier 1 hedge funds based on market situation that is explained by CNN SPX Fear & Greed Index and Crypto Fear & Greed Index. Processing only reliable tokens that are having at least $100,000,000 market cap. If Fear & Greed Index less than 45, api sends BUY recommendation and if Fear & Greed Index more than 55, api sends SELL recommendation.

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

### System Design Overview
![System Design](https://raw.githubusercontent.com/r3v5/toptokens-api/dev/toptokens-system-design.png)


### System Design In Depth
**System Design Architecture for Buffettsbot**

**1. Backend (Django Rest Framework)**
•  **Users**: 
Signup - ```curl -X POST http://127.0.0.1:1337/api/v1/users/signup/ \
     -H "Content-Type: application/json" \
     -d '{
           "email": "t@gmail.com",
           "password": "12345678",
           "password_confirm": "12345678"
         }'``` 
Example response: {
"id":  1,
"email":  "t@gmail.com"
}

Login - ```curl -X POST http://127.0.0.1:1337/api/v1/users/login/ \
     -H "Content-Type: application/json" \
     -d '{
           "email": "t@gmail.com",
           "password": "12345678"
         }'```
 Example response: {
``"access_token":  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNDI0NjM0LCJpYXQiOjE3MjM0MjQ1MTQsImp0aSI6ImU5YjNhYmM0YTUyNjQxZmQ4NTIyYTNiYzc1YTFjMTk1IiwidXNlcl9pZCI6MX0.TNqzEHzUAWJu1mkjrgzL7MZf3GatnUeMnOfQekb56mY",``

``"refresh_token":  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMzQyNDc1NCwiaWF0IjoxNzIzNDI0NTE0LCJqdGkiOiIxMzAyMDUxYjU4MTM0ZTczODRlZWVkZjZkNDc5OTgwMSIsInVzZXJfaWQiOjF9.0jDGiT73JzZmcNb8VyWJzMHNDgr3hTk2HZReRvJcPcE"``
}
         
Logout - ```curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -X POST http://127.0.0.1:1337/api/v1/users/logout/ \
     -H "Content-Type: application/json" \
     -d '{
           "refresh_token": <YOUR_REFRESH_TOKEN>,
         }'```
Example response:
{
"message":  "Logout successfully"
}
        
 Refresh token - ```curl -X POST http://127.0.0.1:1337/api/v1/users/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{
           "refresh": <YOUR_REFRESH_TOKEN>,
         }'```
 Example response: 
{``"access":  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNDI0ODIzLCJpYXQiOjE3MjM0MjQ2NzksImp0aSI6ImNlMzE4YTk3YjcwYjQ2MGQ5ZjllZWYzNTBmOTBkNWE0IiwidXNlcl9pZCI6MX0.F4F68gv4ZlNnPoKJUTNGFUMCrJCl8RH8sg8sb0gh7ts"``}


 Verify Token - ```curl -X POST http://127.0.0.1:1337/api/v1/users/token/verify/\
     -H "Content-Type: application/json" \
     -d '{
           "refresh_token": <YOUR_REFRESH_TOKEN>,
         }'```
 Example response:
 {
``"message":  "Refresh token is valid."``
}

 Profile - ```curl -X GET http://127.0.0.1:1337/api/v1/users/profile/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```
Example response: 
{
``"email":  "t@gmail.com",
"date_joined":  "2024-08-12"``
}
 
 Delete profile - ```curl -X DELETE http://127.0.0.1:1337/api/v1/users/delete-profile/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```

 Delete tokens with None users - ```curl -X DELETE http://127.0.0.1:1337/api/v1/users/token/delete-tokens-with-none-users/```

•  **Analytic screener**:
 List of Cryptocurrencies that are backed by tier 1 hedge funds and have at least $100,000,000 market cap  - ```curl -X GET http://127.0.0.1:1337/api/v1/analytic-screener/cryptocurrencies/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```
 Example response: 
  [

{

"id":  1,

"name":  "Ethereum",

"ticker":  "ETH",

"price":  2537.59,

"market_cap":  305490398140,

"hedge_funds":  [

{

"id":  1,

"name":  "Andreessen Horowitz"

},

{

"id":  3,

"name":  "Galaxy Digital"

},

{

"id":  8,

"name":  "Multicoin Capital"

},

{

"id":  11,

"name":  "Delphi Digital"

}

]

},

{

"id":  2,

"name":  "Solana",

"ticker":  "SOL",

"price":  142.85,

"market_cap":  66735204199,

"hedge_funds":  [

{

"id":  1,

"name":  "Andreessen Horowitz"

},

{

"id":  8,

"name":  "Multicoin Capital"

},

{

"id":  11,

"name":  "Delphi Digital"

}

]

},

{

"id":  3,

"name":  "XRP",

"ticker":  "XRP",

"price":  0.555332,

"market_cap":  31174287222,

"hedge_funds":  [

{

"id":  1,

"name":  "Andreessen Horowitz"

},

{

"id":  6,

"name":  "Pantera Capital"

},

{

"id":  10,

"name":  "Blockchain Capital"

}

]

},

{

"id":  54,

"name":  "Toncoin",

"ticker":  "TON",

"price":  6.19,

"market_cap":  15588430133,

"hedge_funds":  [

{

"id":  6,

"name":  "Pantera Capital"

},

{

"id":  5,

"name":  "Animoca Brands"

}

]

},

 CNN SPX Fear & Greed Index and Crypto Fear & Greed Index  - ```curl -X GET http://127.0.0.1:1337/api/v1/analytic-screener/market-indicators/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```
 Example response:
 [

{

"id":  1,

"name":  "Fear & Greed Stock Market Index",

"value":  24

},

{

"id":  2,

"name":  "Fear & Greed Crypto Market Index",

"value":  25

}

]

Get market recommendations for today  - ```curl -X GET http://127.0.0.1:1337/api/v1/analytic-screener/market-recommendations/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```
 Example response: 
 {

"buy_recommendations":  [

{

"type":  "buy",

"index_name":  "Fear & Greed Stock Market",

"value":  24,

"created_at":  "August 12, 2024, 02:12 AM"

},

{

"type":  "buy",

"index_name":  "Fear & Greed Crypto Market",

"value":  25,

"created_at":  "August 12, 2024, 02:12 AM"

}

],

"sell_recommendations":  []

}

•  **Celery Task Queue for mining data about tier 1 hedge funds portfolios and updating market indicators values**:
```
# Configure Celery Beat

app.conf.beat_schedule = {

"parse_tier_1_portfolios": {

"task": "analytic_screener.tasks.parse_tier_1_portfolios",

"schedule": timedelta(seconds=20),

},

"update_fear_and_greed_indices": {

"task": "analytic_screener.tasks.update_fear_and_greed_indices",

"schedule": timedelta(seconds=20),

},

}

  

app.autodiscover_tasks()
```

**2. Database (PostgreSQL)**
•  **Tables**:
- **CustomUser**: Stores data about user
  - **Fields**:
    - `email`: EmailField, Primary Key, unique, used as the username for authentication.
    - `is_staff`: Boolean, Flag to indicate if the user has staff privileges or not.
    - `is_active`: Boolean, Flag to indicate if the user’s account is active.
    - `date_joined`: DateTimeField, Timestamp of when the user joined the system.
 
- **Cryptocurrency**: Represents a cryptocurrency
  - **Fields**:
    - `name`: CharField, Name of the cryptocurrency.
    - `ticker`: CharField, Abbreviation or symbol of the cryptocurrency.
    - `price`: FloatField, Current price of the cryptocurrency.
    - `market_cap`: PositiveBigIntegerField, Market capitalization of the cryptocurrency.
   
- ******HedgeFund******: Represents a hedge fund
  - **Fields**:
    - `name`: CharField, Name of the hedge fund.
    - `cryptocurrencies`: ManyToManyField, Links to multiple Cryptocurrency instances, indicating which cryptocurrencies the hedge fund is associated with.

- ****MarketIndicator****: Represents a market indicator
  - **Fields**:
    - `name`: CharField, Name of the market indicator.
    - `value`: PositiveIntegerField, Value of the market indicator.

- ******MarketRecommendation******: Represents a market recommendation
  - **Fields**:
    - `type`: CharField, ChoiceField indicating the type of recommendation ("buy" or "sell").
    - `index_name`: CharField, Name of the index or recommendation source.
    - `value`: PositiveIntegerField, Value associated with the recommendation.
    - `created_at`: DateTimeField, Timestamp of when the recommendation was created.
  
   




**4. Deployment & Infrastructure**

•  **Docker Containers**: Used for containerizing the Django application, PostgreSQL database, NGINX reverse proxy server, Redis as message broker and Celery workers that are long-running processes that constantly monitor the task queues for new work and Celery Beat that a single process that schedules periodic tasks

•  **Docker Compose**: Manages multi-container Docker applications.

### Built With

 <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,django,docker,postgres,redis,nginx" />
  </a>

<p align="right">(<a href="#about-the-project">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Get a free API Key at [https://docs.coingecko.com/reference/setting-up-your-api-key](https://docs.coingecko.com/reference/setting-up-your-api-key)

2. Clone the repo
   ```sh
   https://github.com/r3v5/toptokens-api
   ```
3. Navigate to the project directory
   ```sh
   cd toptokens-api
   ```
4. Create a .env.dev file
   ```
   DEBUG=1
   SECRET_KEY=foo
   DJANGO_ALLOWED_HOSTS=localhost  127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=toptokensdb
   SQL_USER=toptokensadmin
   SQL_PASSWORD=toptokensadmin
   SQL_HOST=toptokens-db
   SQL_PORT=5432
   DATABASE=postgres
   POSTGRES_USER=toptokensadmin
   POSTGRES_PASSWORD=toptokensadmin
   POSTGRES_DB=toptokensdb
   CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
   COINGECKO_API_KEY=<YOUR-API-KEY>``
  
  5. Start building docker containers with app and run:
   ```
   docker compose -f docker-compose.yml up --build
   ```
  6. Make migrations, apply them and collect staticfiles:
   ```
   docker compose -f docker-compose.yml exec toptokens-api python manage.py makemigrations
   docker compose -f docker-compose.yml exec toptokens-api python manage.py migrate
   docker compose -f docker-compose.yml exec toptokens-api python manage.py collectstatic --no-input --clear
   ```
   7. Create Django superuser to grant access to Django admin panel:
   ```
   docker compose -f docker-compose.yml exec toptokens-api python manage.py createsuperuser
   ``` 
  8. Run tests:
   ```
   docker compose -f docker-compose.yml exec toptokens-api pytest
   ```
  9. Navigate to Django Admin Panel by this url http://localhost:1337/admin/login/?next=/admin/ and access the content of database with cryptocurrency data:
   ```
   Email address: email address you used to create superuser
   Password: password you used to create superuser
   ```
### Tests Passed

![Tests Passed](https://raw.githubusercontent.com/r3v5/toptokens-api/main/tests-passed.png)
   
<p align="right">(<a href="#about-the-project">back to top</a>)</p>






<!-- CONTACT -->
## Contact

Ian Miller - [linkedin](https://www.linkedin.com/in/ian-miller-620a63245/) 

Project Link: [https://github.com/r3v5/toptokens-api](https://github.com/r3v5/toptokens-api)

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

