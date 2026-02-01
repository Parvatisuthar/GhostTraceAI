import os

def create_sample_datasets():
    base = "data_ingestion/sample_datasets"
    os.makedirs(base, exist_ok=True)

    samples = {

# ---------------- API v1 ----------------

"payment_api_v1.0_2021.txt": """
PAYMENT API DOCUMENTATION — VERSION 1.0 (DEPRECATED)

Base URL:
https://api.product.com/v1/

Endpoint:
POST /charge

Request JSON:
{
  "card_number": "string",
  "expiry": "MM/YY",
  "cvv": "123",
  "amount": 500
}

Response:
{
  "status": "success",
  "transaction_id": "tx_123"
}

Authentication:
API Key in header: X-API-KEY

Notes:
- No idempotency support
- No currency field
- No webhook support
""",

"auth_api_v1.0_2021.txt": """
AUTHENTICATION API — VERSION 1.0

Login Endpoint:
POST /login

Request:
{
  "email": "user@mail.com",
  "password": "plain_text"
}

Response:
{
  "token": "jwt-token"
}

Limitations:
- No refresh token
- Token expiry: 24 hrs
""",

# ---------------- API v2 ----------------

"payment_api_v2.0_2022.txt": """
PAYMENT API DOCUMENTATION — VERSION 2.0

Base URL:
https://api.product.com/v2/

Endpoint:
POST /payments/charge

Request:
{
  "card": {
     "number": "string",
     "expiry": "MM/YY",
     "cvv": "123"
  },
  "amount": 500,
  "currency": "INR"
}

Headers:
Authorization: Bearer <token>

Response:
{
  "status": "success",
  "payment_id": "pay_456"
}

New Features:
- Currency support
- Webhook callbacks added
- Retry-safe using idempotency-key header
""",

"sdk_android_v2.0_guide.txt": """
ANDROID SDK — VERSION 2.0

Initialization:
PaymentSDK.init(context, apiKey)

Charge Payment:
sdk.charge(cardObj, amount, currency)

Callbacks:
onSuccess(paymentId)
onFailure(errorCode)

Min Android:
API 23+
""",

# ---------------- API v3 (LATEST) ----------------

"payment_api_v3.0_2024.txt": """
PAYMENT API DOCUMENTATION — VERSION 3.0 (LATEST)

Base URL:
https://api.product.com/v3/

Endpoint:
POST /payments

Request:
{
  "payment_method_id": "pm_987",
  "amount": 500,
  "currency": "INR",
  "customer_id": "cust_001"
}

Authentication:
OAuth2 Access Token

Response:
{
  "status": "authorized",
  "payment_id": "pay_999",
  "next_action": "3ds_verification"
}

Breaking Changes:
- Card details never sent directly
- Tokenized payment methods only
- Mandatory customer object
""",

"webhook_events_v3.0.txt": """
WEBHOOK EVENTS — VERSION 3.0

payment.authorized
payment.failed
payment.captured

Payload Example:
{
  "event": "payment.captured",
  "payment_id": "pay_999",
  "amount": 500,
  "currency": "INR",
  "timestamp": "2024-11-20T10:30:00Z"
}

Security:
HMAC signature verification required
""",

"rate_limits_v3.0.txt": """
RATE LIMIT POLICY — VERSION 3.0

Limits:
100 requests/min per API key

Burst:
20 req/sec

429 Response:
Retry-After header mandatory

Abuse Protection:
Automatic temporary IP blocking
""",

# ---------------- CONFIG & MIGRATION ----------------

"migration_guide_v1_to_v3.txt": """
MIGRATION GUIDE: API v1 → v3

Major Changes:
- Card data not allowed directly
- OAuth2 required
- Payment method tokenization mandatory

Steps:
1. Create customer object
2. Generate payment method token
3. Use /payments endpoint

Common Errors:
401: Invalid OAuth token
422: Missing customer_id

Testing:
Use sandbox tokens only
""",

"config_options_v3.0.txt": """
CONFIGURATION OPTIONS — VERSION 3.0

Timeout:
Default: 30 seconds

Retry Policy:
Exponential backoff

Webhook Retry:
Up to 5 attempts

Security:
IP allowlisting supported

Dashboard Settings:
Enable fraud checks
""",

# ---------------- DEPRECATED NOTICE ----------------

"deprecation_notice_2024.txt": """
DEPRECATION NOTICE — JAN 2024

APIs Deprecated:
v1.0 — Fully disabled
v2.0 — Support ends Dec 2024

Risks:
Older SDKs may fail silently

Action Required:
Migrate to v3 immediately

Support:
developer-support@product.com
"""
    }

    for name, content in samples.items():
        with open(os.path.join(base, name), "w", encoding="utf-8") as f:
            f.write(content)

    print("✅ API documentation datasets (multi-version) created successfully.")

