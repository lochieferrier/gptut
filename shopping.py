from gpkit import Variable, VectorVariable, Model
from gpkit.tools import te_exp_minus1
import numpy as np


class ShoppingCart(Model):
    def setup(self, goods=None, bads=None, taylor_order=6):
        goods = goods if goods else {}
        goods.update({1/k: 1/v for k, v in bads.items()})
        N = check_values_length(goods)

        exp_S = VectorVariable(N, "e^{S}")
        VectorVariable(N, "S")

        self.cost = 1
        constraints = [[exp_S >= 1, exp_S.prod() == np.e]]
        for monomial, options in goods.items():
            m_nd = Variable("|%s|" % monomial.latex(excluded=["models", "units"]))
            exp_m = Variable("e^{%s}" % m_nd.latex(excluded=["models"]))
            self.cost /= monomial
            if hasattr(options, "units"):
                monomial = monomial/(1*options.units)
                options = options.magnitude
            options_scale = options.mean()
            options /= options_scale
            constraints.append([
                m_nd == monomial/options_scale,
                (exp_S**options).prod() == exp_m,
                exp_m >= 1 + te_exp_minus1(m_nd, taylor_order),
            ])

        return constraints

    def process_result(self, solution):
        S, e_S = self["S"], self["e^{S}"]
        solution["freevariables"][S] = np.log(solution(e_S))
        solution["variables"][S] = np.log(solution(e_S))


def check_values_length(dictionary, N=None):
    for option in dictionary.values():
        if N is None:
            N = len(option)
        elif len(option) != N:
            raise ValueError("all values must be of equal length, but one was"
                             "length %i while another was length %i" % (N, len(option)))
    return N
