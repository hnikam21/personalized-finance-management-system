from decimal import Decimal, getcontext
from datetime import date

getcontext().prec = 10


def calculate_fd(principal, rate, start_date):
    if not start_date or not rate:
        return principal

    years = Decimal((date.today() - start_date).days) / Decimal(365)
    rate = Decimal(rate) / Decimal(100)

    amount = Decimal(principal) * ((Decimal(1) + rate) ** years)
    return amount.quantize(Decimal("0.01"))


def calculate_sip(principal, rate, start_date):
    if not start_date or not rate:
        return principal

    months = (
        (date.today().year - start_date.year) * 12 +
        (date.today().month - start_date.month)
    )

    monthly_rate = Decimal(rate) / Decimal(100) / Decimal(12)

    if monthly_rate == 0:
        return Decimal(principal)

    future_value = Decimal(principal) * (
        ((Decimal(1) + monthly_rate) ** months - 1) / monthly_rate
    )

    return future_value.quantize(Decimal("0.01"))


def calculate_stock(quantity, buy_price, simulated_growth=Decimal("0.12")):
    if not quantity or not buy_price:
        return Decimal(0)

    return (
        Decimal(quantity) *
        Decimal(buy_price) *
        (Decimal(1) + simulated_growth)
    ).quantize(Decimal("0.01"))
