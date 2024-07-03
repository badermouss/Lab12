from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Country
                    from go_sales.go_retailers gr 
                    order by Country asc
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_sales.go_retailers gr 
                    where gr.Country = %s 
                """

        cursor.execute(query, (country, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(country, year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gds.Retailer_code AS r1, gds2.Retailer_code AS r2, COUNT(DISTINCT gds.Product_number) AS peso
                    FROM go_sales.go_daily_sales gds, go_sales.go_daily_sales gds2, go_sales.go_retailers gr1 , go_sales.go_retailers gr2 
                    where YEAR(gds.`Date`) = %s AND YEAR(gds2.`Date`) = %s
                    and gr1.Country = %s  and gr2.Country = %s
                    AND gr1.Retailer_code < gr2.Retailer_code
                    AND gds.Product_number = gds2.Product_number
                    and gds.Retailer_code = gr1.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code 
                    group by r1, r2
                """

        cursor.execute(query, (year, year, country, country, ))

        for row in cursor:
            result.append((idMap[row["r1"]], idMap[row["r2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result


