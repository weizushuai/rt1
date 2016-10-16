"""
Core module for 1st order scattering simulations using arbitrary BRDF and phase functions

References
----------
Quast & Wagner (2016): doi:10.1364/AO.55.005379

"""

###todo implement unittests

import numpy as np
from scipy.special import expi
from scipy.special import expn

import sympy as sp



class RT1(object):
    """
    main class to perform RT simulations
    """
    def __init__(self, I0, mu_0, mu_ex, phi_0, phi_ex, RV=None, SRF=None):
        """
        Parameters
        ----------
        I0 : float
            incidence radiation
        RV : Volume
            random volume object
        """
        self.I0 = I0
        self.mu_0 = mu_0
        self.mu_ex = mu_ex
        self.theta_0 = np.arccos(self.mu_0)  # todo set this as a property instead of fixed coding heres
        self.theta_ex = np.arccos(self.mu_ex)
        self.phi_0 = phi_0
        self.phi_ex = phi_ex

        self.RV = RV
        assert self.RV is not None, 'ERROR: needs to provide volume information'

        self.SRF = SRF
        assert self.SRF is not None, 'ERROR: needs to provide surface information'

        # precalculate the expansiion coefficients for the interaction term
        expr_int = self._calc_interaction_expansion()

        # now we have the integral formula ready. The next step is now to
        # extract the expansion coefficients
        self.fn = self._extract_coefficients(expr_int)
        print 'coefficients:'
        print self.fn


    def _extract_coefficients(self, expr):
        """
        extract Fn coefficients from given forumula
        This is done by setting all the exponents to zero and look at the
        remainer for each power of cosine
        """
        theta_s = sp.Symbol('theta_s')
        replacementsnull= {sp.cos(theta_s):0.}

        # construct a list of coefficients
        fn=[]
        fn= fn + [expr.xreplace(replacementsnull)]

        for nn in range(1,self.SRF.ncoefs+self.RV.ncoefs+1):
            replacementsnn = [(sp.cos(theta_s)**i,0.)  for i in range(1,self.SRF.ncoefs+self.RV.ncoefs+1) if i !=nn]
            replacementsnn = dict(replacementsnn + [(sp.cos(theta_s)**nn,1)])
            fn = fn + [(expr.xreplace(replacementsnn)-fn[0])]
        return fn






    def _calc_interaction_expansion(self):
        """
        calculate expensions to be able to analytically estimate Eq.23 needed for the interaction term
        The approach is as follows
        1) expand the legrende coefficents of the surface and volume phase functions
        2) replace the cosine terms in the Legrende polynomials by sines which corresponds to the intergration between 0 and 2*pi
        """
        # preevaluate expansions for volume and surface phase functions
        # this returns symbolic code to be then further used
        volexp = self.RV.legexpansion().doit()
        brdfexp = self.SRF.legexpansion().doit()


        #todo for efficency reasons this should be only done once and not for each angle !!!


        #   preparation of the product of p*BRDF for coefficient retrieval
        fPoly =(2*sp.pi*volexp*brdfexp).expand().doit()  # this is the eq.23. and would need to be integrated from 0 to 2pi     todo, why multiplicative factor of 2*pi???

        # do integration of eq. 23
        expr = self._integrate_0_2pi_phis(fPoly)

        # now we do still simplify the expression to be able to express things as power series of cos(theta_s)
        theta_s = sp.Symbol('theta_s')
        replacements = [(sp.sin(theta_s)**i,((1.-sp.cos(theta_s)**2.)**sp.Rational(i,2)).expand())  for i in range(1,self.SRF.ncoefs+self.RV.ncoefs+1) if i % 2 == 0]
        res = expr.xreplace(dict(replacements)).expand()

        # o.k., by now we have he integral formulation ready.
        return res

    def _gammafunkt(self, x):
        return (sp.factorial(x/2.)*(-4.)**(x/2.))/sp.factorial(x)*sp.sqrt(sp.pi)


    def _cosintegral(self, i):
        """
        integral of cos(x)**i in the interval 0 ... 2*pi
        """
        if i % 2 == 0.:  # origin of this formula? todo
            return 1./(2.*sp.pi)*(2.**(i+1)*sp.pi**2.)/(sp.factorial(i)*self._gammafunkt(i)**2.)
        else:
            # for odd exponents result is always zero
            return 0.

    def _integrate_0_2pi_phis(self, expr):
        """
        integrate from zero to 2pi for phi_s
        and return similified expression
        """
        phi_s = sp.Symbol('phi_s')

        # replace first all odd powers of sin(phi_s) as these are all zero for the integral
        replacements1 = [(sp.sin(phi_s)**i, 0.) for i in range(1,self.SRF.ncoefs+self.RV.ncoefs+5) if i % 2 == 1]
        res = expr.xreplace(dict(replacements1)).expand()

        # then subsitute the sine**2 by 1-cos**2
        replacements2 = [(sp.sin(phi_s)**i, ((1.-sp.cos(phi_s)**2)**sp.Rational(i,2)).expand()) for i in range(2,self.SRF.ncoefs+self.RV.ncoefs+5) if i % 2 == 0]
        res = res.xreplace(dict(replacements2)).expand()

        # integrate the cosine terms
        replacements3 = [(sp.cos(phi_s)**i,self._cosintegral(i)) for i in range(1,self.SRF.ncoefs+self.RV.ncoefs+5)]
        res = res.xreplace(dict(replacements3)).expand()
        return res



    def calc(self):
        """
        Perform actual calculation of bistatic scattering at top of the random volume (z=0; tau(z) = 0)

        Returns
        -------
        specific intensities Itot, Isurf, Ivol, Iint
        """
        # (16)
        Isurf = self.surface()
        if self.RV.tau > 0.:  # explicit differentiation for non-existing canopy, as otherwise NAN values
            Ivol = self.volume()
            Iint = self.interaction()
        else:
            Ivol = 0.
            Iint = 0.
        return Isurf + Ivol + Iint, Isurf, Ivol, Iint

    def surface(self):
        """
        (17)
        """
        return self.I0 * np.exp(-(self.RV.tau / self.mu_0) - (self.RV.tau/self.mu_ex)) * self.mu_0 * self.SRF.brdf(self.theta_0, self.theta_ex, self.phi_0, self.phi_ex)

    def volume(self):
        """
        (18)
        """
        return (self.I0*self.RV.omega*self.mu_0/(self.mu_0+self.mu_ex)) * (1.-np.exp(-(self.RV.tau/self.mu_0)-(self.RV.tau/self.mu_ex))) * self.RV.p(self.theta_0, self.theta_ex, self.phi_0, self.phi_ex)

    def interaction(self):
        """
        (19)
        """
        Fint1 = self._calc_Fint(self.mu_0, self.mu_ex)
        Fint2 = self._calc_Fint(self.mu_ex, self.mu_0)
        return self.I0 * self.mu_0 * self.RV.omega * (np.exp(-self.RV.tau/self.mu_ex) * Fint1 + np.exp(-self.RV.tau/self.mu_0)*Fint2 )

    def _calc_Fint(self, mu1, mu2):
        return 0.  # todo this is a dummy


    def _calc_Fintxx(self, mu1, mu2):
        """
        (37)
        """
        S = 0.

        for n in xrange(nmax):
            S2 = 0.
            for k in xrange(1,(n+1)+1):
                E_k1 = expn(k+1., self.RV.tau)
                S2 += mu1**(-k) * (E_k1 - np.exp(-self.RV.tau/mu1)/k)

            # final sum
            # todo check once more the function
            S += fn[n] * mu1**(n+1) * (np.exp(-self.RV.tau/mu1)*np.log(mu1/(1.-mu1)) - expi(-self.RV.tau) + np.exp(-self.RV.tau/mu1)*expi(self.RV.tau/mu1-self.RV.tau) + S2)

        return S


#   function that evaluates the coefficients
#~ def fnfunktexp(n,t0):
    #~ return fn[n].xreplace({thetaex:t0})
#~
#~
#~ #   definition of surface- volume and first-order interaction-term
#~ def CC(n,tau,tex):
    #~ if n==0:
        #~ return np.exp(-tau/np.cos(tex))*np.log(np.cos(tex)/(1-np.cos(tex)))-scipy.special.expi(-tau)+np.exp(-tau/np.cos(tex))*scipy.special.expi(tau/np.cos(tex)-tau)
    #~ else:
        #~ return CC(n-1,tau,tex)*np.cos(tex)-(np.exp(-tau/np.cos(tex))/n-scipy.special.expn(n+1,tau))
#~
#~ def intback(t0,tau,omega):
    #~ return omega*np.cos(t0)*np.exp(-tau/np.cos(t0))*np.sum(fnfunktexp(n,t0)*CC(n+1,tau,t0) for n in range(0,Np+NBRDF+1))






