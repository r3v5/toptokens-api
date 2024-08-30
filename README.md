# **TopTokens**
★ TopTokens is an API that provides analytic screener that sends market recommendations about sell or buy cryptocurrencies that are backed by tier 1 hedge funds based on market situation that is explained by CNN SPX Fear & Greed Index and Crypto Fear & Greed Index. Processing only reliable tokens that are having at least $500,000,000 market cap.

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

TopTokens is an API that provides analytic screener that sends market recommendations about sell or buy cryptocurrencies that are backed by tier 1 hedge funds based on market situation that is explained by CNN SPX Fear & Greed Index and Crypto Fear & Greed Index. Processing only reliable tokens that are having at least $500,000,000 market cap. If Fear & Greed Index less than 45, api sends BUY recommendation and if Fear & Greed Index more than 55, api sends SELL recommendation.

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

### System Design Overview
![System Design](https://raw.githubusercontent.com/r3v5/toptokens-api/dev/toptokens-system-design.png)


### System Design In Depth
**System Design Architecture for Buffettsbot**

**1. Backend (Django Rest Framework)**
• API docs in Postman: [API docs](https://documenter.getpostman.com/view/27242366/2sAXjJ4sVE#intro)

•  **Celery Task Queue for mining data about tier 1 hedge funds portfolios and updating market indicators values**:
```
# Configure Celery Beat
```app.conf.beat_schedule = {
    "parse_tier_1_portfolios": {
        "task": "analytic_screener.tasks.parse_tier_1_portfolios",
        "schedule": timedelta(hours=12),
    },
    "update_fear_and_greed_indices": {
        "task": "analytic_screener.tasks.update_fear_and_greed_indices",
        "schedule": timedelta(hours=12),
    },
    "delete_expired_refresh_tokens": {
        "task": "users.tasks.delete_expired_refresh_tokens",
        "schedule": crontab(
            hour=0, minute=0
        ),  # for dev purposes 2 mins, for prod every midnight
    },
}

app.autodiscover_tasks()
```

**2. Database (PostgreSQL)**
## TopTokens Database Overview
![System Design](https://raw.githubusercontent.com/r3v5/toptokens-api/dev/toptokens-database.png)
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
    - `hedge_funds`: ManyToManyField

- ******HedgeFund******: Represents a hedge fund
  - **Fields**:
    - `name`: CharField, Name of the hedge fund.

- ****MarketIndicator****: Represents a market indicator
  - **Fields**:
    - `name`: CharField, Name of the market indicator.
    - `value`: PositiveIntegerField, Value of the market indicator.

- ******MarketRecommendation******: Represents a market recommendation
  - **Fields**:
    - `type`: CharField, ChoiceField indicating the type of recommendation ("buy" or "sell").
    - `indicator_name`: CharField, Name of the index or recommendation source.
    - `value`: PositiveIntegerField, Value associated with the recommendation.
    - `created_at`: DateTimeField, Timestamp of when the recommendation was created.
  
   



**4. Deployment & Infrastructure**

•  **Docker Containers**: Used for containerizing the Django application, PostgreSQL database, NGINX reverse proxy server, Redis as message broker and Celery workers that are long-running processes that constantly monitor the task queues for new work and Celery Beat that a single process that schedules periodic tasks

•  **Docker Compose**: Manages multi-container Docker applications.

•  **Microsoft Azure Linux Ubuntu**: VM with 2 CPUs and 4gb RAM

•  **Microsoft Azure Container Registries**: Two repositories for toptokens-api and nginx

### Built With

 <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,django,docker,postgres,redis,nginx,azure,linux,ubuntu" />
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
  
  5. In settings.py comment these variables and uncomment CSRF_TRUSTED_ORIGINS for localhost
   ```
   #SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
   #CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")
   CSRF_TRUSTED_ORIGINS = ["http://localhost:1337"]
   ```
  
  6. Start building docker containers for API, Nginx, PostgreSQL, Redis, Celery worker, Celery-beat and up them:
   ```
   docker compose -f docker-compose.yml up --build
   ```
  7. Make migrations, apply them and collect staticfiles:
   ```
   docker compose -f docker-compose.yml exec toptokens-api python manage.py makemigrations
   docker compose -f docker-compose.yml exec toptokens-api python manage.py migrate
   docker compose -f docker-compose.yml exec toptokens-api python manage.py collectstatic --no-input --clear
   ```
   8. Create Django superuser to grant access to Django admin panel:
   ```
   docker compose -f docker-compose.yml exec toptokens-api python manage.py createsuperuser
   ``` 
  9. Run tests:
   ```
   docker compose -f docker-compose.yml exec toptokens-api pytest
   ```
  10. Navigate to Django Admin Panel by this url http://localhost:1337/admin/login/?next=/admin/ and access the content of database with cryptocurrency data:
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

API docs in Postman: [API docs](https://documenter.getpostman.com/view/27242366/2sAXjJ4sVE#intro)

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

