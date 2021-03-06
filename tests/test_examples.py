# -*- coding: utf-8 -*-

"""
test examples given in paper by comparison against reference solution
"""

from __future__ import print_function


from nose.tools import nottest

import unittest
import numpy as np

import sys

#sys.path.append(os.path.join('..', 'mintrend'))
sys.path.append('..')
from rt1.rt1 import RT1
from rt1.volume import Rayleigh
from rt1.surface import CosineLobe


class TestExamples(unittest.TestCase):

    def setUp(self):
        # read reference solutions for backscattering case
        # fname = 'example1_fn_cc.tab'
        #x = np.loadtxt(fname, delimiter='\t',skiprows=1)
        #~ self.inc = x[:,0]
        #~ self.n = x[:,1]
        #~ self.tau = x[:,2]
        #~ self.fn = x[:,3]
        #~ self.cc = x[:,4]
        self.step = 1

    @nottest
    def test_example1_fn(self):
        S = CosineLobe(ncoefs=10, i=5, NormBRDF = np.pi)  # somehow this is only working for ncoefs=1 at the moment!
        V = Rayleigh(tau=0.7, omega=0.3)

        I0=1.
        phi_0 = 0.
        #~ phi_0 = np.pi/2.
        phi_ex = np.pi  # backscatter case
        fn = None
        for i in range(0,len(self.inc),self.step):

            #~ if self.n[i] % 2 == 1:
                #~ continue   # todo skipping odds at the moment


            t_0 = self.inc[i]
            t_ex = t_0*1.
            RT = RT1(I0, t_0, t_ex, phi_0, phi_ex, RV=V, SRF=S, fn=fn)
            self.assertAlmostEqual(self.inc[i], RT.theta_0)

            mysol = RT._get_fn(int(self.n[i]), RT.theta_0, phi_0)

            print('inc,n,fnref,mysol:', RT.t_0, self.n[i], self.fn[i], mysol)
            fn=RT.fn

            self.assertEqual(self.tau[i],V.tau)   # check that tau for reference is the same as used for Volume object
            if self.fn[i] == 0.:
                self.assertEqual(mysol, self.fn[i])
            else:
                #~ if np.abs(self.fn[i]) > 1.E-:
                    #~ thres = 1.E-3 ## 1 promille threshold
                #~ else:
                thres = 1.E-8  # one percent threshold for very small numbers
                ratio = mysol / self.fn[i]
                self.assertTrue(np.abs(1.-ratio) < thres)

                #~ todo hier weiter

    @nottest
    def test_example1_Fint(self):
        # backscatter case
        S = CosineLobe(ncoefs=10, i=5, NormBRDF = np.pi)
        V = Rayleigh(tau=0.7, omega=0.3)

        I0=1.
        phi_0 = 0.
        phi_ex = np.pi  # backscatter case
        for i in range(0,len(self.inc),self.step):
            print('i,n:', i, self.n[i])
            t_0 = self.inc[i]
            t_ex = t_0*1.

            RT = RT1(I0, t_0, t_ex, phi_0, phi_ex, RV=V, SRF=S)
            self.assertEqual(self.tau[i],V.tau)   # check that tau for reference is the same as used for Volume object

            Fint1 = RT._calc_Fint(t_0, t_ex, phi_0, phi_ex)  # todo clairfy usage of phi!!!
            Fint2 = RT._calc_Fint(t_ex, t_0, phi_ex, phi_0)

            self.assertEqual(Fint1,Fint2)
            #~ self.assertAlmostEqual(Fint1,self.cc[i])






        #~ print RT._get_fn(0, np.arccos(mu_0), phi_0)
        #~ stop


#~ def intback(t0,tau,omega):
    #~ return omega*np.cos(t0)*np.exp(-tau/np.cos(t0))*np.sum(fnfunktexp(n,t0)*CC(n+1,tau,t0) for n in range(0,Np+NBRDF+1))
#~
#~ def fnfunktexp(n,t0):
    #~ return fn[n].xreplace({thetaex:t0})
#~
#~
#~ #   definition of surface- volume and first-order interaction-term
#~ def CC(n,tau,tex):
    #~ if n==0:
        #~ return np.exp(-tau/np.cos(tex))*np.log(np.cos(tex)/(1-np.cos(tex)))-scipy.special.expi(-tau)+np.exp(-tau/np.cos(tex))*scipy.special.expi(tau/np.cos(tex)-tau)
    #~ else:
        #~ return CC(n-1,tau,tex)*np.cos(tex)-(np.exp(-tau/np.cos(tex))/n-scipy.special.expn(n+1,tau))  #todo not clear if this really works for the bistatic case or if this is only for the backscatter case



        #~ Itot, Isurf, Ivol, Iint = RT.calc()


    #~ def test_example1(self):
#~
        #~ S = CosineLobe(ncoefs=10)
        #~ V = Rayleigh(tau=0.7, omega=0.3)
#~
        #~ fname = './example1.json'
        #~ x = json.load(open(fname,'r'))
        #~ inc = x['inc']
#~
        #~ fn = None
        #~ I0 = 1.
        #~ phi_0 = x['phii']
        #~ phi_ex = x['phiex']
        #~ step = 10
        #~ for i in range(0,len(inc),step):
            #~ t0 = inc[i]
            #~ mu_0 = np.cos(t0)
            #~ mu_ex = mu_0*1. # test is for backscattering case
            #~ RT = RT1(I0, mu_0, mu_ex, phi_0, phi_ex, RV=V, SRF=S, fn=fn)
            #~ Itot, Isurf, Ivol, Iint = RT.calc()
#~
            #~ self.assertAlmostEqual(Isurf,x['surf'][i],10)
            #~ self.assertAlmostEqual(Ivol,x['vol'][i],10)
            #~ self.assertAlmostEqual(Iint,x['int'][i],10)



if __name__ == "__main__":
    unittest.main()


