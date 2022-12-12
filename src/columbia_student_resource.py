import pymysql
from os import getenv


class ColumbiaStudentResource:

    def __init__(self):
        pass

    @staticmethod
    def _get_connection():
        conn = pymysql.connect(
            user="admin",
            password="12345678",
            host="coms-6156-contacts.cjpbkidulxni.us-east-1.rds.amazonaws.com",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_params(params):
        limit, offset = 10, 0
        if "limit" in params:
            limit = int(params["limit"])
        if "page" in params:
            offset = (int(params["page"]) - 1) * limit
        where_clause = []
        where_params = []
        if "uni" in params:
            where_clause.append("uni=%s")
            where_params.append(params["uni"])
        if "name" in params:
            where_clause.append("name=%s")
            where_params.append(params["name"])
        if "email" in params:
            where_clause.append("email=%s")
            where_params.append(params["email"])
        if "phone" in params:
            where_clause.append("phone=%s")
            where_params.append(params["phone"])
        if "address" in params:
            where_clause.append("address=%s")
            where_params.append(params["address"])
        conn = ColumbiaStudentResource()._get_connection()
        cur = conn.cursor()
        if not where_params:
            sql = "SELECT * FROM contacts.contacts LIMIT %s OFFSET %s"
            cur.execute(sql, (limit, offset))
        else:
            sql = "SELECT * FROM contacts.contacts WHERE " + " AND ".join(where_clause) + " LIMIT %s OFFSET %s"
            cur.execute(sql, where_params + [limit, offset])
        result = cur.fetchall()
        conn.close()
        return result


    @staticmethod
    def get_by_key(key):
        sql = "SELECT * FROM contacts.contacts where uni=%s";
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=key)
        result = cur.fetchone()
        conn.close()

        return result

    @staticmethod
    def update_by_key(uni, contact):
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        content = []
        if "name" in contact:
            content.append("name = \"" + contact["name"] + "\"")
        if "email" in contact:
            content.append("email = \"" + contact["email"] + "\"")
        if "phone" in contact:
            content.append("phone = \"" + contact["phone"] + "\"")
        if "address" in contact:
            content.append("address = \"" + contact["address"] + "\"")

        sql = "UPDATE contacts.contacts SET " + ", ".join(content) + " WHERE uni = %s"
        res = cur.execute(sql, args=uni)
        result = cur.fetchone()
        conn.close()

        return result

    @staticmethod
    def insert_by_key(contact):
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        if "uni" not in contact:
            raise ValueError("No UNI")
        uni = contact["uni"] if "uni" in contact else ""
        name = contact["name"] if "name" in contact else ""
        email = contact["email"] if "email" in contact else ""
        phone = contact["phone"] if "phone" in contact else ""
        address = contact["address"] if "address" in contact else ""
        sql = "INSERT INTO contacts.contacts (uni, name, email, phone, address) " \
              "VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, args=(uni, name, email, phone, address))
        result = cur.fetchone()
        conn.close()

        return result

    @staticmethod
    def delete_by_key(uni):
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        sql = "DELETE FROM contacts.contacts WHERE uni = %s"
        cur.execute(sql, args=uni)
        conn.close()
        return
