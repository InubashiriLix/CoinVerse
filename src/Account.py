from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime
from enum import Enum, auto
from typing import Optional, Union, List, Tuple

import logging
from utils import _hash_pwd

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


class OutcomeType(Enum):
    FOOD = auto()
    RENT = auto()
    TRANSPORT = auto()
    ENTERTAIN = auto()
    OTHER = auto()


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
        if self.amount >= 0:
            if not isinstance(self.category, IncomeType):
                raise ValueError(
                    "Positive (or zero) amount transaction must have an IncomeType category."
                )
        elif self.amount < 0:
            if not isinstance(self.category, OutcomeType):
                raise ValueError(
                    "Negative amount transaction must have an OutcomeType category."
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


class Account:
    id: int
    name: str
    pwd_hash: str
    books: Optional[List[AccountBook]]

    def __init__(
        self,
        id: int,
        name: str,
        pwd_hash: str,
        books: Optional[List[AccountBook]] = None,
    ):
        self.id = id
        self.name = name
        self.pwd_hash = pwd_hash
        self.books = books if books is not None else []

    @staticmethod
    def register(conn: sqlite3.Connection, name: str, pwd: str) -> Account:
        cur = conn.execute(
            "INSERT INTO accounts (name, pwd) VALUES (?, ?)", (name, _hash_pwd(pwd))
        )
        conn.commit()
        # Return the new Account object (initialize books list empty)
        account_id = cur.lastrowid
        assert account_id is not None, "Failed to create account, no ID returned."
        return Account(id=account_id, name=name, pwd_hash=_hash_pwd(pwd), books=[])

    @staticmethod
    def login(conn: sqlite3.Connection, name: str, pwd: str) -> Optional[Account]:
        row = conn.execute(
            "SELECT account_id, pwd FROM accounts WHERE name = ?", (name,)
        ).fetchone()
        if not row:
            return None
        acc_id, db_hash = row
        if db_hash != _hash_pwd(pwd):
            return None
        books = Account._load_books(conn, acc_id)
        return Account(id=acc_id, name=name, pwd_hash=db_hash, books=books)

    @staticmethod
    def create_book(
        conn: sqlite3.Connection, account_id: int, book_name: str
    ) -> AccountBook:
        cur = conn.execute(
            "INSERT INTO account_books (name, account_id) VALUES (?, ?)",
            (book_name, account_id),
        )
        conn.commit()
        # Instantiate a new AccountBook object for the created book
        account_book_id = cur.lastrowid
        assert account_book_id is not None, (
            "Failed to create account book, no ID returned."
        )
        return AccountBook(id=account_id, name=book_name, account_id=account_id)

    @staticmethod
    def list_books(conn: sqlite3.Connection, account_id: int) -> List[AccountBook]:
        return Account._load_books(conn, account_id)

    @staticmethod
    def change_pwd(
        conn: sqlite3.Connection, account_id: int, old_pwd: str, new_pwd: str
    ) -> bool:
        row = conn.execute(
            "SELECT pwd FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        if not row or row[0] != _hash_pwd(old_pwd):
            return False
        conn.execute(
            "UPDATE accounts SET pwd = ? WHERE account_id = ?",
            (_hash_pwd(new_pwd), account_id),
        )
        conn.commit()
        return True

    @staticmethod
    def _load_books(conn: sqlite3.Connection, account_id: int) -> List[AccountBook]:
        rows = conn.execute(
            "SELECT account_book_id, name FROM account_books WHERE account_id = ?",
            (account_id,),
        ).fetchall()
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
    def add_income(
        conn: sqlite3.Connection,
        acc_bk_obj: AccountBook,
        amount: float,
        time: Optional[datetime],
        note: str = "",
        income_type: IncomeType = IncomeType.OTHER,
    ) -> None:
        """
        Add an income transaction to the account book.
        """
        if acc_bk_obj._id is None:
            raise ValueError("AccountBook ID is not set. Cannot add income.")
        tx = Transaction(
            amount=amount,
            account_book_id=acc_bk_obj._id,
            category=income_type,
            time=time,
            note=note,
        )
        Transaction.execute_db_add(conn, tx)  # This will commit the transaction

    @staticmethod
    def add_outcome(
        conn: sqlite3.Connection,
        acc_bk_obj: AccountBook,
        amount: float,
        time: Optional[datetime],
        note: str = "",
        outcome_type: OutcomeType = OutcomeType.OTHER,
    ) -> None:
        """
        Add an expense transaction to the account book.
        """
        if acc_bk_obj._id is None:
            raise ValueError("AccountBook ID is not set. Cannot add outcome.")
        tx = Transaction(
            amount=amount,
            account_book_id=acc_bk_obj._id,
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

    def execute_find_transaction(
        self,
        conn: sqlite3.Connection,
        time: Optional[datetime] = None,
        note: Optional[str] = None,
        account_name: Optional[str] = None,
        account_book_name: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Find transactions in the current account book matching the optional filters.
        """
        return Transaction.execute_db_query(
            conn=conn,
            account_book_id=self._id,
            time=time,
            note=note,
            account_name=account_name,
            account_book_name=account_book_name,
        )

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
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        pwd        TEXT NOT NULL
    )
    """)

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


if __name__ == "__main__":
    # 0️⃣ 彻底重置数据库（调试用）
    delete_all()

    # 1️⃣ 初始化
    conn, _ = init()

    # 2️⃣ 注册 & 登录
    alice = Account.register(conn, "alice", "123456")
    print("👤 注册成功:", alice)

    login_acc = Account.login(conn, "alice", "123456")
    print("🔐 登录成功:", login_acc)

    # 3️⃣ 创建账本
    book = Account.create_book(conn, account_id=login_acc.id, book_name="My First Book")  # pyright: ignore[reportOptionalMemberAccess]
    print("📒 创建账本:", book.__dict__)

    # 4️⃣ 记一笔收入 (+100) 与支出 (‑30)
    AccountBook.add_income(
        conn,
        book,
        amount=100.0,
        time=datetime.now(),
        note="Salary",
        income_type=IncomeType.SALARY,
    )
    AccountBook.add_outcome(
        conn,
        book,
        amount=-30.0,
        time=datetime.now(),
        note="Dinner",
        outcome_type=OutcomeType.FOOD,
    )
    print("💰 已添加 2 条交易")

    # 5️⃣ 查询交易 & 余额
    tx_list = book.execute_find_transaction(conn)
    print("🔍 当前账本交易:")
    for tx in tx_list:
        print("   ", tx.__dict__)

    balance = book.get_balance(conn)
    print("📊 当前余额:", balance)

    # 6️⃣ 删除全部交易 → 再查余额
    book.execute_remove_transaction(conn)
    print("🗑️  已删除全部交易")
    print("📊 删除后余额:", book.get_balance(conn))

    # 7️⃣ 修改密码并验证
    ok = Account.change_pwd(
        conn,
        account_id=login_acc.id,  # pyright: ignore[reportOptionalMemberAccess]
        old_pwd="123456",
        new_pwd="better_pwd",
    )
    print("🔑 修改密码成功?:", ok)
    relog = Account.login(conn, "alice", "better_pwd")
    print("🔐 新密码登录:", bool(relog))

    conn.close()
