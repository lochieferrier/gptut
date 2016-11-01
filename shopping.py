from gpkit import Variable, VectorVariable, Model
from gpkit.tools import te_exp_minus1
import numpy as np


class ShoppingCart(Model):
    def __init__(self, goods=None, bads=None, taylor_order=6):
        goods = goods if goods else {}
        goods.update({1/k: 1/v for k, v in bads.items()})
        N = check_values_length(goods)
        
        exp_S = VectorVariable(N, "e^{S}")   
        self.exp_selection = exp_S

        objective = 1
        constraints = [[exp_S >= 1, exp_S.prod() == np.e]]
        for monomial, options in goods.items():
            m_nd = Variable("|%s|" % monomial.latex(excluded=["models", "units"]))
            exp_m = Variable("e^{%s}" % m_nd.latex(excluded=["models"]))
            objective /= monomial
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
        Model.__init__(self, objective, constraints)
        
    def selection(self, solution):
        return np.log([v.value for v in solution(self.exp_selection)])
        
        
def check_values_length(dictionary, N=None):
    for option in dictionary.values():
        if N is None:
            N = len(option)
        elif len(option) != N:
            raise ValueError("all values must be of equal length, but one was"
                             "length %i while another was length %i" % (N, len(option)))
    return N
