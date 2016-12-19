"""
Class for quick visualization of results and used phasefunctions

polarplot() ... plot p and the BRDF as polar-plot

"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scatter import Scatter

class Plots(Scatter):
    """
    Parameters:
        R ... RT1 class object
    """
    def __init__(self, **kwargs):
        pass
    

    def polarplot(self, R = None, SRF = None, V = None, incp = [15.,35.,55.,75.], incBRDF = [15.,35.,55.,75.], pmultip = 2., BRDFmultip = 1.):
        """
        generate a polar-plot of the volume- and the surface scattering phase function
        together or in separate plots. 
        The used approximation in terms of legendre-polynomials is also plotted as dashed line.
        
        
        Parameters:
        
            R	   ... a RT1 object 
            SRF     ... a rt1.surface module
            V       ... a rt1.volume module
        
        Optional Parameters:
            incp        ... incidence-angles [deg] at which the volume-scattering phase-function will be plotted 
            incBRDF     ... incidence-angles [deg] at which the BRDF will be plotted
        
            
            pmultip     ... multiplicator of max-plotrange for p     (in case the chosen plotranges are not satisfying)
            BRDFmultip  ... multiplicator of max-plotrange for BRDF
        
            max-plotrange for p is given by the max. value of p in forward-direction (for the chosen incp)
            and for the BRDF by the max. value of the BRDF in specular direction (for the chosen incBRDF)
        """
        
       
        assert isinstance(incp,list), 'Error: incidence-angles for polarplot of p must be a list'
        assert isinstance(incBRDF,list), 'Error: incidence-angles for polarplot of the BRDF must be a list'
        for i in incBRDF: assert i<=90, 'ERROR: the incidence-angle of the BRDF in polarplot must be < 90'
        
        assert isinstance(pmultip,float), 'Error: plotrange-multiplier for polarplot of p must be a floating-point number'
        assert isinstance(BRDFmultip,float), 'Error: plotrange-multiplier for polarplot of the BRDF must be a floating-point number'

        if R==None and SRF==None and V==None:
            assert False, 'Error: You must either provide R or SRF and/or V'
            
                
        # if R is provided, use it to define SRF and V, else use the provided functions
        if R !=None:
            SRF = R.SRF
            V = R.RV
            
        # define functions for plotting that evaluate the used approximations in terms of legendre-polynomials
        n = sp.Symbol('n')        
        

        if V != None:
            # define a plotfunction of the analytic form of p
            phasefunkt = sp.lambdify(('theta_i', 'theta_s', 'phi_i', 'phi_s'), V._func,"numpy") 
            # define a plotfunction of the legendre-approximation of p
            phasefunktapprox = sp.lambdify(('theta_i', 'theta_s', 'phi_i', 'phi_s'), sp.Sum(V.legcoefs*sp.legendre(n,self.thetap('theta_i','theta_s','phi_i','phi_s')),(n,0,V.ncoefs-1)).doit(),"numpy") 

            # plot of volume-scattering phase-function
            if SRF == None:
                # if SRF is None, plot only a single plot of p
                polarfig = plt.figure(figsize=(7,7))
                polarax = polarfig.add_subplot(111,projection='polar')
            else:
                # plot p and the BRDF together
                polarfig = plt.figure(figsize=(14,7))
                polarax = polarfig.add_subplot(121,projection='polar')
            
            # set incidence-angles for which p is calculated
            plottis=np.deg2rad(incp)
            colors = ['r','g','b', 'k','c','m','y']*(len(plottis)/7+1)
            # reset color-counter
            i=0
            
            pmax = pmultip*max(phasefunkt(plottis, np.pi-plottis, 0., 0.))
            
            for ti in plottis:
                color = colors[i]
                i=i+1
                thetass = np.arange(0.,2.*np.pi,.01)
                rad=phasefunkt(ti, thetass, 0., 0.)
                radapprox=phasefunktapprox(ti, thetass, 0., 0.)
                
                polarax.set_theta_direction(-1)   # set theta direction to clockwise
                polarax.set_theta_offset(np.pi/2.) # set theta to start at z-axis
                
                polarax.plot(thetass,rad, color)
                polarax.plot(thetass,radapprox, color+'--')
                polarax.arrow(-ti,pmax*1.2  ,0.,-pmax*0.8, head_width = .0, head_length=.0, fc = color, ec = color, lw=1, alpha=0.3)
                polarax.fill_between(thetass,rad,alpha=0.2, color=color)
                polarax.set_xticklabels(['$0^\circ$','$45^\circ$','$90^\circ$','$135^\circ$','$180^\circ$'])
                polarax.set_yticklabels([])
                polarax.set_rmax(pmax*1.2)
                polarax.set_title('Volume-Scattering Phase Function \n')
            
   
                
        if SRF !=None:
            # define a plotfunction of the analytic form of the BRDF
            brdffunkt = sp.lambdify(('theta_i', 'theta_s', 'phi_i', 'phi_s'), SRF._func,"numpy") 
            # define a plotfunction of the analytic form of the BRDF
            brdffunktapprox = sp.lambdify(('theta_i', 'theta_s', 'phi_i', 'phi_s'), sp.Sum(SRF.legcoefs*sp.legendre(n,self.thetaBRDF('theta_i','theta_s','phi_i','phi_s')),(n,0,SRF.ncoefs-1)).doit(),"numpy") 
     
      
            # plot of BRDF
            if V == None:
                # if V is None, plot only a single plot of the BRDF
                polarfig = plt.figure(figsize=(7,7))
                polarax = polarfig.add_subplot(111,projection='polar')
            else: 
                # plot p and the BRDF together
                polarax = polarfig.add_subplot(122,projection='polar')
            
            # set incidence-angles for which the BRDF is calculated
            plottis=np.deg2rad(incBRDF)
            colors = ['r','g','b', 'k','c','m','y']*(len(plottis)/7+1)
            i=0
            
            brdfmax = BRDFmultip*max(brdffunkt(plottis, plottis, 0., 0.))
            
            for ti in plottis:
                color = colors[i]
                i=i+1
                thetass = np.arange(-np.pi/2.,np.pi/2.,.01)
                rad=brdffunkt(ti, thetass, 0., 0.)
                radapprox = brdffunktapprox(ti, thetass, 0., 0.)
                
                polarax.set_theta_direction(-1)   # set theta direction to clockwise
                polarax.set_theta_offset(np.pi/2.) # set theta to start at z-axis
                
                polarax.plot(thetass,rad, color)
                polarax.plot(thetass,radapprox, color + '--')
                polarax.fill(np.arange(np.pi/2.,3.*np.pi/2.,.01),np.ones_like(np.arange(np.pi/2.,3.*np.pi/2.,.01))*brdfmax*1.2,'k')
            
            
                polarax.arrow(-ti,brdfmax*1.2  ,0.,-brdfmax*0.8, head_width =.0, head_length=.0, fc = color, ec = color, lw=1, alpha=0.3)
                polarax.fill_between(thetass,rad,alpha=0.2, color=color)
                polarax.set_xticklabels(['$0^\circ$','$45^\circ$','$90^\circ$'])
                polarax.set_yticklabels([])
                polarax.set_rmax(brdfmax*1.2)
                polarax.set_title('Surface-BRDF\n')

        
        
        


        
        
    def logmono(self, inc, Itot=None, Isurf= None, Ivol = None, Iint=None, ylim = None, sig0=False, fractions = True, label = None):
        """
        plot either backscattered intensity or sigma_0 in dB
        
        Parameters:
             
        inc ...     incidence-angle range used for calculating the intensities
                    (array)
           
        Itot, Ivol, Isurf, Iint ... individual signal contributions, i.e. outputs from RT1.calc()
                    (array's of same length as inc)        
        
        sig0 ... If True, sigma0 will be plotted which is related to I via:  sigma_0 = 4 Pi cos(inc) * I             
                    (True, False)
                    
        ylim ... manual entry of plot-boundaries as [ymin, ymax]
                
        label ...   manual label of plot        
        """
        
        assert isinstance(inc,np.ndarray), 'Error, inc must be a numpy array'
    
        if Itot is not None: assert isinstance(Itot,np.ndarray), 'Error, Itot must be a numpy array'
        if Itot is not None: assert len(inc) == len(Itot), 'Error: Length of inc and Itot is not equal'

        if Isurf is not None: assert isinstance(Isurf,np.ndarray), 'Error, Isurf must be a numpy array'
        if Isurf is not None: assert len(inc) == len(Isurf), 'Error: Length of inc and Isurf is not equal'

        if Ivol is not None: assert isinstance(Ivol,np.ndarray), 'Error, Ivol must be a numpy array'
        if Ivol is not None: assert len(inc) == len(Ivol), 'Error: Length of inc and Ivol is not equal'
        
        if Iint is not None: assert isinstance(Iint,np.ndarray), 'Error, Iint must be a numpy array'
        if Iint is not None: assert len(inc) == len(Iint), 'Error: Length of inc and Iint is not equal'
        
        if label is not None:assert isinstance(label,str), 'Error, Label must be a string'
     
        
        if ylim is not None: assert len(ylim)!=2, 'Error: ylim must be an array of length 2!   ylim = [ymin, ymax]'
        if ylim is not None: assert isinstance(ylim[0],(int,float)), 'Error: ymin must be a number'
        if ylim is not None: assert isinstance(ylim[1],(int,float)), 'Error: ymax must be a number'
        
        assert isinstance(sig0,bool), 'Error: sig0 must be either True or False'
        assert isinstance(fractions,bool), 'Error: fractions must be either True or False'


        ctot='black'
        csurf='red'
        cvol='green'
        cint='blue'      
            
        
        if sig0 == True:
            #  I..  will be multiplied with sig0  to get sigma0 values instead of normalized intensity
            signorm = 4.*np.pi*np.cos(np.deg2rad(inc))
        else:
            signorm = 1.
        
        if fractions == True:
            f = plt.figure(figsize=(14,7))
            ax = f.add_subplot(121)
            ax2 = f.add_subplot(122)
        else:
            f = plt.figure(figsize=(7,7))
            ax = f.add_subplot(111)

        ax.grid()
        ax.set_xlabel('$\\theta_0$ [deg]')
        
        if sig0 == True:
            if Itot is not None: ax.plot(inc, 10.*np.log10(signorm*Itot), color=ctot, label='$\\sigma_0^{tot}$')
            if Isurf is not None: ax.plot(inc, 10.*np.log10(signorm*Isurf), color=csurf, label='$\\sigma_0^{surf}$')
            if Ivol is not None: ax.plot(inc, 10.*np.log10(signorm*Ivol), color=cvol, label='$\\sigma_0^{vol}$')
            if Iint is not None: ax.plot(inc, 10.*np.log10(signorm*Iint), color=cint, label='$\\sigma_0^{int}$')
            
            if label == None:
                ax.set_title('Bacscattering Coefficient')
            else:
                ax.set_title(label)
            
            ax.set_ylabel('$\\sigma_0$ [dB]')

                
        else:
            if Itot is not None: ax.plot(inc, 10.*np.log10(signorm*Itot), color=ctot, label='$I_{tot}$')
            if Isurf is not None: ax.plot(inc, 10.*np.log10(signorm*Isurf), color=csurf, label='$I_{surf}$')
            if Ivol is not None: ax.plot(inc, 10.*np.log10(signorm*Ivol), color=cvol, label='$I_{vol}$')
            if Iint is not None: ax.plot(inc, 10.*np.log10(signorm*Iint), color=cint, label='$I_{int}$')
            
            if label == None:
                ax.set_title('Normalized Intensity')
            else:
                ax.set_title(label)
            
            ax.set_ylabel('$I^+$ [dB]')
        ax.legend()
        
        if ylim == None:
            if Itot is not None and Iint is not None: ax.set_ylim(np.nanmax(10.*np.log10(signorm*Iint))-5.,np.nanmax(10.*np.log10(signorm*Itot))+5)
        else:
            ax.set_ylim(ylim[0],ylim[1])
        
        if fractions == True:    
            # plot fractions
            if Itot is not None and Isurf is not None: ax2.plot(inc, Isurf/Itot, label='surface', color=csurf)
            if Itot is not None and Ivol is not None: ax2.plot(inc, Ivol/Itot, label='volume', color=cvol)
            if Itot is not None and Iint is not None: ax2.plot(inc, Iint/Itot, label='interaction', color=cint)
            ax2.set_title('Fractional contributions to total signal')
            ax2.set_xlabel('$\\theta_0$ [deg]')
            if sig0 == True:
                ax2.set_ylabel('$\\sigma_0 / \\sigma_0^{tot}$')
            else:
                ax2.set_ylabel('$I / I_{tot}$')
            ax2.grid()
            ax2.legend()
        
        plt.show()