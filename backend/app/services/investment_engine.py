from app.services.return_calculators import (
    calculate_fd,
    calculate_sip,
    calculate_stock
)

def update_investment_value(investment):

    if investment.investment_type == "FD":
        return calculate_fd(
            investment.principal_amount,
            investment.rate_of_return,
            investment.start_date
        )

    elif investment.investment_type == "SIP":
        return calculate_sip(
            investment.principal_amount,
            investment.rate_of_return,
            investment.start_date
        )

    elif investment.investment_type == "STOCK":
        return calculate_stock(
            investment.quantity,
            investment.buy_price
        )

    return investment.principal_amount
