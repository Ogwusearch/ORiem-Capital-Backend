from app.routers import (
    auth_router,
    user_router,
    account_router,
    transaction_router,
    loan_router,
    investment_router,
    admin_router,
    audit_router,
    bill_router,
    profile_router,
    card_router,
)

ROUTERS = [
    (auth_router.router,        "/api/v1/auth",         "Auth"),
    (user_router.router,        "/api/v1/users",        "Users"),
    (account_router.router,     "/api/v1/accounts",     "Accounts"),
    (transaction_router.router, "/api/v1/transactions", "Transactions"),
    (loan_router.router,        "/api/v1/loans",        "Loans"),
    (investment_router.router,  "/api/v1/investments",  "Investments"),
    (admin_router.router,       "/api/v1/admin",        "Admin"),
    (audit_router.router,       "/api/v1/audit",        "Audit Logs"),
    (bill_router.router,        "/api/v1/bills",        "Bill Payments"),
    (profile_router.router,     "/api/v1/profile",      "Profile"),
    (card_router.router,        "/api/v1/cards",        "Card Services"),
]
