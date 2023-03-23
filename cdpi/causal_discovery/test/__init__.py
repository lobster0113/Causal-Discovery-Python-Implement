from ._conditional_mutual_information_test import (conditional_mutual_information_test)
from ._kcit import ( gaussian_kernel, 
                    centralized_gaussian_kernel,
                    kcit)


def get_test(test_name):
    test_array = [conditional_mutual_information_test, 
                  kcit]
    
    test_name = test_name.lower()
    for test in test_array:
        if test.__name__ == test_name: return test