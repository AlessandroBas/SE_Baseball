from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    @staticmethod
    def read_team_salary(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT team_id, SUM(salary) AS total
                    FROM salary
                    WHERE year = %s
                    GROUP BY team_id"""

        cursor.execute(query, (year,))
        result = {row["team_id"]: row["total"] for row in cursor}
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_team_by_year(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, team_code, name
                    FROM team
                    WHERE year = %s"""

        cursor.execute(query, (year,))
        teams = [Team(row["id"], row["team_code"], row["name"]) for row in cursor]
        cursor.close()
        conn.close()
        return teams
    @staticmethod
    def read_year():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT t.year
                    FROM team t
                    WHERE t.year>1980"""
        cursor.execute(query)
        result=[row["year"] for row in cursor]
        cursor.close()
        conn.close()
        return result