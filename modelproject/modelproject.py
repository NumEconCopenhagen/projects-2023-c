import numpy as np
from scipy import linalg
from scipy import optimize
import sympy as sm

# Define parameters
k = sm.symbols('k')
h = sm.symbols('h')
alpha = sm.symbols('alpha')
delta = sm.symbols('delta')
phi = sm.symbols('phi')
s_K = sm.symbols('s_K')
s_H = sm.symbols('s_H')
g = sm.symbols('g')
n = sm.symbols('n')
param = [k, h, alpha, delta, phi, s_K, s_H, g, n]


def nullclines(param):
    """ Finds nullclines. 

    Args:
        param : parameters

    Returns:
        nullclines for k and h.

    """ 
    
    # a. Transition equations
    trans_k = sm.Eq(k,(s_K*k**alpha*h**phi+(1-delta)*k)/((1+n)*(1+g)))
    trans_h = sm.Eq(h,(s_H*k**alpha*h**phi+(1-delta)*h)/((1+n)*(1+g)))
    
    # b. finding the nulclines
    Delta_k = trans_k.lhs - trans_k.rhs
    Delta_h = trans_h.lhs - trans_h.rhs
    # setting both leftsides equal to 0
    zero_k = sm.Eq(0, Delta_k)
    zero_h = sm.Eq(0, Delta_h)
    
    nullcline_k = sm.solve(zero_k,h)
    nullcline_h = sm.solve(zero_h,h)

    return nullcline_k, nullcline_h

def aevaluation(x):
    """ Evaluates the model with concrete parameter values
    
    Args:
        param : parameters

    Returns:
        Steady state values for k and h

    """
    kss = ((s_K**(1-phi) * s_H**phi) / ((n+g+delta+n*g)))**(1 / (1-alpha-phi))
    hss = ((s_K**(alpha) * s_H**(1-alpha)) / ((n+g+delta+n*g)))**(1 / (1-alpha-phi))

    # Turing solutions into Python functions
    kss_func = sm.lambdify((s_K,s_H,g,n,delta,phi,alpha),kss)
    hss_func = sm.lambdify((s_K,s_H,g,n,delta,phi,alpha),hss)

    return kss_func, hss_func

def capital(s_K, s_H, n, delta, alpha, phi, k0, h0, T, g):
    """
    Calculates the Solow-Human Capital model over time for given parameters
    
    Args:
        s_K (float): savings rate for capital
        s_H (float): savings rate for human capital
        n (float): population growth rate
        delta (float): rate of depreciation of capital and human capital
        alpha (float): share of capital in production function
        phi (float): share of human capital in production function
        k0 (float): initial value of capital
        h0 (float): initial value of human capital
        T (int): number of time periods to simulate
        g (float, optional): growth rate of technology
    
    Returns:
        k (numpy array): stock of capital over time
        h (numpy array): stock of human capital over time
    """
    
    # Create arrays to store values over time
    k = np.zeros(T)
    h = np.zeros(T)
    k[0] = k0
    h[0] = h0
    
    for t in range(1, T):
        k[t] = ((s_K*k[t-1]**alpha*h[t-1]**phi + (1-delta)*k[t-1]) / (1+n+g)) 
        h[t] = ((s_H*k[t-1]**alpha*h[t-1]**phi + (1-delta)*h[t-1]) / (1+n+g))

    return k, h