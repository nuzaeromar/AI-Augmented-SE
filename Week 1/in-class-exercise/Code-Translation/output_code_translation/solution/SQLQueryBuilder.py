class SQLQueryBuilder:
    @staticmethod
<<<<<<< Updated upstream
    def select(table, columns=None, where=None):
        if columns is None:
            columns = ["*"]
        if where is None:
            where = []
        query = []
        if len(columns) == 1 and columns[0] == "*":
            query.append("SELECT *")
        else:
            query.append("SELECT " + ", ".join(columns))
        query.append(f" FROM {table}")
        if where:
            query.append(" WHERE " + " AND ".join([f"{key}='{value}'" for key, value in where]))
        return "".join(query)

    @staticmethod
    def insert(table, data):
        query = []
        query.append(f"INSERT INTO {table} (")
        query.append(", ".join([item[0] for item in data]))
        query.append(") VALUES (")
        query.append(", ".join([f"'{item[1]}'" for item in data]))
        query.append(")")
        return "".join(query)

    @staticmethod
    def delete_(table, where=None):
        if where is None:
            where = []
        query = []
        query.append(f"DELETE FROM {table}")
        if where:
            query.append(" WHERE " + " AND ".join([f"{item[0]}='{item[1]}'" for item in where]))
        return "".join(query)

    @staticmethod
    def update(table, data, where=None):
        if where is None:
            where = []
        query = []
        query.append(f"UPDATE {table} SET ")
        query.append(", ".join([f"{item[0]}='{item[1]}'" for item in data]))
        if where:
            query.append(" WHERE " + " AND ".join([f"{item[0]}='{item[1]}'" for item in where]))
        return "".join(query)
=======
    def _format_columns(columns):
        if not columns:
            return "*"
        if isinstance(columns, (list, tuple)):
            return ", ".join(str(col) for col in columns)
        # fallback to string representation
        return str(columns)

    @staticmethod
    def _format_where(where):
        if not where:
            return ""
        clauses = []
        if isinstance(where, dict):
            for k, v in where.items():
                clauses.append(f"{k}='{v}'")
        else:
            # assume iterable of (key, value)
            for k, v in where:
                clauses.append(f"{k}='{v}'")
        return " WHERE " + " AND ".join(clauses)

    @staticmethod
    def select(table, columns=None, where=None):
        if columns is None:
            columns = ["*"]
        col_part = SQLQueryBuilder._format_columns(columns)
        query = f"SELECT {col_part} FROM {table}"
        query += SQLQueryBuilder._format_where(where)
        return query

    @staticmethod
    def insert(table, data):
        # data can be dict or iterable of (key, value)
        if isinstance(data, dict):
            keys = list(data.keys())
            values = [f"'{v}'" for v in data.values()]
        else:
            # assume list of pairs
            keys = [k for k, _ in data]
            values = [f"'{v}'" for _, v in data]
        cols = ", ".join(keys)
        vals = ", ".join(values)
        query = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
        return query

    @staticmethod
    def delete_(table, where=None):
        query = f"DELETE FROM {table}"
        query += SQLQueryBuilder._format_where(where)
        return query

    @staticmethod
    def update(table, data, where=None):
        # data can be dict or iterable of (key, value)
        if isinstance(data, dict):
            set_parts = [f"{k}='{v}'" for k, v in data.items()]
        else:
            set_parts = [f"{k}='{v}'" for k, v in data]
        set_clause = ", ".join(set_parts)
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            query += SQLQueryBuilder._format_where(where)
        return query
>>>>>>> Stashed changes
