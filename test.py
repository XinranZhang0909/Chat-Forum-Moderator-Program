"""
Author: Xinran Zhang
SID: 500671702
Unikey: xzha0459
"""

"""
Do not edit the following line - it is required to pass the testcases.
In your test suite, write tests targeting these functions.
They can be called like normal functions, e.g. is_valid_name()
"""
from test_functions import is_valid_name, is_chronological

def test01():
    name = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -"
    actual = is_valid_name(name)
    expected = True
    result = False
    if actual == expected:
        result = True
    return result

def test02():
    name = " "
    actual = is_valid_name(name)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

def test03():
    name = ""
    actual = is_valid_name(name)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

def test04():
    name = "Lydia$"
    actual = is_valid_name(name)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

def test05():
    name = 100
    actual = is_valid_name(name)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

def test06():
    ealier_dt="1996-09-12T16:30:16"
    later_dt="1997-09-12T16:30:16"
    actual = is_chronological(ealier_dt,later_dt)
    expected = True
    result = False
    if actual == expected:
        result = True
    return result

def test07():
    ealier_dt="1996-09-12T16:30:16"
    later_dt="1995-09-12T16:30:16"
    actual = is_chronological(ealier_dt,later_dt)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

def test08():
    ealier_dt=1
    later_dt="1995-09-12T16:30:16"
    result=True
    try:
        is_chronological(ealier_dt,later_dt)
    except:
        result=False
    return result

def test09():
    ealier_dt="1996-09-12 16:30:16"
    later_dt="1996-09-12T16:30:16"
    actual = is_chronological(ealier_dt,later_dt)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

def test10():
    ealier_dt="1996-09-12T16:30:16"
    later_dt="1996-09-12T16:30:16"
    actual = is_chronological(ealier_dt,later_dt)
    expected = False
    result = False
    if actual == expected:
        result = True
    return result

first_test = test01() and test02() and test03() and test04() and test05()
second_test = test06() and test07() and test08() and test09() and test10()
if first_test == True:
    print("is_valid_name has passed.")
else:
    print("is_valid_name has failed.")
if second_test == True:
    print("is_chronological has passed.")
else:
    print("is_chronological has failed.")
