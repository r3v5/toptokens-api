from django.db import connection
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CryptocurrencyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        By default sort the json by market cap in descending order
        """

        query = """
            SELECT c.id AS cryptocurrency_id, c.name AS cryptocurrency_name, c.ticker, c.price, c.market_cap,
                   c.price_dynamics_for_1_year, c.price_dynamics_for_6_months,
                   c.price_dynamics_for_3_months, c.price_dynamics_for_1_month,
                   h.id AS hedge_fund_id, h.name AS hedge_fund_name
            FROM analytic_screener_cryptocurrency AS c
            LEFT JOIN analytic_screener_cryptocurrency_hedge_funds AS chf ON c.id = chf.cryptocurrency_id
            LEFT JOIN analytic_screener_hedgefund AS h ON chf.hedgefund_id = h.id
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Convert rows to a list of dictionaries
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]

            # Organize data into structured format
            result = {}
            for item in data:
                crypto_id = item["cryptocurrency_id"]
                if crypto_id not in result:
                    result[crypto_id] = {
                        "id": crypto_id,
                        "name": item["cryptocurrency_name"],
                        "ticker": item["ticker"],
                        "price": item["price"],
                        "market_cap": item["market_cap"],
                        "price_dynamics_for_1_year": item["price_dynamics_for_1_year"],
                        "price_dynamics_for_6_months": item[
                            "price_dynamics_for_6_months"
                        ],
                        "price_dynamics_for_3_months": item[
                            "price_dynamics_for_3_months"
                        ],
                        "price_dynamics_for_1_month": item[
                            "price_dynamics_for_1_month"
                        ],
                        "hedge_funds": [],
                    }
                if item["hedge_fund_id"]:
                    result[crypto_id]["hedge_funds"].append(
                        {"id": item["hedge_fund_id"], "name": item["hedge_fund_name"]}
                    )

            # Convert result to list
            result_list = list(result.values())

            # Sort by market cap in descending order
            result_list.sort(key=lambda x: x["market_cap"], reverse=True)

            return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PriceDynamics1YAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Filter cryptocurrencies with price dynamics for 1 year and sort price percentage change in descending order.
        """

        query = """
            SELECT c.id AS cryptocurrency_id, c.name AS cryptocurrency_name, c.ticker, c.price, c.market_cap,
                   c.price_dynamics_for_1_year,
                   h.id AS hedge_fund_id, h.name AS hedge_fund_name
            FROM analytic_screener_cryptocurrency AS c
            LEFT JOIN analytic_screener_cryptocurrency_hedge_funds AS chf ON c.id = chf.cryptocurrency_id
            LEFT JOIN analytic_screener_hedgefund AS h ON chf.hedgefund_id = h.id
            WHERE c.price_dynamics_for_1_year IS NOT NULL
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]

            # Organize data into structured format
            result = {}
            for item in data:
                crypto_id = item["cryptocurrency_id"]
                if crypto_id not in result:
                    result[crypto_id] = {
                        "id": crypto_id,
                        "name": item["cryptocurrency_name"],
                        "ticker": item["ticker"],
                        "price": item["price"],
                        "market_cap": item["market_cap"],
                        "price_dynamics_for_1_year": item["price_dynamics_for_1_year"],
                        "hedge_funds": [],
                    }
                if item["hedge_fund_id"]:
                    result[crypto_id]["hedge_funds"].append(
                        {"id": item["hedge_fund_id"], "name": item["hedge_fund_name"]}
                    )

            # Convert result to list
            result_list = list(result.values())

            # Sort by price dynamics for 1 year in descending order
            result_list.sort(
                key=lambda x: (x["price_dynamics_for_1_year"]),
                reverse=True,
            )

            return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class CryptocurrencyDetailAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         query = """
#             SELECT c.id AS cryptocurrency_id, c.name AS cryptocurrency_name, c.ticker, c.price, c.market_cap,
#                    c.price_dynamics_for_1_year, c.price_dynamics_for_6_months,
#                    c.price_dynamics_for_3_months, c.price_dynamics_for_1_month,
#                    h.id AS hedge_fund_id, h.name AS hedge_fund_name
#             FROM analytic_screener_cryptocurrency AS c
#             LEFT JOIN analytic_screener_cryptocurrency_hedge_funds AS chf ON c.id = chf.cryptocurrency_id
#             LEFT JOIN analytic_screener_hedgefund AS h ON chf.hedgefund_id = h.id
#             WHERE c.id = %s
#         """

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, [pk])
#                 row = cursor.fetchone()

#             if not row:
#                 return Response(
#                     {"error": "Cryptocurrency not found"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # Convert row to a dictionary
#             columns = [col[0] for col in cursor.description]
#             data = dict(zip(columns, row))

#             # Organize data into structured format
#             result = {
#                 "id": data["cryptocurrency_id"],
#                 "name": data["cryptocurrency_name"],
#                 "ticker": data["ticker"],
#                 "price": data["price"],
#                 "market_cap": data["market_cap"],
#                 "price_dynamics_for_1_year": data["price_dynamics_for_1_year"],
#                 "price_dynamics_for_6_months": data["price_dynamics_for_6_months"],
#                 "price_dynamics_for_3_months": data["price_dynamics_for_3_months"],
#                 "price_dynamics_for_1_month": data["price_dynamics_for_1_month"],
#                 "hedge_funds": [],
#             }

#             if data["hedge_fund_id"]:
#                 result["hedge_funds"].append(
#                     {"id": data["hedge_fund_id"], "name": data["hedge_fund_name"]}
#                 )

#             return Response(result, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HedgeFundsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        query = """
            SELECT h.id AS hedge_fund_id, h.name AS hedge_fund_name,
                   c.id AS cryptocurrency_id, c.name AS cryptocurrency_name, c.ticker, c.price, c.market_cap,
                   c.price_dynamics_for_1_year, c.price_dynamics_for_6_months,
                   c.price_dynamics_for_3_months, c.price_dynamics_for_1_month
            FROM analytic_screener_hedgefund AS h
            LEFT JOIN analytic_screener_cryptocurrency_hedge_funds AS chf ON h.id = chf.hedgefund_id
            LEFT JOIN analytic_screener_cryptocurrency AS c ON chf.cryptocurrency_id = c.id
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            if not rows:
                return Response(
                    {"error": "No hedge funds found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Convert rows to a list of dictionaries
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]

            # Organize data into structured format
            result = {}
            for item in data:
                hedge_fund_id = item["hedge_fund_id"]
                if hedge_fund_id not in result:
                    result[hedge_fund_id] = {
                        "id": hedge_fund_id,
                        "name": item["hedge_fund_name"],
                        "cryptocurrencies": [],
                    }
                if item["cryptocurrency_id"]:
                    result[hedge_fund_id]["cryptocurrencies"].append(
                        {
                            "id": item["cryptocurrency_id"],
                            "name": item["cryptocurrency_name"],
                            "ticker": item["ticker"],
                            "price": item["price"],
                            "market_cap": item["market_cap"],
                            "price_dynamics_for_1_year": item[
                                "price_dynamics_for_1_year"
                            ],
                            "price_dynamics_for_6_months": item[
                                "price_dynamics_for_6_months"
                            ],
                            "price_dynamics_for_3_months": item[
                                "price_dynamics_for_3_months"
                            ],
                            "price_dynamics_for_1_month": item[
                                "price_dynamics_for_1_month"
                            ],
                        }
                    )

            # Convert result to list
            result_list = list(result.values())

            return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class HedgeFundsDetailAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         query = """
#             SELECT h.id AS hedge_fund_id, h.name AS hedge_fund_name,
#                    c.id AS cryptocurrency_id, c.name AS cryptocurrency_name, c.ticker, c.price, c.market_cap,
#                    c.price_dynamics_for_1_year, c.price_dynamics_for_6_months,
#                    c.price_dynamics_for_3_months, c.price_dynamics_for_1_month
#             FROM analytic_screener_hedgefund AS h
#             LEFT JOIN analytic_screener_cryptocurrency_hedge_funds AS chf ON h.id = chf.hedgefund_id
#             LEFT JOIN analytic_screener_cryptocurrency AS c ON chf.cryptocurrency_id = c.id
#             WHERE h.id = %s
#         """

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, [pk])
#                 rows = cursor.fetchall()

#             if not rows:
#                 return Response(
#                     {"error": "Hedge fund not found"}, status=status.HTTP_404_NOT_FOUND
#                 )

#             # Convert rows to a list of dictionaries
#             columns = [col[0] for col in cursor.description]
#             data = [dict(zip(columns, row)) for row in rows]

#             # Organize data into structured format
#             result = {
#                 "id": data[0]["hedge_fund_id"],
#                 "name": data[0]["hedge_fund_name"],
#                 "cryptocurrencies": [],
#             }

#             for item in data:
#                 if item["cryptocurrency_id"]:
#                     result["cryptocurrencies"].append(
#                         {
#                             "id": item["cryptocurrency_id"],
#                             "name": item["cryptocurrency_name"],
#                             "ticker": item["ticker"],
#                             "price": item["price"],
#                             "market_cap": item["market_cap"],
#                             "price_dynamics_for_1_year": item[
#                                 "price_dynamics_for_1_year"
#                             ],
#                             "price_dynamics_for_6_months": item[
#                                 "price_dynamics_for_6_months"
#                             ],
#                             "price_dynamics_for_3_months": item[
#                                 "price_dynamics_for_3_months"
#                             ],
#                             "price_dynamics_for_1_month": item[
#                                 "price_dynamics_for_1_month"
#                             ],
#                         }
#                     )

#             return Response(result, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
