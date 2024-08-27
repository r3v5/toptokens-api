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
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
     -d '{
           "refresh_token": <YOUR_REFRESH_TOKEN>,
         }'```


•  **Analytic screener**:
 List of Cryptocurrencies that are backed by tier 1 hedge funds and have at least $500,000,000 market cap.
 Query Parameters:
	•	order: (optional) "asc" or "desc" to specify the sorting order by market cap. Defaults to "desc".
  ```curl -X GET http://127.0.0.1:1337/api/v1/analytic-screener/cryptocurrencies/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```
 Example response: 
  [
    {
        "id": 1,
        "name": "ethereum",
        "ticker": "ETH",
        "price": 2585.79,
        "market_cap": 311009745811,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 3,
                "name": "Galaxy Digital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 2,
        "name": "solana",
        "ticker": "SOL",
        "price": 155.42,
        "market_cap": 72438447133,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 3,
        "name": "ripple",
        "ticker": "XRP",
        "price": 0.597524,
        "market_cap": 33576445782,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 28,
        "name": "the-open-network",
        "ticker": "TON",
        "price": 5.49,
        "market_cap": 13904458661,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 5,
                "name": "Animoca Brands"
            }
        ]
    },
    {
        "id": 4,
        "name": "avalanche-2",
        "ticker": "AVAX",
        "price": 25.77,
        "market_cap": 10428722114,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 3,
                "name": "Galaxy Digital"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            }
        ]
    },
    {
        "id": 29,
        "name": "shiba-inu",
        "ticker": "SHIB",
        "price": 1.458e-05,
        "market_cap": 8584657466,
        "hedge_funds": [
            {
                "id": 5,
                "name": "Animoca Brands"
            }
        ]
    },
    {
        "id": 33,
        "name": "polkadot",
        "ticker": "DOT",
        "price": 4.58,
        "market_cap": 6433533844,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            }
        ]
    },
    {
        "id": 5,
        "name": "near",
        "ticker": "NEAR",
        "price": 4.88,
        "market_cap": 5393982890,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 23,
        "name": "matic-network",
        "ticker": "MATIC",
        "price": 0.494203,
        "market_cap": 4588694923,
        "hedge_funds": [
            {
                "id": 3,
                "name": "Galaxy Digital"
            },
            {
                "id": 5,
                "name": "Animoca Brands"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 6,
        "name": "uniswap",
        "ticker": "UNI",
        "price": 6.05,
        "market_cap": 4563321766,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            },
            {
                "id": 2,
                "name": "Paradigm"
            }
        ]
    },
    {
        "id": 7,
        "name": "internet-computer",
        "ticker": "ICP",
        "price": 8.19,
        "market_cap": 3843379043,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 8,
        "name": "aptos",
        "ticker": "APT",
        "price": 7.44,
        "market_cap": 3617796488,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 24,
        "name": "monero",
        "ticker": "XMR",
        "price": 162.15,
        "market_cap": 2990701508,
        "hedge_funds": [
            {
                "id": 3,
                "name": "Galaxy Digital"
            }
        ]
    },
    {
        "id": 48,
        "name": "blockstack",
        "ticker": "STX",
        "price": 1.81,
        "market_cap": 2696624236,
        "hedge_funds": [
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 9,
        "name": "sui",
        "ticker": "SUI",
        "price": 0.921594,
        "market_cap": 2394197129,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 41,
        "name": "render-token",
        "ticker": "RENDER",
        "price": 6.02,
        "market_cap": 2362089610,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            }
        ]
    },
    {
        "id": 26,
        "name": "filecoin",
        "ticker": "FIL",
        "price": 3.95,
        "market_cap": 2295115611,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            },
            {
                "id": 4,
                "name": "Sequoia Capital Portfolio"
            }
        ]
    },
    {
        "id": 30,
        "name": "immutable-x",
        "ticker": "IMX",
        "price": 1.44,
        "market_cap": 2267748806,
        "hedge_funds": [
            {
                "id": 5,
                "name": "Animoca Brands"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 34,
        "name": "injective-protocol",
        "ticker": "INJ",
        "price": 20.99,
        "market_cap": 2046669548,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            }
        ]
    },
    {
        "id": 38,
        "name": "mantle",
        "ticker": "MNT",
        "price": 0.607671,
        "market_cap": 1985164370,
        "hedge_funds": [
            {
                "id": 7,
                "name": "DragonFly Capital"
            }
        ]
    },
    {
        "id": 10,
        "name": "maker",
        "ticker": "MKR",
        "price": 2118.86,
        "market_cap": 1972061738,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 2,
                "name": "Paradigm"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            }
        ]
    },
    {
        "id": 35,
        "name": "arbitrum",
        "ticker": "ARB",
        "price": 0.560007,
        "market_cap": 1956996251,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            }
        ]
    },
    {
        "id": 20,
        "name": "cosmos",
        "ticker": "ATOM",
        "price": 4.89,
        "market_cap": 1909908443,
        "hedge_funds": [
            {
                "id": 2,
                "name": "Paradigm"
            },
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            }
        ]
    },
    {
        "id": 49,
        "name": "aave",
        "ticker": "AAVE",
        "price": 123.54,
        "market_cap": 1842828277,
        "hedge_funds": [
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 11,
        "name": "optimism",
        "ticker": "OP",
        "price": 1.47,
        "market_cap": 1743686803,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 2,
                "name": "Paradigm"
            }
        ]
    },
    {
        "id": 12,
        "name": "arweave",
        "ticker": "AR",
        "price": 24.76,
        "market_cap": 1619911806,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 42,
        "name": "the-graph",
        "ticker": "GRT",
        "price": 0.16086,
        "market_cap": 1536076756,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 43,
        "name": "thorchain",
        "ticker": "RUNE",
        "price": 4.22,
        "market_cap": 1412641538,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 39,
        "name": "bitget-token",
        "ticker": "BGB",
        "price": 0.99594,
        "market_cap": 1394712138,
        "hedge_funds": [
            {
                "id": 7,
                "name": "DragonFly Capital"
            }
        ]
    },
    {
        "id": 50,
        "name": "theta-token",
        "ticker": "THETA",
        "price": 1.33,
        "market_cap": 1333779729,
        "hedge_funds": [
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 13,
        "name": "helium",
        "ticker": "HNT",
        "price": 7.01,
        "market_cap": 1186566424,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            }
        ]
    },
    {
        "id": 44,
        "name": "algorand",
        "ticker": "ALGO",
        "price": 0.134398,
        "market_cap": 1105735613,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            }
        ]
    },
    {
        "id": 25,
        "name": "celestia",
        "ticker": "TIA",
        "price": 5.33,
        "market_cap": 1103614074,
        "hedge_funds": [
            {
                "id": 3,
                "name": "Galaxy Digital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 45,
        "name": "pyth-network",
        "ticker": "PYTH",
        "price": 0.298285,
        "market_cap": 1080612872,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 46,
        "name": "sei-network",
        "ticker": "SEI",
        "price": 0.325749,
        "market_cap": 1074381108,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 14,
        "name": "lido-dao",
        "ticker": "LDO",
        "price": 1.16,
        "market_cap": 1042176575,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 2,
                "name": "Paradigm"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 36,
        "name": "ondo-finance",
        "ticker": "ONDO",
        "price": 0.697151,
        "market_cap": 1006521958,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 15,
        "name": "flow",
        "ticker": "FLOW",
        "price": 0.575578,
        "market_cap": 879144689,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 5,
                "name": "Animoca Brands"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            }
        ]
    },
    {
        "id": 16,
        "name": "axie-infinity",
        "ticker": "AXS",
        "price": 4.98,
        "market_cap": 742836764,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 2,
                "name": "Paradigm"
            },
            {
                "id": 5,
                "name": "Animoca Brands"
            }
        ]
    },
    {
        "id": 17,
        "name": "dydx-chain",
        "ticker": "DYDX",
        "price": 1.053,
        "market_cap": 651634598,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 7,
                "name": "DragonFly Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    },
    {
        "id": 31,
        "name": "the-sandbox",
        "ticker": "SAND",
        "price": 0.277221,
        "market_cap": 647461559,
        "hedge_funds": [
            {
                "id": 5,
                "name": "Animoca Brands"
            }
        ]
    },
    {
        "id": 27,
        "name": "conflux-token",
        "ticker": "CFX",
        "price": 0.146462,
        "market_cap": 635150898,
        "hedge_funds": [
            {
                "id": 4,
                "name": "Sequoia Capital Portfolio"
            }
        ]
    },
    {
        "id": 21,
        "name": "starknet",
        "ticker": "STRK",
        "price": 0.389064,
        "market_cap": 630077766,
        "hedge_funds": [
            {
                "id": 2,
                "name": "Paradigm"
            },
            {
                "id": 4,
                "name": "Sequoia Capital Portfolio"
            },
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 18,
        "name": "worldcoin-wld",
        "ticker": "WLD",
        "price": 1.62,
        "market_cap": 624935114,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            },
            {
                "id": 10,
                "name": "Blockchain Capital"
            }
        ]
    },
    {
        "id": 47,
        "name": "wormhole",
        "ticker": "W",
        "price": 0.237456,
        "market_cap": 612423919,
        "hedge_funds": [
            {
                "id": 8,
                "name": "Multicoin Capital"
            }
        ]
    },
    {
        "id": 19,
        "name": "ronin",
        "ticker": "RON",
        "price": 1.67,
        "market_cap": 576375208,
        "hedge_funds": [
            {
                "id": 1,
                "name": "Andreessen Horowitz"
            }
        ]
    },
    {
        "id": 22,
        "name": "mina-protocol",
        "ticker": "MINA",
        "price": 0.485424,
        "market_cap": 555495299,
        "hedge_funds": [
            {
                "id": 2,
                "name": "Paradigm"
            },
            {
                "id": 6,
                "name": "Pantera Capital"
            },
            {
                "id": 8,
                "name": "Multicoin Capital"
            },
            {
                "id": 9,
                "name": "Coinbase Ventures"
            }
        ]
    },
    {
        "id": 37,
        "name": "zcash",
        "ticker": "ZEC",
        "price": 36.27,
        "market_cap": 548313378,
        "hedge_funds": [
            {
                "id": 6,
                "name": "Pantera Capital"
            }
        ]
    },
    {
        "id": 32,
        "name": "decentraland",
        "ticker": "MANA",
        "price": 0.293673,
        "market_cap": 546973857,
        "hedge_funds": [
            {
                "id": 5,
                "name": "Animoca Brands"
            }
        ]
    },
    {
        "id": 40,
        "name": "ethena",
        "ticker": "ENA",
        "price": 0.292514,
        "market_cap": 528363871,
        "hedge_funds": [
            {
                "id": 7,
                "name": "DragonFly Capital"
            },
            {
                "id": 11,
                "name": "Delphi Digital"
            }
        ]
    }
]

Get tier 1 hedge funds portfolios - ```curl -X GET http://127.0.0.1:1337/api/v1/analytic-screener/hedge-funds-portfolio/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"```
Example response:
[
    {
        "id": 1,
        "name": "Andreessen Horowitz",
        "cryptocurrencies": [
            {
                "id": 2,
                "name": "solana",
                "ticker": "SOL",
                "price": 155.42,
                "market_cap": 72438447133,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 3,
                "name": "ripple",
                "ticker": "XRP",
                "price": 0.597524,
                "market_cap": 33576445782,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 4,
                "name": "avalanche-2",
                "ticker": "AVAX",
                "price": 25.77,
                "market_cap": 10428722114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 5,
                "name": "near",
                "ticker": "NEAR",
                "price": 4.88,
                "market_cap": 5393982890,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 6,
                "name": "uniswap",
                "ticker": "UNI",
                "price": 6.05,
                "market_cap": 4563321766,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 7,
                "name": "internet-computer",
                "ticker": "ICP",
                "price": 8.19,
                "market_cap": 3843379043,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 8,
                "name": "aptos",
                "ticker": "APT",
                "price": 7.44,
                "market_cap": 3617796488,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 9,
                "name": "sui",
                "ticker": "SUI",
                "price": 0.921594,
                "market_cap": 2394197129,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 10,
                "name": "maker",
                "ticker": "MKR",
                "price": 2118.86,
                "market_cap": 1972061738,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 11,
                "name": "optimism",
                "ticker": "OP",
                "price": 1.47,
                "market_cap": 1743686803,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    }
                ]
            },
            {
                "id": 12,
                "name": "arweave",
                "ticker": "AR",
                "price": 24.76,
                "market_cap": 1619911806,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 13,
                "name": "helium",
                "ticker": "HNT",
                "price": 7.01,
                "market_cap": 1186566424,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 14,
                "name": "lido-dao",
                "ticker": "LDO",
                "price": 1.16,
                "market_cap": 1042176575,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 15,
                "name": "flow",
                "ticker": "FLOW",
                "price": 0.575578,
                "market_cap": 879144689,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 16,
                "name": "axie-infinity",
                "ticker": "AXS",
                "price": 4.98,
                "market_cap": 742836764,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 17,
                "name": "dydx-chain",
                "ticker": "DYDX",
                "price": 1.053,
                "market_cap": 651634598,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 18,
                "name": "worldcoin-wld",
                "ticker": "WLD",
                "price": 1.62,
                "market_cap": 624935114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 19,
                "name": "ronin",
                "ticker": "RON",
                "price": 1.67,
                "market_cap": 577341064,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    }
                ]
            },
            {
                "id": 1,
                "name": "ethereum",
                "ticker": "ETH",
                "price": 2585.79,
                "market_cap": 311009745811,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            }
        ]
    },
    {
        "id": 2,
        "name": "Paradigm",
        "cryptocurrencies": [
            {
                "id": 10,
                "name": "maker",
                "ticker": "MKR",
                "price": 2118.86,
                "market_cap": 1972061738,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 20,
                "name": "cosmos",
                "ticker": "ATOM",
                "price": 4.89,
                "market_cap": 1909908443,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 11,
                "name": "optimism",
                "ticker": "OP",
                "price": 1.47,
                "market_cap": 1743686803,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    }
                ]
            },
            {
                "id": 14,
                "name": "lido-dao",
                "ticker": "LDO",
                "price": 1.16,
                "market_cap": 1042176575,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 16,
                "name": "axie-infinity",
                "ticker": "AXS",
                "price": 4.98,
                "market_cap": 742836764,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 21,
                "name": "starknet",
                "ticker": "STRK",
                "price": 0.389064,
                "market_cap": 630077766,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 22,
                "name": "mina-protocol",
                "ticker": "MINA",
                "price": 0.485424,
                "market_cap": 555495299,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 6,
                "name": "uniswap",
                "ticker": "UNI",
                "price": 6.05,
                "market_cap": 4563321766,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            }
        ]
    },
    {
        "id": 3,
        "name": "Galaxy Digital",
        "cryptocurrencies": [
            {
                "id": 4,
                "name": "avalanche-2",
                "ticker": "AVAX",
                "price": 25.77,
                "market_cap": 10428722114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 23,
                "name": "matic-network",
                "ticker": "MATIC",
                "price": 0.494203,
                "market_cap": 4588694923,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 24,
                "name": "monero",
                "ticker": "XMR",
                "price": 162.15,
                "market_cap": 2990701508,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    }
                ]
            },
            {
                "id": 25,
                "name": "celestia",
                "ticker": "TIA",
                "price": 5.33,
                "market_cap": 1103614074,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 1,
                "name": "ethereum",
                "ticker": "ETH",
                "price": 2585.79,
                "market_cap": 311009745811,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            }
        ]
    },
    {
        "id": 4,
        "name": "Sequoia Capital Portfolio",
        "cryptocurrencies": [
            {
                "id": 27,
                "name": "conflux-token",
                "ticker": "CFX",
                "price": 0.146462,
                "market_cap": 635150898,
                "hedge_funds": [
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    }
                ]
            },
            {
                "id": 21,
                "name": "starknet",
                "ticker": "STRK",
                "price": 0.389064,
                "market_cap": 630077766,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 26,
                "name": "filecoin",
                "ticker": "FIL",
                "price": 3.95,
                "market_cap": 2295115611,
                "hedge_funds": [
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            }
        ]
    },
    {
        "id": 5,
        "name": "Animoca Brands",
        "cryptocurrencies": [
            {
                "id": 29,
                "name": "shiba-inu",
                "ticker": "SHIB",
                "price": 1.458e-05,
                "market_cap": 8584657466,
                "hedge_funds": [
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 23,
                "name": "matic-network",
                "ticker": "MATIC",
                "price": 0.494203,
                "market_cap": 4588694923,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 30,
                "name": "immutable-x",
                "ticker": "IMX",
                "price": 1.44,
                "market_cap": 2267748806,
                "hedge_funds": [
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 15,
                "name": "flow",
                "ticker": "FLOW",
                "price": 0.575578,
                "market_cap": 879144689,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 16,
                "name": "axie-infinity",
                "ticker": "AXS",
                "price": 4.98,
                "market_cap": 742836764,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 31,
                "name": "the-sandbox",
                "ticker": "SAND",
                "price": 0.277221,
                "market_cap": 647461559,
                "hedge_funds": [
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 32,
                "name": "decentraland",
                "ticker": "MANA",
                "price": 0.293673,
                "market_cap": 546973857,
                "hedge_funds": [
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 28,
                "name": "the-open-network",
                "ticker": "TON",
                "price": 5.49,
                "market_cap": 13904458661,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            }
        ]
    },
    {
        "id": 6,
        "name": "Pantera Capital",
        "cryptocurrencies": [
            {
                "id": 28,
                "name": "the-open-network",
                "ticker": "TON",
                "price": 5.49,
                "market_cap": 13904458661,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    }
                ]
            },
            {
                "id": 33,
                "name": "polkadot",
                "ticker": "DOT",
                "price": 4.58,
                "market_cap": 6433533844,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    }
                ]
            },
            {
                "id": 5,
                "name": "near",
                "ticker": "NEAR",
                "price": 4.88,
                "market_cap": 5393982890,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 26,
                "name": "filecoin",
                "ticker": "FIL",
                "price": 3.95,
                "market_cap": 2295115611,
                "hedge_funds": [
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 34,
                "name": "injective-protocol",
                "ticker": "INJ",
                "price": 20.99,
                "market_cap": 2046669548,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    }
                ]
            },
            {
                "id": 35,
                "name": "arbitrum",
                "ticker": "ARB",
                "price": 0.560007,
                "market_cap": 1956996251,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    }
                ]
            },
            {
                "id": 20,
                "name": "cosmos",
                "ticker": "ATOM",
                "price": 4.89,
                "market_cap": 1909908443,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 13,
                "name": "helium",
                "ticker": "HNT",
                "price": 7.01,
                "market_cap": 1186566424,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 36,
                "name": "ondo-finance",
                "ticker": "ONDO",
                "price": 0.697151,
                "market_cap": 1006521958,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 21,
                "name": "starknet",
                "ticker": "STRK",
                "price": 0.389064,
                "market_cap": 630077766,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 22,
                "name": "mina-protocol",
                "ticker": "MINA",
                "price": 0.485424,
                "market_cap": 555495299,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 37,
                "name": "zcash",
                "ticker": "ZEC",
                "price": 36.27,
                "market_cap": 548313378,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    }
                ]
            },
            {
                "id": 3,
                "name": "ripple",
                "ticker": "XRP",
                "price": 0.597524,
                "market_cap": 33576445782,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            }
        ]
    },
    {
        "id": 7,
        "name": "DragonFly Capital",
        "cryptocurrencies": [
            {
                "id": 5,
                "name": "near",
                "ticker": "NEAR",
                "price": 4.88,
                "market_cap": 5393982890,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 23,
                "name": "matic-network",
                "ticker": "MATIC",
                "price": 0.494203,
                "market_cap": 4588694923,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 8,
                "name": "aptos",
                "ticker": "APT",
                "price": 7.44,
                "market_cap": 3617796488,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 38,
                "name": "mantle",
                "ticker": "MNT",
                "price": 0.607671,
                "market_cap": 1985164370,
                "hedge_funds": [
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 10,
                "name": "maker",
                "ticker": "MKR",
                "price": 2118.86,
                "market_cap": 1972061738,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 20,
                "name": "cosmos",
                "ticker": "ATOM",
                "price": 4.89,
                "market_cap": 1909908443,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 39,
                "name": "bitget-token",
                "ticker": "BGB",
                "price": 0.99594,
                "market_cap": 1394712138,
                "hedge_funds": [
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            },
            {
                "id": 14,
                "name": "lido-dao",
                "ticker": "LDO",
                "price": 1.16,
                "market_cap": 1042176575,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 17,
                "name": "dydx-chain",
                "ticker": "DYDX",
                "price": 1.053,
                "market_cap": 651634598,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 40,
                "name": "ethena",
                "ticker": "ENA",
                "price": 0.292514,
                "market_cap": 528363871,
                "hedge_funds": [
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 4,
                "name": "avalanche-2",
                "ticker": "AVAX",
                "price": 25.77,
                "market_cap": 10428722114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    }
                ]
            }
        ]
    },
    {
        "id": 8,
        "name": "Multicoin Capital",
        "cryptocurrencies": [
            {
                "id": 2,
                "name": "solana",
                "ticker": "SOL",
                "price": 155.42,
                "market_cap": 72438447133,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 5,
                "name": "near",
                "ticker": "NEAR",
                "price": 4.88,
                "market_cap": 5393982890,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 7,
                "name": "internet-computer",
                "ticker": "ICP",
                "price": 8.19,
                "market_cap": 3843379043,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 8,
                "name": "aptos",
                "ticker": "APT",
                "price": 7.44,
                "market_cap": 3617796488,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 41,
                "name": "render-token",
                "ticker": "RENDER",
                "price": 6.02,
                "market_cap": 2362089610,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 12,
                "name": "arweave",
                "ticker": "AR",
                "price": 24.76,
                "market_cap": 1619911806,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 42,
                "name": "the-graph",
                "ticker": "GRT",
                "price": 0.16086,
                "market_cap": 1536076756,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 43,
                "name": "thorchain",
                "ticker": "RUNE",
                "price": 4.22,
                "market_cap": 1412641538,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 13,
                "name": "helium",
                "ticker": "HNT",
                "price": 7.01,
                "market_cap": 1186566424,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 44,
                "name": "algorand",
                "ticker": "ALGO",
                "price": 0.134398,
                "market_cap": 1105735613,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 45,
                "name": "pyth-network",
                "ticker": "PYTH",
                "price": 0.298285,
                "market_cap": 1080612872,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 46,
                "name": "sei-network",
                "ticker": "SEI",
                "price": 0.325749,
                "market_cap": 1074381108,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 14,
                "name": "lido-dao",
                "ticker": "LDO",
                "price": 1.16,
                "market_cap": 1042176575,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 15,
                "name": "flow",
                "ticker": "FLOW",
                "price": 0.575578,
                "market_cap": 879144689,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 21,
                "name": "starknet",
                "ticker": "STRK",
                "price": 0.389064,
                "market_cap": 630077766,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 18,
                "name": "worldcoin-wld",
                "ticker": "WLD",
                "price": 1.62,
                "market_cap": 624935114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 47,
                "name": "wormhole",
                "ticker": "W",
                "price": 0.237456,
                "market_cap": 612423919,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    }
                ]
            },
            {
                "id": 22,
                "name": "mina-protocol",
                "ticker": "MINA",
                "price": 0.485424,
                "market_cap": 555495299,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 1,
                "name": "ethereum",
                "ticker": "ETH",
                "price": 2585.79,
                "market_cap": 311009745811,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            }
        ]
    },
    {
        "id": 9,
        "name": "Coinbase Ventures",
        "cryptocurrencies": [
            {
                "id": 23,
                "name": "matic-network",
                "ticker": "MATIC",
                "price": 0.494203,
                "market_cap": 4588694923,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 6,
                "name": "uniswap",
                "ticker": "UNI",
                "price": 6.05,
                "market_cap": 4563321766,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 8,
                "name": "aptos",
                "ticker": "APT",
                "price": 7.44,
                "market_cap": 3617796488,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 9,
                "name": "sui",
                "ticker": "SUI",
                "price": 0.921594,
                "market_cap": 2394197129,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 30,
                "name": "immutable-x",
                "ticker": "IMX",
                "price": 1.44,
                "market_cap": 2267748806,
                "hedge_funds": [
                    {
                        "id": 5,
                        "name": "Animoca Brands"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 12,
                "name": "arweave",
                "ticker": "AR",
                "price": 24.76,
                "market_cap": 1619911806,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 42,
                "name": "the-graph",
                "ticker": "GRT",
                "price": 0.16086,
                "market_cap": 1536076756,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 25,
                "name": "celestia",
                "ticker": "TIA",
                "price": 5.33,
                "market_cap": 1103614074,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 46,
                "name": "sei-network",
                "ticker": "SEI",
                "price": 0.325749,
                "market_cap": 1074381108,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 14,
                "name": "lido-dao",
                "ticker": "LDO",
                "price": 1.16,
                "market_cap": 1042176575,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 36,
                "name": "ondo-finance",
                "ticker": "ONDO",
                "price": 0.697151,
                "market_cap": 1006521958,
                "hedge_funds": [
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 21,
                "name": "starknet",
                "ticker": "STRK",
                "price": 0.389064,
                "market_cap": 630077766,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 18,
                "name": "worldcoin-wld",
                "ticker": "WLD",
                "price": 1.62,
                "market_cap": 624935114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 22,
                "name": "mina-protocol",
                "ticker": "MINA",
                "price": 0.485424,
                "market_cap": 555495299,
                "hedge_funds": [
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            },
            {
                "id": 5,
                "name": "near",
                "ticker": "NEAR",
                "price": 4.88,
                "market_cap": 5393982890,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    }
                ]
            }
        ]
    },
    {
        "id": 10,
        "name": "Blockchain Capital",
        "cryptocurrencies": [
            {
                "id": 6,
                "name": "uniswap",
                "ticker": "UNI",
                "price": 6.05,
                "market_cap": 4563321766,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 7,
                "name": "internet-computer",
                "ticker": "ICP",
                "price": 8.19,
                "market_cap": 3843379043,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 48,
                "name": "blockstack",
                "ticker": "STX",
                "price": 1.81,
                "market_cap": 2696624236,
                "hedge_funds": [
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 26,
                "name": "filecoin",
                "ticker": "FIL",
                "price": 3.95,
                "market_cap": 2295115611,
                "hedge_funds": [
                    {
                        "id": 4,
                        "name": "Sequoia Capital Portfolio"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 49,
                "name": "aave",
                "ticker": "AAVE",
                "price": 123.54,
                "market_cap": 1842828277,
                "hedge_funds": [
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 12,
                "name": "arweave",
                "ticker": "AR",
                "price": 24.76,
                "market_cap": 1619911806,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 50,
                "name": "theta-token",
                "ticker": "THETA",
                "price": 1.33,
                "market_cap": 1333779729,
                "hedge_funds": [
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 25,
                "name": "celestia",
                "ticker": "TIA",
                "price": 5.33,
                "market_cap": 1103614074,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 18,
                "name": "worldcoin-wld",
                "ticker": "WLD",
                "price": 1.62,
                "market_cap": 624935114,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            },
            {
                "id": 3,
                "name": "ripple",
                "ticker": "XRP",
                "price": 0.597524,
                "market_cap": 33576445782,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 6,
                        "name": "Pantera Capital"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    }
                ]
            }
        ]
    },
    {
        "id": 11,
        "name": "Delphi Digital",
        "cryptocurrencies": [
            {
                "id": 2,
                "name": "solana",
                "ticker": "SOL",
                "price": 155.42,
                "market_cap": 72438447133,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 43,
                "name": "thorchain",
                "ticker": "RUNE",
                "price": 4.22,
                "market_cap": 1412641538,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 25,
                "name": "celestia",
                "ticker": "TIA",
                "price": 5.33,
                "market_cap": 1103614074,
                "hedge_funds": [
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 10,
                        "name": "Blockchain Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 45,
                "name": "pyth-network",
                "ticker": "PYTH",
                "price": 0.298285,
                "market_cap": 1080612872,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 46,
                "name": "sei-network",
                "ticker": "SEI",
                "price": 0.325749,
                "market_cap": 1074381108,
                "hedge_funds": [
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 14,
                "name": "lido-dao",
                "ticker": "LDO",
                "price": 1.16,
                "market_cap": 1042176575,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 2,
                        "name": "Paradigm"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 9,
                        "name": "Coinbase Ventures"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 17,
                "name": "dydx-chain",
                "ticker": "DYDX",
                "price": 1.053,
                "market_cap": 651634598,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 40,
                "name": "ethena",
                "ticker": "ENA",
                "price": 0.292514,
                "market_cap": 528363871,
                "hedge_funds": [
                    {
                        "id": 7,
                        "name": "DragonFly Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            },
            {
                "id": 1,
                "name": "ethereum",
                "ticker": "ETH",
                "price": 2585.79,
                "market_cap": 311009745811,
                "hedge_funds": [
                    {
                        "id": 1,
                        "name": "Andreessen Horowitz"
                    },
                    {
                        "id": 3,
                        "name": "Galaxy Digital"
                    },
                    {
                        "id": 8,
                        "name": "Multicoin Capital"
                    },
                    {
                        "id": 11,
                        "name": "Delphi Digital"
                    }
                ]
            }
        ]
    }
]

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

"indicator_name":  "Fear & Greed Stock Market",

"value":  24,

"created_at":  "August 12, 2024, 02:12 AM"

},

{

"type":  "buy",

"indicator_name":  "Fear & Greed Crypto Market",

"value":  25,

"created_at":  "August 12, 2024, 02:12 AM"

}

],

"sell_recommendations":  []

}

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

