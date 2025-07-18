from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime
import time
from enum import Enum, auto
from typing import Optional, Union, List, Tuple

import secrets
import hashlib

import logging

from utils import verify_email_format
from cus_exceptions import (
    DuplicatedAccountBookError,
    EmailFormatError,
    IncomeValueError,
    InvalidOutcomeIncomeValueError,
    OutcomeValueError,
    PasswordWrongError,
    RequireInfoLostException,
    TokenExpireException,
    PwdNotMatchError,
    TokenNotFoundError,
)

DB_PATH = Path(__file__).parent / ".." / "db" / "account.db"
DB_PATH.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(name)s - %(levelname)s] - %(message)s",
)


class IncomeType(Enum):
    SALARY = auto()
    BONUS = auto()
    INVEST = auto()
    OTHER = auto()

    @staticmethod
    def index_2_income_type(idx: int) -> IncomeType:
        return IncomeType(idx) if 0 <= idx < len(IncomeType) else IncomeType.OTHER

    @staticmethod
    def index_2_income_type_name(idx: int) -> str:
        return (
            IncomeType.index_2_income_type(idx).name
            if 0 <= idx < len(IncomeType)
            else "OTHER"
        )


class OutcomeType(Enum):
    FOOD = auto()
    RENT = auto()
    TRANSPORT = auto()
    ENTERTAIN = auto()
    OTHER = auto()

    @staticmethod
    def index_2_outcome_type(idx: int) -> OutcomeType:
        return OutcomeType(idx) if 0 <= idx < len(OutcomeType) else OutcomeType.OTHER

    @staticmethod
    def index_2_outcome_type_name(idx: int) -> str:
        return (
            OutcomeType.index_2_outcome_type(idx).name
            if 0 <= idx < len(OutcomeType)
            else "OTHER"
        )


class DebtType(Enum):
    LOAN = auto()
    CREDIT_CARD = auto()


class Transaction:
    def __init__(
        self,
        amount: float,
        account_book_id: int,
        category: Optional[Union[IncomeType, OutcomeType]] = None,
        time: Optional[datetime] = None,
        note: str = "",
        id: Optional[int] = None,
    ) -> None:
        """
        Initialize a Transaction record.

        Args:
            amount: The transaction amount (positive for income, negative for expense).
            account_book_id: The ID of the account book this transaction belongs to.
            category: An IncomeType (if amount >= 0) or OutcomeType (if amount < 0) categorizing the transaction.
            time: The datetime of the transaction (defaults to now if None).
            note: An optional note or description for the transaction.
            id: The transaction ID (primary key), if known (used when loading from the database).
        """
        self.amount = amount
        self.account_book_id = account_book_id
        self.time = time if time is not None else datetime.now()
        self.note = note
        self.id = id
        self.category = category
        # Validate that category is provided and matches the sign of amount
        try:
            if isinstance(self.category, IncomeType) and self.amount < 0:
                raise IncomeValueError(
                    "the income should be an float or int and it should be positive"
                )
            elif isinstance(self.category, OutcomeType) and self.amount >= 0:
                raise OutcomeValueError(
                    "the outcome should be an float or int and it should be negative"
                )
        except ValueError as e:
            raise InvalidOutcomeIncomeValueError(
                "the outcome or income value should be a float or int, consider parsing bugs"
            )

    @staticmethod
    def execute_db_add(conn: sqlite3.Connection, tx: Transaction) -> Optional[int]:
        """
        Add a new transaction to the database.

        Args:
            conn: The open sqlite3.Connection object.
            tx: The Transaction object to insert (must have category set).

        Returns:
            int: The auto-generated ID of the new transaction.
        """
        sql = """
            INSERT INTO transactions (
                account_book_id,
                amount,
                time,
                note,
                category
            ) VALUES (?, ?, ?, ?, ?)
        """
        cur = conn.execute(
            sql,
            (
                tx.account_book_id,
                tx.amount,
                tx.time.isoformat(timespec="seconds"),
                tx.note,
                tx.category.name if tx.category is not None else None,
            ),
        )
        conn.commit()
        tx.id = cur.lastrowid
        return tx.id

    @staticmethod
    def execute_db_remove(
        conn: sqlite3.Connection, remove_transaction_ids: Union[int, List[int]]
    ) -> int:
        """
        Deletes one or more transaction records.

        Args:
            conn: sqlite3.Connection
            remove_transaction_ids: A single transaction ID or a list of IDs to remove.

        Returns:
            int: The number of rows actually deleted.
        """
        if isinstance(remove_transaction_ids, int):
            ids: Tuple[int, ...] = (remove_transaction_ids,)
        else:
            ids = tuple(set(remove_transaction_ids))
        if not ids:
            return 0
        placeholders = ",".join("?" for _ in ids)
        sql = f"DELETE FROM transactions WHERE id IN ({placeholders})"
        cursor = conn.execute(sql, ids)
        conn.commit()
        return cursor.rowcount

    @staticmethod
    def execute_db_query(
        conn: sqlite3.Connection,
        account_book_id: int,
        transaction_id: Optional[int] = None,
        time: Optional[datetime] = None,
        note: Optional[str] = None,
        account_name: Optional[str] = None,
        account_book_name: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Query transactions with optional filters. Returns a list of Transaction objects.
        """
        sql = """
            SELECT t.id, t.amount, t.time, t.note, t.category
            FROM transactions AS t
            JOIN account_books AS ab ON t.account_book_id = ab.account_book_id
            JOIN accounts AS a ON ab.account_id = a.account_id
            WHERE 1 = 1
        """
        params: List = []
        if account_book_id is not None:
            sql += " AND t.account_book_id = ?"
            params.append(account_book_id)
        if transaction_id is not None:
            sql += " AND t.id = ?"
            params.append(transaction_id)
        if time is not None:
            sql += " AND DATE(t.time) = DATE(?)"
            params.append(time.isoformat())
        if note is not None:
            sql += " AND t.note LIKE ?"
            params.append(f"%{note}%")
        if account_name is not None:
            sql += " AND a.name = ?"
            params.append(account_name)
        if account_book_name is not None:
            sql += " AND ab.name = ?"
            params.append(account_book_name)
        rows = conn.execute(sql, params).fetchall()
        result: List[Transaction] = []
        for row in rows:
            tx_id, amount, t_time, t_note, t_category = row
            # Determine category enum from stored name and amount sign
            if t_category is None:
                category_enum = None
            else:
                category_name: str = t_category  # e.g., "SALARY" or "FOOD"
                if amount >= 0:
                    category_enum = IncomeType[category_name]
                else:
                    category_enum = OutcomeType[category_name]
            result.append(
                Transaction(
                    amount=amount,
                    account_book_id=account_book_id,
                    time=datetime.fromisoformat(t_time),
                    note=t_note,
                    category=category_enum,
                    id=tx_id,
                )
            )
        return result


def _hash_pwd(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()


def _gen_token() -> str:
    # 32 字节 -> 64 位十六进制字符串
    return secrets.token_hex(32)


class Account:
    id: int
    name: str
    email: str  # 新增
    pwd_hash: str
    token: str  # 新增
    books: List[AccountBook]

    # ------------------------- 构造器 ------------------------- #
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        pwd_hash: str,
        token: str,
        books: Optional[List[AccountBook]] = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.pwd_hash = pwd_hash
        self.token = token
        self.books = books or []

    # ------------------------- 账号注册 ------------------------ #
    @staticmethod
    def register(
        conn: sqlite3.Connection, name: str, email: str, pwd_hash: str
    ) -> bool:
        if not verify_email_format(email):
            raise EmailFormatError("Invalid email format")

        token = _gen_token()
        cur = conn.execute(
            "INSERT INTO accounts (name, email, pwd, token) VALUES (?, ?, ?, ?)",
            (name, email, pwd_hash, token),
        )
        conn.commit()
        acc_id = cur.lastrowid
        if acc_id is None:
            raise RuntimeError("Failed to create account, no ID returned.")
        logging.info(f"Account created with ID: {acc_id}, Name: {name}, Email: {email}")
        return Account(acc_id, name, email, pwd_hash, token, books=[]) is not None

    # ------------------------- 密码登录 ------------------------ #
    @staticmethod
    def login(
        conn: sqlite3.Connection, name_or_email: str, pwd_hash: str
    ) -> Optional["Account"]:
        import secrets

        row = conn.execute(
            """
            SELECT account_id, name, email, pwd, token
            FROM accounts
            WHERE name = ? OR email = ?
            """,
            (name_or_email, name_or_email),
        ).fetchone()
        if not row:
            return None
        acc_id, name, email, db_hash, _ = row
        if pwd_hash != db_hash:
            raise PwdNotMatchError(
                "Invalid password hash code, consider using wrong password or hash compute error"
            )
        # Generate new token and expire time
        new_token = secrets.token_urlsafe(32)
        expire = int(time.time()) + 3600 * 24 * 15  #  15 day expiry
        conn.execute(
            "UPDATE accounts SET token = ?, token_expire = ? WHERE account_id = ?",
            (new_token, expire, acc_id),
        )
        conn.commit()
        books = Account._load_books(conn, acc_id)
        return Account(acc_id, name, email, db_hash, new_token, books)

    # ------------------------- Token 登录 --------------------- #
    @staticmethod
    def login_by_token(conn: sqlite3.Connection, token: str) -> Optional["Account"]:
        row = conn.execute(
            "SELECT account_id, name, email, pwd, token FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if not row:
            return None
        acc_id, name, email, pwd_hash, token = row
        books = Account._load_books(conn, acc_id)
        return Account(acc_id, name, email, pwd_hash, token, books)

    @staticmethod
    def refresh_token(conn: sqlite3.Connection, old_token: str) -> Optional["Account"]:
        import secrets

        row = conn.execute(
            """
            SELECT account_id, name, email, pwd, token, token_expire
            FROM accounts
            WHERE token = ?
            """,
            (old_token,),
        ).fetchone()
        if not row:
            return None
        acc_id, name, email, db_hash, token, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired")
        # 生成新 token 和过期时间
        new_token = secrets.token_urlsafe(32)
        expire = now + 3600 * 24 * 15  # 15 day expire
        conn.execute(
            "UPDATE accounts SET token = ?, token_expire = ? WHERE account_id = ?",
            (new_token, expire, acc_id),
        )
        conn.commit()
        books = Account._load_books(conn, acc_id)
        return Account(acc_id, name, email, db_hash, new_token, books)

    @staticmethod
    def logout(conn: sqlite3.Connection, token: str) -> bool:
        row = conn.execute(
            "SELECT account_id, token_expire FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if not row:
            raise TokenNotFoundError("Token not found")
        account_id, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            return True
        # 使 token 立即过期
        conn.execute(
            "UPDATE accounts SET token_expire = ? WHERE account_id = ?",
            (now - 1, account_id),
        )
        conn.commit()
        return True

    @staticmethod
    def get_profile(conn: sqlite3.Connection, token: str) -> "Account":
        row = conn.execute(
            "SELECT account_id, name, email, pwd, token, token_expire FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if not row:
            raise TokenNotFoundError("Token not found")
        acc_id, name, email, pwd_hash, token, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired")
        books = Account._load_books(conn, acc_id)
        return Account(acc_id, name, email, pwd_hash, token, books)

    # ------------------------- 其它接口（基本保持不变） -------- #
    @staticmethod
    def create_book(
        conn: sqlite3.Connection, token: str, book_name: str
    ) -> AccountBook:
        if book_name is None or book_name.strip() == "":
            raise RequireInfoLostException("Book name is required.")
        cur = conn.execute(
            "SELECT account_id, token_expire FROM accounts WHERE token = ?",
            (token,),
        )
        row = cur.fetchone()
        if row is None:
            raise TokenNotFoundError("Token not found.")
        account_id, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired.")
        dup_cur = conn.execute(
            "SELECT 1 FROM account_books WHERE name = ? AND account_id = ?",
            (book_name, account_id),
        )
        if dup_cur.fetchone() is not None:
            raise DuplicatedAccountBookError(
                "Account book name already exists for this account."
            )
        cur = conn.execute(
            "INSERT INTO account_books (name, account_id) VALUES (?, ?)",
            (book_name, account_id),
        )
        conn.commit()
        book_id = cur.lastrowid
        if book_id is None:
            raise RuntimeError("Failed to create account book, no ID returned.")
        return AccountBook(id=book_id, name=book_name, account_id=account_id)

    @staticmethod
    def list_books(conn: sqlite3.Connection, token: str) -> List[AccountBook]:
        row = conn.execute(
            "SELECT account_id, token_expire FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if row is None:
            raise TokenNotFoundError("Token not found.")
        account_id, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired.")
        return Account._load_books(conn, account_id)

    @staticmethod
    def remove_account_book(conn: sqlite3.Connection, token: str, book_id: int) -> bool:
        # Check token validity and expiry
        row = conn.execute(
            "SELECT account_id, token_expire FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if row is None:
            raise TokenNotFoundError("Token not found.")
        account_id, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired.")
        # Check if the account_book belongs to the account
        book_row = conn.execute(
            "SELECT 1 FROM account_books WHERE account_book_id = ? AND account_id = ?",
            (book_id, account_id),
        ).fetchone()
        if book_row is None:
            raise RuntimeError(
                "Account book not found or does not belong to this account."
            )
        # Remove the account_book
        conn.execute(
            "DELETE FROM account_books WHERE account_book_id = ?",
            (book_id,),
        )
        conn.commit()
        return True

    @staticmethod
    def change_pwd(
        conn: sqlite3.Connection,
        email_or_name: str,
        old_pwd_hash: str,
        new_pwd_hash: str,
    ) -> bool:
        row = conn.execute(
            "SELECT account_id, pwd FROM accounts WHERE name = ? OR email = ?",
            (email_or_name, email_or_name),
        ).fetchone()
        if not row or row[1] != old_pwd_hash:
            raise PasswordWrongError
        account_id = row[0]
        conn.execute(
            "UPDATE accounts SET pwd = ? WHERE account_id = ?",
            (new_pwd_hash, account_id),
        )
        conn.commit()
        return True

    @staticmethod
    def _load_books(conn: sqlite3.Connection, account_id: int) -> List[AccountBook]:
        rows = conn.execute(
            "SELECT account_book_id, name FROM account_books WHERE account_id = ?",
            (account_id,),
        ).fetchall()
        print(rows)
        return [AccountBook(id=r[0], name=r[1], account_id=account_id) for r in rows]


class AccountBook:
    def __init__(self, id: int, name: str, account_id: int):
        """
        Initialize an AccountBook instance.
        """
        self._id = id
        self.name = name
        self.account_id = account_id
        self._transactions: List[
            Transaction
        ] = []  # Initialize empty list of transactions

    def __eq__(self, other: object) -> bool:
        """Determine equality based on AccountBook ID."""
        if not isinstance(other, AccountBook):
            return False
        return self._id == other._id

    @staticmethod
    def verify_book_ownership(
        conn: sqlite3.Connection,
        token: str,
        account_book_id: int,
    ) -> bool:
        """
        Verify if the account book belongs to the account associated with the token.
        Raises TokenNotFoundError or TokenExpireException if token is invalid/expired.
        Returns True if ownership is verified, otherwise raises RuntimeError.
        """
        row = conn.execute(
            "SELECT account_id, token_expire FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if row is None:
            raise TokenNotFoundError("Token not found.")
        account_id, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired.")
        book_row = conn.execute(
            "SELECT 1 FROM account_books WHERE account_book_id = ? AND account_id = ?",
            (account_book_id, account_id),
        ).fetchone()
        if book_row is None:
            raise RuntimeError(
                "Account book not found or does not belong to this account."
            )
        return True

    @staticmethod
    def add_income(
        conn: sqlite3.Connection,
        token: str,
        account_book_id: int,
        amount: float,
        time: Optional[datetime],
        note: str = "",
        income_type: IncomeType = IncomeType.OTHER,
    ) -> None:
        """
        Add an income transaction to the account book.
        """
        # Verify ownership
        AccountBook.verify_book_ownership(conn, token, account_book_id)
        tx = Transaction(
            amount=amount,
            account_book_id=account_book_id,
            category=income_type,
            time=time,
            note=note,
        )
        Transaction.execute_db_add(conn, tx)  # This will commit the transaction

    @staticmethod
    def add_outcome(
        conn: sqlite3.Connection,
        token: str,
        account_book_id: int,
        amount: float,
        time: Optional[datetime],
        note: str = "",
        outcome_type: OutcomeType = OutcomeType.OTHER,
    ) -> None:
        """
        Add an expense transaction to the account book.
        """
        AccountBook.verify_book_ownership(conn, token, account_book_id)

        tx = Transaction(
            amount=amount,
            account_book_id=account_book_id,
            category=outcome_type,
            time=time,
            note=note,
        )
        Transaction.execute_db_add(conn, tx)

    def execute_remove_transaction(
        self,
        conn: sqlite3.Connection,
        time: Optional[datetime] = None,
        note: Optional[str] = None,
        account_name: Optional[str] = None,
        account_book_name: Optional[str] = None,
    ) -> None:
        """
        Remove all transactions in the current account book matching the optional filters.
        """
        transactions = Transaction.execute_db_query(
            conn=conn,
            account_book_id=self._id,
            time=time,
            note=note,
            account_name=account_name,
            account_book_name=account_book_name,
        )
        if not transactions:
            return
        # Collect IDs of transactions to remove
        tx_ids = [tx.id for tx in transactions if tx.id is not None]
        if tx_ids:
            Transaction.execute_db_remove(conn, tx_ids)

    @staticmethod
    def get_transaction_list(
        conn: sqlite3.Connection,
        token: str,
        account_book_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        note: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Find transactions in the specified account book matching the optional filters,
        sorted by time (earlier first). Token is verified and book ownership checked.
        By default, shows all transactions.
        """
        # Verify token and get account_id
        row = conn.execute(
            "SELECT account_id, token_expire FROM accounts WHERE token = ?",
            (token,),
        ).fetchone()
        if row is None:
            raise TokenNotFoundError("Token not found.")
        account_id, token_expire = row
        now = int(time.time())
        if token_expire is not None and now > token_expire:
            raise TokenExpireException("Token expired.")

        # Check if the account_book belongs to the account
        book_row = conn.execute(
            "SELECT 1 FROM account_books WHERE account_book_id = ? AND account_id = ?",
            (account_book_id, account_id),
        ).fetchone()
        if book_row is None:
            raise RuntimeError(
                "Account book not found or does not belong to this account."
            )

        # Default time range: show all transactions
        if start_time is None:
            start_time = datetime.fromtimestamp(0)  # beginning of time
        if end_time is None:
            end_time = datetime.now()

        sql = """
            SELECT t.id, t.amount, t.time, t.note, t.category
            FROM transactions AS t
            WHERE t.account_book_id = ?
              AND t.time >= ?
              AND t.time <= ?
        """
        params: List = [account_book_id, start_time.isoformat(), end_time.isoformat()]
        if note is not None:
            sql += " AND t.note LIKE ?"
            params.append(f"%{note}%")
        sql += " ORDER BY t.time ASC"
        rows = conn.execute(sql, params).fetchall()
        result: List[Transaction] = []
        for row in rows:
            tx_id, amount, t_time, t_note, t_category = row
            if t_category is None:
                category_enum = None
            else:
                category_name: str = t_category
                if amount >= 0:
                    category_enum = IncomeType[category_name]
                else:
                    category_enum = OutcomeType[category_name]
            result.append(
                Transaction(
                    amount=amount,
                    account_book_id=account_book_id,
                    time=datetime.fromisoformat(t_time),
                    note=t_note,
                    category=category_enum,
                    id=tx_id,
                )
            )
        return result

    def get_balance(self, conn: sqlite3.Connection) -> float:
        """
        Calculate the current balance of the account book (sum of all transaction amounts).
        """
        all_tx = Transaction.execute_db_query(conn, account_book_id=self._id)
        if not all_tx:
            return 0.0
        total = sum(tx.amount for tx in all_tx)
        return total


def init() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Create tables (with updated schema):
    # transactions table (uses single 'category' field instead of income_type/outcome_type)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        account_book_id INTEGER NOT NULL,
        amount          REAL    NOT NULL,
        time            TEXT    NOT NULL,
        note            TEXT,
        category        TEXT,
        FOREIGN KEY (account_book_id)
            REFERENCES account_books(account_book_id)
            ON DELETE CASCADE
    )
    """)

    # account_books table (no ON DELETE CASCADE on account_id foreign key)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_books (
        account_book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT NOT NULL,
        account_id      INTEGER NOT NULL,
        FOREIGN KEY (account_id)
            REFERENCES accounts(account_id)
    )
    """)

    # accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
        account_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT    NOT NULL UNIQUE,
        email         TEXT    NOT NULL UNIQUE,
        pwd           TEXT    NOT NULL,        
        token         TEXT    NOT NULL,
        token_expire  INTEGER 
    );""")

    # linking table for accounts and account_books (for future multi-user support)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_with_account_books (
        account_id      INTEGER NOT NULL,
        account_book_id INTEGER NOT NULL,
        PRIMARY KEY (account_id, account_book_id),
        FOREIGN KEY (account_id)
            REFERENCES accounts(account_id) ON DELETE CASCADE,
        FOREIGN KEY (account_book_id)
            REFERENCES account_books(account_book_id) ON DELETE CASCADE
    )
    """)

    # (Removed account_books_with_transactions table as it was redundant)

    conn.commit()
    logging.info("Database initialized successfully.")
    return conn, cursor


def delete_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS account_books")
    cursor.execute("DROP TABLE IF EXISTS accounts")
    cursor.execute("DROP TABLE IF EXISTS account_with_account_books")
    # Note: account_books_with_transactions table is not present anymore
    conn.close()


# if __name__ == "__main__":
#     # 0️⃣ 彻底重置数据库（调试用）
#     delete_all()
#
#     # 1️⃣ 初始化
#     conn, _ = init()
#
#     # 2️⃣ 注册 & 登录
#     alice = Account.register(
#         conn, name="alice", email="123321@gmail.com", pwd_hash="123456"
#     )
#     print("👤 注册成功:", alice)
#
#     login_acc = Account.login(conn, "alice", "123456")  # pyright: ignore[reportCallIssue]
#     print("🔐 登录成功:", login_acc)
#
#     # 3️⃣ 创建账本
#     # FIXME: fix this
#     book = Account.create_book(conn, account_id=login_acc.id, book_name="My First Book")  # pyright: ignore[reportOptionalMemberAccess]
#     print("📒 创建账本:", book.__dict__)
#
#     # 4️⃣ 记一笔收入 (+100) 与支出 (‑30)
#     AccountBook.add_income(
#         conn,
#         book,
#         amount=100.0,
#         time=datetime.now(),
#         note="Salary",
#         income_type=IncomeType.SALARY,
#     )
#     AccountBook.add_outcome(
#         conn,
#         book,
#         amount=-30.0,
#         time=datetime.now(),
#         note="Dinner",
#         outcome_type=OutcomeType.FOOD,
#     )
#     print("💰 已添加 2 条交易")
#
#     # 5️⃣ 查询交易 & 余额
#     tx_list = book.execute_find_transaction(conn)
#     print("🔍 当前账本交易:")
#     for tx in tx_list:
#         print("   ", tx.__dict__)
#
#     balance = book.get_balance(conn)
#     print("📊 当前余额:", balance)
#
#     # 6️⃣ 删除全部交易 → 再查余额
#     book.execute_remove_transaction(conn)
#     print("🗑️  已删除全部交易")
#     print("📊 删除后余额:", book.get_balance(conn))
#
#     # 7️⃣ 修改密码并验证
#     ok = Account.change_pwd(
#         conn=conn,
#         email_or_name="alice",  # pyright: ignore[reportArgumentType]
#         old_pwd_hash="123456",
#         new_pwd_hash="better_pwd",
#     )
#     print("🔑 修改密码成功?:", ok)
#     relog = Account.login(conn, "alice", "better_pwd")
#     print("🔐 新密码登录:", bool(relog))
#
#     conn.close()
