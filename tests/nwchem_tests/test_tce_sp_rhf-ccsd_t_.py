#! single-point CCSD(T)/cc-pvdz on water
import os
import sys
from ..utils import *
from ..addons import *
import qcdb

h2o = qcdb.set_molecule('''
        O     0.000000000000    0.000000000000   -0.065638538099
        H     0.000000000000   -0.757480611647    0.520865616174
        H     0.000000000000    0.757480611647    0.520865616174
        ''')

print(h2o)


def check_ccsd_t_(return_value):
    ref = -76.026744421192
    nre = 9.187334240165
    ccsdcorl = -0.213350416141872
    ccsdtot = -76.240094837333771
    ccsd_t_corr = -0.003062727448805
    ccsd_t_corl = -0.216413143590677
    ccsd_t_tot = -76.243157564782578

    assert compare_values(ref, qcdb.get_variable('HF TOTAL ENERGY'), 5, 'hf ref')
    assert compare_values(ccsdcorl, qcdb.get_variable('CCSD CORRELATION ENERGY'), 5, 'ccsd corl')
    assert compare_values(ccsdtot, qcdb.get_variable('CCSD TOTAL ENERGY'), 5, 'ccsd total')
    assert compare_values(ccsd_t_corr, qcdb.get_variable('(T) CORRECTION ENERGY'), 5, 'ccsd(t) corr')
    assert compare_values(ccsd_t_corl, qcdb.get_variable('CCSD(T) CORRELATION ENERGY'), 5, 'ccsd(t) corl')
    assert compare_values(ccsd_t_tot, qcdb.get_variable('CCSD(T) TOTAL ENERGY'), 5, 'ccsd(t) tot')
    assert compare_values(nre, qcdb.get_variable('NUCLEAR REPULSION ENERGY'), 5, 'nre')


@using_nwchem
def test_1_ccsd_t_():
    qcdb.set_options({
        'basis': 'cc-pvdz',
        'memory': '600 mb',
        'nwchem_scf': 'rhf',
        'nwchem_scf_thresh': 1.0e-12,
        'nwchem_tce_dft': False,
        'nwchem_tce_module': 'CCSD(T)',
        'nwchem_tce': True,
        'nwchem_tce_thresh': 1.0e-12,
        'nwchem_task_tce': 'energy'
    })
    print('     Testing ccsd(t) ...')
    val = qcdb.energy('nwc-ccsd(t)')
    check_ccsd_t_(val)
