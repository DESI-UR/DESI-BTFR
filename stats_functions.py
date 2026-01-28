# import gc
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib

from scipy.optimize import curve_fit
import scipy.stats as stats

# matplotlib.rcParams['figure.dpi'] = 100
# matplotlib.rcParams['savefig.dpi'] = 300


def gaussian(x, x0, sigma):
    '''
    normal dist

    PARAMETERS
    ==========

    x : array
        data
    x0 : float
        mean
    sigma : float
        width
    
    RETURNS
    =======
    gaussian w parameters
    '''

    return 1/(np.sqrt(2*np.pi) * sigma) * np.exp(-(x-x0)**2/(2*sigma**2))

def fit_to_gaussian(binned_data, plot_dir='', plot_name='', bin_lab='' , bin_order='norm',plot_bins=[], xlab='', 
                    use_custom_bins=False, custom_bins=[], median_guess=False):
    '''
    fit gaussian dist to data and plot data, fit. bins must have at least 10
    data pts

    PARAMETERS
    ==========
    binned_data : array
        data in bins

    plot_dir : string
        file path for plots

    plot_name : string
        name to save plots

    bin_lab : string
        what each plot is a bin of, label for title

    bin_order : string
        'norm' or 'flip', default is 'norm', order of bins for plot titles (e.g. use flip for magnitudes)
    
    plot_bins : list
        bin edges that define each plot/gaussian dist

    xlab : string
        x-axis label for plots
    
    use_custom_bins : boolean
        default is False, True to manually define bins for each distribution

    custom_bins : list of arrays
        each array is the bins used to histogram the binned data

    RETURNS
    =======
    avgs : array
        gaussian mean in each bin
    sigmas : array
        width of gaussian for each bin
    
    '''

    avgs = np.ones(len(binned_data)) * np.nan
    sigmas = np.ones(len(binned_data)) * np.nan

    for i in range(len(binned_data)):

        data = binned_data[i]
        
        if use_custom_bins:
            counts, bins = np.histogram(data, bins=custom_bins[i], density=True)
        else:
            counts, bins = np.histogram(data, bins=int(np.sqrt(len(data))+1), density=True)
        bin_ctrs = (bins[1:] + bins[:-1])/2

        p0 = [ np.median(data), np.std(data)]
        if median_guess:
            p0 = [np.median(data), stats.median_abs_deviation(data)]

        if len(data) >= 10:


            try:
    
                popt, pcov = curve_fit(gaussian, bin_ctrs, counts, p0=p0)
                # mu, sig = stats.norm.fit(data)
    
            except:
    
                print(f'failed on bin {i}')
                continue
    
            avgs[i] = popt[0]
            # sigmas[i] = popt[2]/np.sqrt(len(data))
            sigmas[i] = popt[1]

            # avgs[i] = mu
            # sigmas[i] = sig
    
            

            xs = np.linspace(bins[0], bins[-1], 100)
            plt.plot(xs, gaussian(xs, popt[0], popt[1]), color='r', label=fr'$\mu$ = {popt[0]:.2}, $\sigma$ = {popt[1]:.2}')
            # plt.plot(xs, len(data)*(bin_ctrs[1] - bin_ctrs[0])*stats.norm.pdf(xs, mu, sig), 
                    #  color='r', label=fr'$\mu$ = {mu:.2}, $\sigma$ = {sig:.2}')

            plt.xlabel(xlab, fontsize=14)
        
            # plt.scatter(bin_ctrs, counts, 
            #         #  marker='.', color='k'
            #          )

            # plt.hist(bins[:-1], bins, weights=counts)

            plt.stairs(counts, bins)

            # plt.title(plot_name + f'_bin_{i}')

            if bin_order=='flip':
                plt.title(f'{plot_bins[i]:.2f} > {bin_lab} > {plot_bins[i+1]:.2f}', fontsize=14, y=1)

            else:

                plt.title(f'{plot_bins[i]:.2f} < {bin_lab} <  {plot_bins[i+1]:.2f}', fontsize=14, y=1)

            plt.tick_params( axis='both', direction='in', labelsize=12)

            plt.tight_layout()
            plt.savefig(plot_dir + plot_name + f'_bin_{i}' + '.png', bbox_inches='tight')
            plt.close()

        else:
            print(f'not enough data points in bin {i}')

    return avgs, sigmas