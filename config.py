import urllib

# Cấu hình thông tin SQL Server
SQL_SERVER = "THANHTIN"  # Tên server
SQL_DATABASE = "khoaluantotnghiep"  # Tên database

# Kết nối dùng Windows Authentication
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(
    f"DRIVER={{SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};Trusted_Connection=yes;"
)
