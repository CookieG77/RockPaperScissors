"""Module for database utilities."""

import sqlite3
import hashlib
import os

class Database:
    """Generic database class."""

    def __init__(self, db_name : str, pepper : str = "") -> None:
        """Initialize the database connection."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.pepper = pepper
        if pepper:
            self.has_pepper = True
        else:
            self.has_pepper = False

    def create_table(self, table_name : str, columns : dict) -> None:
        """
        Create a table with the given name and columns.
        
        Args:
            table_name (str): Name of the table to create.
            columns (dict): Dictionary of column names and their data types.            
        Example:
            db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
                
            --> Creates a table named 'users' with the specified columns : id (INTEGER PRIMARY KEY), name (TEXT), age (INTEGER).
        """
        cols = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")
        self.conn.commit()

    def insert(self, table_name : str, data: dict) -> None:
        """
        Insert data into the specified table.
        
        Args:
            table_name (str): Name of the table to insert data into.
            data (dict): Dictionary of column names and their values.
            
        Example:
            db.insert("users", {"name": "Alice", "age": 30})
                
            --> Inserts a new row into the 'users' table with name 'Alice' and age 30.
        """

        self.cursor.execute(
            f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(['?' for _ in data])})",
            tuple(data.values())
        )

    def execute(self, query : str, params : tuple = ()) -> list:
        """
        Execute a raw SQL query.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple): Optional parameters for the SQL query.
            
        Returns:
            list: The result of the query.
            
        Example:
            results = db.execute("SELECT * FROM users WHERE age > ?", (25,))
                
            --> Executes the query and returns all users older than 25.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self) -> None:
        """Close the database connection."""
        self.conn.commit()
        self.conn.close()

    def _hash(self, value : str, salt : str = "") -> str:
        """Hash a value with optional salt and pepper using SHA-512."""
        if self.has_pepper:
            value += self.pepper
        if salt:
            value += salt
        return hashlib.sha256(value.encode()).hexdigest()

    def __str__(self) -> str:
        """String representation of the database connection."""
        return f"Database connection: {self.conn}"

    def print_database_info(self) -> None:
        """Print information about the database tables and their contents."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [t[0] for t in self.cursor.fetchall()]

        header = f"\033[93mDatabase connection\033[0m: {self.conn}\n\033[32mTables\033[0m:\n"
        output_lines = [header]

        if not tables:
            output_lines.append("  (no user tables found)\n")
            print(''.join(output_lines))
            return

        for table_name in tables:
            output_lines.append(f"  \033[96mTable\033[0m: {table_name}\n")

            # Get column info
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            col_names = [col[1] for col in columns]

            if not col_names:
                output_lines.append("  (no columns)\n")
                continue

            # Fetch rows
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()

            # Compute column widths: consider column names and all values as strings
            col_widths = [len(name) for name in col_names]
            for row in rows:
                for i, val in enumerate(row):
                    s = str(val)
                    if len(s) > col_widths[i]:
                        col_widths[i] = len(s)

            # Build format string
            sep = ' | '
            header_cells = [name.ljust(col_widths[i]) for i, name in enumerate(col_names)]
            header_line = '  ' + sep.join(header_cells) + '\n'
            output_lines.append(header_line)

            # separator underline
            underline_cells = ['-' * col_widths[i] for i in range(len(col_names))]
            output_lines.append('  ' + sep.join(underline_cells) + '\n')

            # rows
            if rows:
                for row in rows:
                    row_cells = [str(row[i]).ljust(col_widths[i]) for i in range(len(col_names))]
                    output_lines.append('  ' + sep.join(row_cells) + '\n')
            else:
                output_lines.append('  (no rows)\n')

            output_lines.append('\n')

        print(''.join(output_lines))


class RPSDatabase(Database):
    """Class for managing the RPS game database."""

    db = None

    def __init__(self, db_name : str = "rps_game.db"):
        """Initialize the RPS database."""
        pepper = os.getenv("pepper")
        if not pepper:
            pepper = ""
        super().__init__(db_name, pepper=pepper)
        RPSDatabase.db = self
        self._init_tables()

    def _init_tables(self) -> None:
        """Initialize the required tables for the RPS game."""
        self.create_table("users", {
            "id": "INTEGER PRIMARY KEY",
            "gamertag": "TEXT",
            "hashed_password": "TEXT",
            "salt": "TEXT"
        })
        self.create_table("scores", {
            "user_id": "INTEGER",
            "victories": "INTEGER",
            "defeats": "INTEGER",
            "FOREIGN KEY(user_id)": "REFERENCES users(id)"
        })

    def insert_user(self, gamertag : str, password : str, salt : str) -> None:
        """Insert a new user into the users table."""
        hashed_password = self._hash(password, salt)
        self.insert("users", {"gamertag": gamertag, "hashed_password": hashed_password, "salt": salt})
        self.insert("scores", {"user_id": self.cursor.lastrowid, "victories": 0, "defeats": 0})

    def add_victory(self, user_id : int) -> None:
        """Increment the victory count for a user."""
        self.execute("UPDATE scores SET victories = victories + 1 WHERE user_id = ?", (user_id,))

    def add_defeat(self, user_id : int) -> None:
        """Increment the defeat count for a user."""
        self.execute("UPDATE scores SET defeats = defeats + 1 WHERE user_id = ?", (user_id,))

    def get_user_scores(self, user_id : int) -> tuple[int, int]:
        """Get the victory and defeat counts for a user."""
        self.cursor.execute("SELECT victories, defeats FROM scores WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone() or (0, 0)

    def check_user_credentials_by_gamertag(self, gamertag : str, password : str) -> bool:
        """Check if the provided gamertag and password match a user in the database."""
        self.cursor.execute("SELECT hashed_password, salt FROM users WHERE gamertag = ?", (gamertag,))
        result = self.cursor.fetchone()
        if result:
            stored_hashed_password, salt = result
            return stored_hashed_password == self._hash(password, salt)
        return False

    def check_user_credentials_by_id(self, user_id: int, password: str) -> bool:
        """Check if the provided user ID and password match a user in the database."""
        self.cursor.execute("SELECT hashed_password, salt FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            stored_hashed_password, salt = result
            return stored_hashed_password == self._hash(password, salt)
        return False

    def close(self) -> None:
        """Close the RPS database connection."""
        super().close()
        RPSDatabase.db = None
