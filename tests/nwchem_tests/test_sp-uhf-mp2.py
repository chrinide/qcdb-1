#! single-point UHF-MP2/cc-pVDZ  on NH2
# ROHF-MP2 is not available in NWChem
import os
import sys
from ..utils import *
from ..addons import *
import qcdb

nh2 = qcdb.set_molecule('''
         N        0.08546       -0.00020       -0.05091
         H       -0.25454       -0.62639        0.67895
         H       -0.25454       -0.31918       -0.95813
        ''')
print(nh2)


def check_uhf_mp2(return_value, is_5050):
    ref = -55.566057523877
    mp2_tot = -55.711202243414
    mp2_corl = -0.145144719537
    scs_tot = -55.712082715312
    scs_corl = -0.146025191435
    mp2os = -0.112665713372
    mp2ss = -0.032479006165
    a5050corl = 0.5 * (mp2os + mp2ss)
    a5050tot = a5050corl + ref

    assert compare_values(ref, qcdb.get_variable('HF TOTAL ENERGY'), 5, 'scf')
    assert compare_values(mp2_tot, qcdb.get_variable('MP2 TOTAL ENERGY'), 5, 'mp2 tot')
    assert compare_values(mp2_corl, qcdb.get_variable('MP2 CORRELATION ENERGY'), 5, 'mp2 corl')
    assert compare_values(scs_tot, qcdb.get_variable('SCS-MP2 TOTAL ENERGY'), 5, 'scs mp2 tot')
    assert compare_values(scs_corl, qcdb.getvariable('SCS-MP2 CORRELATION ENERGY'), 5, 'scs mp2 corl')
    assert compare_values(mp2ss, qcdb.get_variable('MP2 SAME-SPIN CORRELATION ENERGY'), 5, 'mp2 ss')
    assert compare_values(mp2os, qcdb.get_variable('MP2 OPPOSITE-SPIN CORRELATION ENERGY'), 5, 'mp2 os')
    if is_5050:
        assert compare_values(a5050corl, qcdb.get_variable('CUSTOM SCS-MP2 CORRELATION ENERGY'), 5, 'mp2 scscorl')
        assert compare_values(a5050tot, qcdb.get_variable('CUSTOM SCS-MP2 TOTAL ENERGY'), 5, 'mp2 scstot')

@using_nwchem
def test_1_mp2_5050no():
    qcdb.set_options({
        'basis': 'cc-pvdz',
        'memory': '300 mb',
        'nwchem_scf__UHF': True,
        'nwchem_scf__nopen': 1,
        #'nwchem_scf_mixiter': 80,
        'nwchem_scf__thresh': 1.0e-8,
    })
    print('Testing hf...')
    val = qcdb.energy('nwc-mp2')
    check_uhf_mp2(val, is_5050=False)

@using_nwchem
def test_2_mp2_5050yes():
    qcdb.set_options({
        'basis': 'cc-pvdz',
        'memory': '300 mb',
        'nwchem_scf__UHF': True,
        'nwchem_scf__nopen': 1,
        #'nwchem_scf_mixiter': 80,
        'nwchem_scf__thresh': 1.0e-8,
    })
    print('Testing mp2...')
    val = qcdb.energy('nwc-mp2')
    check_uhf_mp2(val, is_5050=True)
