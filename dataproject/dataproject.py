import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import datetime

import pandas_datareader


def figure1(gdp, nber, start, end):
    """
    Plots time series of gdp and gdp growth
    
    Args:
        gdp (pandas.Dataframe): gdp data
        nber (pandas.Dataframe): recession indicator
        start (float): start date
        end (float): end date
    
    Returns:
       Figure with gdp and gdp growth
    """
    # Plot of Figure 1
    fig, (fig1, fig1_2) = plt.subplots(2, figsize=(14,7))

    # Plot GDP in absolute values
    fig1.plot(gdp, label='GDP')
    fig1.set_xlim(start, end)
    fig1.grid(axis='y')
    fig1.set_ylabel('Billion of dollars')
    fig1.set_title('(a)')

    # Plot GDP growth rate
    gdp_g = gdp.pct_change()*100
                        
    fig1_2.plot(gdp_g, label='GDP growth')
    fig1_2.set_xlim(start, end)
    fig1_2.grid(axis='y')
    fig1_2.set_ylabel('Percent %')
    fig1_2.axhline(y=0, color='black')
    fig1_2.set_title('(b)')


    # Recession shade
    for i in range(len(nber)):
        if nber['USREC'].iloc[i] == 1:
            fig1.axvspan(nber.index[i-1], nber.index[i], alpha=0.2, color='gray')
            fig1_2.axvspan(nber.index[i-1], nber.index[i], alpha=0.2, color='gray')
        if nber['USREC'].iloc[i] == 0:
            fig1.axvspan(nber.index[i-1], nber.index[i], alpha=1, color='white')
            fig1_2.axvspan(nber.index[i-1], nber.index[i], alpha=1, color='white')

    # Set title and textbox for annotation
    fig.suptitle('Figure 1. GDP and GDP growth', fontsize="16")
    fig.text(0.5, 0, 'Source: Federal Reserve Economic Data (FRED)\nAnnotation: Shaded areas are NBER defined recessions', transform=fig.transFigure, fontsize=12, horizontalalignment='center')

    # Show plot
    plt.show()

def figure2(yield_curves, nber, start, end):
    """
    Plots different yield curves
    
    Args:
        yield_curves (pandas.Dataframe): data for yield curves
        nber (pandas.Dataframe): recession indicator
        start (float): start date
        end (float): end date
    
    Returns:
       Figure with yield curves and recession shading
    """
    # Plot of Figure 2
    fig, fig2 = plt.subplots(figsize=(14,7))

    fig2.plot(yield_curves['10Y-3M'], label='10 year - 3 month treasury yield spread')
    fig2.plot(yield_curves['10Y-2Y'], label='10 year - 2 year treasury yield spread')
    fig2.plot(yield_curves['10Y-FFR'], label='10 year - federal funds rate spread')

    # Set title, labebls, legends and textbox
    fig2.set_title('Figure 2. Different yield curves')
    fig2.set_xlabel('Date')
    fig2.set_ylabel('Percent %')
    fig2.set_xlim(start, end)
    fig2.legend()
    fig2.text(12000, -2.5,'Source: Federal Reserve Economic Data (FRED)\nAnnotation: Shaded areas are NBER defined recessions',ha='center')

    # Gridlines
    fig2.grid(axis='y')
    fig2.axhline(y=0, color='black')

    # Recession shade
    for i in range(len(nber)):
        if nber['USREC'].iloc[i] == 1:
            fig2.axvspan(nber.index[i-1], nber.index[i], alpha=0.2, color='gray')
        if nber['USREC'].iloc[i] == 0:
            fig2.axvspan(nber.index[i-1], nber.index[i], alpha=1, color='white')
    # Show plot
    plt.show()
