# # import scipy.optimize
# from datetime import date


# def xnpv(rate, cashflows):
#     """
#     Equivalent of Excel's XNPV function.
#     >>> from datetime import date
#     >>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
#     >>> values = [-10000, 20, 10100]
#     >>> xnpv(0.1, values, dates)
#     -966.4345...
#     """
#     if rate <= -1.0:
#         return float('inf')
#     d0 = cashflows[0][0]    # or min(dates)
#     return sum([c[1] / (1.0 + rate)**((c[0] - d0).days / 365.0) for c in cashflows])
#
#
# def xirr(cashflows):
#     """
#     Equivalent of Excel's XIRR function.
#     >>> from datetime import date
#     >>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
#     >>> values = [-10000, 20, 10100]
#     >>> xirr(values, dates)
#     0.0100612...
#     """
#     try:
#         return scipy.optimize.newton(lambda r: xnpv(r, cashflows), 0.0)
#     except RuntimeError:    # Failed to converge?
#         return scipy.optimize.brentq(lambda r: xnpv(r, cashflows), -1.0, 1e10)


# noinspection PyBroadException

class XIRR:
    # Set maximum epsilon for end of iteration
    eps_max_rate = 1e-6
    eps_max_value = 1e-4
    guess_vals_neg = [-0.1, -0.05, -0.025, -0.15, -0.2, -0.25, -0.3, -0.5, -0.75, -0.9]

    # Set maximum epsilon for end of iteration
    iter_max = 100

    def __init__(self, transactions, guess=None):
        self.transactions = transactions
        self.sort_transactions()
        self.xirr = None
        self.guess = guess
        self.error = False

    def sort_transactions(self):
        try:
            self.transactions.sort(key=lambda x: [x[0], -x[1]])
        except TypeError:
            self.error = True

    def check_if_correct_transactions(self):
        # Check that values contains at least one positive value and one negative value
        positive = False
        negative = False
        # todo: scope of improvement
        for t in self.transactions:
            if t[1] > 0:
                positive = True
            if t[1] < 0:
                negative = True
            if positive and negative:
                break
        if positive and negative:
            correct = True
        else:
            correct = False
        return correct

    def set_guess_rate(self):
        if self.guess is None:
            if sum(k[1] for k in self.transactions) > 0:
                self.guess = -0.1
            else:
                self.guess = 0.1

    def get_xirr(self):
        transactions_correct = self.check_if_correct_transactions()
        if transactions_correct and not self.error:

            guesses_tried_pos = list(map(lambda x: -x, self.guess_vals_neg))
            self.set_guess_rate()
            if self.guess == guesses_tried_pos[0]:
                guesses_try = guesses_tried_pos
            else:
                guesses_try = self.guess_vals_neg
            guesses_try.reverse()
            tries = 0
            while tries < 1 or (self.xirr is None and len(guesses_try)):
                self.guess = guesses_try.pop()
                self.xirr = self.calculate_xirr()
                tries += 1
        return self.xirr

    def calculate_xirr(self):
        try:
            result_rate = self.implement_newtons_method()
            if type(result_rate) not in [float, int]:
                return None
        except (ZeroDivisionError, OverflowError, TypeError):
            result_rate = None
        except Exception:
            result_rate = None
        return result_rate

    def implement_newtons_method(self):
        result_rate = self.guess
        # Implement Newton's method
        iteration = 0
        cont_loop = True
        while cont_loop and (iteration < self.iter_max):
            # Result  value  gives you residual value from the assumed rate of return
            result_value = self.irr_result(result_rate)
            new_rate = result_rate - (result_value / self.irr_result_deriv(result_rate))

            eps_rate = abs(new_rate - result_rate)
            result_rate = new_rate

            iteration += 1
            cont_loop = (eps_rate > self.eps_max_rate) and (
                abs(result_value) > self.eps_max_value
            )
        if cont_loop:
            result_rate = None
        else:
            result_rate = result_rate * 100
        return result_rate

    def irr_result(self, rate):
        r = rate + 1
        result = 0
        first = self.transactions[0]

        for t in self.transactions:
            frac = (t[0] - first[0]).days / 365
            result += t[1] / pow(r, frac)
        return result

    def irr_result_deriv(self, rate):
        # Calculates the first derivation
        r = rate + 1
        result = 0
        first = self.transactions[0]
        for t in self.transactions:
            frac = (t[0] - first[0]).days / 365
            result -= frac * t[1] / pow(r, frac + 1)
        return result

    def set_guess_for_extreme_cases(self):
        pos_amt = sum(k[1] for k in self.transactions if k[1] > 0)
        neg_amt = abs(sum(k[1] for k in self.transactions if k[1] < 0))
        per = (self.transactions[-1][0] - self.transactions[0][0]).days / 365
        self.guess = pow(neg_amt / pos_amt, 1 / per) - 1
