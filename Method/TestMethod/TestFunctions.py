
import numpy as np

"""
@definition:
 Multivariable polynomial test function that returns a * x^3 + b * x * y^2 + c * x * y + d * x + e,
 where a, b, c, d and e are 512x512 sized random arrays which are multidimensional polynomial coefficients
 propagated from dataset to here.
@param "coeffs": 5 length array of 512x512 multidimensional polynomial coefficients.
@param "input": Variable values.
@return: 512x512 array

"""
def TestFunction1(coeffs: list, input: list):
    assert len(coeffs) == 5, "Inappropriate coefficients"
    x = input[0]
    y = input[1]
    a, b, c, d, e = coeffs
    res = c *  y + d * x + e + a * x**2 + b * x * y
    return res


"""
@definition:
 Multivariable polynomial test function that returns a * y^3 + b * x^2  + c * x * y + d * y + e,
 where a, b, c, d and e are 512x512 sized random arrays which are multidimensional polynomial coefficients
 propagated from dataset to here.
@param "coeffs": 5 length array of 512x512 multidimensional polynomial coefficients.
@param "input": Variable values.
@return: 512x512 array

"""
def TestFunction2(coeffs: list, input: list):
    assert len(coeffs) == 5, "Inappropriate coefficients"
    x = input[0]
    y = input[1]
    a, b, c, d, e = coeffs
    return a * y**3 + b * x * y**2 + c * x * y + d * x + e