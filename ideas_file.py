import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
from matplotlib import gridspec

path = '/ligo/home/carlos.campos/Downloads/seismo_test_cal_2024-10-01T22-07-09-752.csv'


################################################################################################################################

print('thinking...')
metadata_rows = []
metadata = {}

with open(path, 'r') as f:
    for _ in range(5):
        metadata_rows.append(f.readline().strip()) 

for row in metadata_rows:
    if ':' in row: 
        key, value = row.split(':', 1)
        metadata[key.strip()] = value.strip()
        

mag = pd.read_csv(path, skiprows=5, delimiter=',')

#mag.columns = ['Sample', 'Time (s)', 'Noise (V)', 'Voltage X (V)', 'Voltage Y (V)', 'Voltage Z (V)', 'blank']

samples = mag['Sample']
times = mag['Time (s)']
#noi = mag['Noise (V)'] * (1.222e-05)/21 
z = mag['Channel Z (V)'] * (1.222e-05)/21 #--------------- This is the conversion factor for Volts to Tesla -------------------#
y = mag['Channel N (V)'] * (1.222e-05)/21
x = mag['Channel E (V)'] * (1.222e-05)/21


########################################### This is the sample rate from the metadata ##########################################

sr = float(metadata['Sample Rate'])
print('\nSample Rate: ' + metadata['Sample Rate'])












def asd(data_z, data_n, data_e, sample_rate, lf, lx, ly, lz, 
        bart_sample_rate, bart_x, bart_y, bart_z, frequency,
        over_lap, fft, signal_prom, ymin, ymax, xmin, xmax, func, channel):
    
#------------------------------------------------------------------------------------------------------------------------------#

    def peaks(signal_freq, signal_log, frequency, signal_prom):
            tolerance = 1

            if frequency is None:
                peak, _ = signal.find_peaks(signal_log,
                                              prominence = signal_prom)
            
            else:
                mask = (signal_freq >= frequency - tolerance) & (signal_freq <= frequency + tolerance)
                peaks_local, _ = signal.find_peaks(signal_log[mask], prominence = signal_prom)

                peak = np.where(mask)[0][peaks_local]

            return peak

#------------------------------------------------------------------------------------------------------------------------------#

    # Helper: Welch
    def spectrum(data, sr):
        f, Pxx = signal.welch(
            data, sr, window = 'hamming',
            nperseg = sr * fft,
            noverlap = round(sr * (over_lap * 0.01))
        )
        return f, np.sqrt(Pxx)

#------------------------------------------------------------------------------------------------------------------------------#
    
    # ---------------- Compute spectra for Z, N, E ----------------
    input_data = {
        'z': data_z,
        'n': data_n,
        'e': data_e
    }

    results = {}

    for key, data in input_data.items():
        if data is None:
            continue

        signal_f, amp = spectrum(data, sample_rate)
        log_amp = np.log(amp)

        disp = amp / (2 * np.pi * signal_f) if func == 'displacement' else None
        peak_gquux = peaks(signal_f, log_amp, frequency, signal_prom)
        
        results[key] = {
            'frequency': signal_f,
            'amp': amp,
            'disp': disp,
            'peaks': peak_gquux
        }

    # ---------------- Compute reference (if not provided) ----------------
    if lf is None or lx is None or ly is None or lz is None:

        ref_data = {'x': bart_x, 'y': bart_y, 'z': bart_z}
        ref_out = {}
        
        for key, data in ref_data.items():
            if data is None:
                continue

            lf, amp = spectrum(data, bart_sample_rate)
            ref_out[key] = amp
        
        lx, ly, lz = ref_out.get('x'), ref_out.get('y'), ref_out.get('z')

    ## ------------------------------------------------------------------------------------- ##
    ## ------------------------------------------------------------------------------------- ##

    # ---------------- Plotting ----------------
    plt.figure(figsize = (20, 8))

    plt.yscale('log')
    plt.xscale('log')


    color_map = {'z': 'black', 'n': 'red', 'e': 'blue'}
    label_map = {'z': 'Z', 'n': 'N', 'e': 'E'}
    ctrl_map   = {'z': lz, 'n': ly, 'e': lx}
    title_map = {'z': drctn_title[2], 'n': drctn_title[1], 'e': drctn_title[0]}


    ## ------------------------------------------------------------------------------------- ##

    # Decide which channels to plot
     
    if func == 'velocity':
        ylabel = v_label 
        title = v_title

    else:
        ylabel = s_label
        title = s_title

    if channel == 'all':
        channels_to_plot = ['z', 'n', 'e']

    else:
        channels_to_plot = [channel[0]]  # 'zed' -> 'z', etc
        title = title_map[channels_to_plot[0]]

#------------------------------------------------------------------------------------------------------------------------------#

    for ch in channels_to_plot:
        if ch not in results:
            continue

        if func == 'velocity':
            y = results[ch]['amp'] 
        else:
            y = results[ch]['disp']
            
        f = results[ch]['frequency']
        peaks_gquux = results[ch]['peaks']
        

        plt.plot(f, y, color = color_map[ch], linewidth = 1.75, label = label_map[ch])
        

        if ctrl_map[ch] is not None:
            plt.plot(lf, ctrl_map[ch], color = 'dimgrey', linewidth = 2, alpha = 0.5, label = f'Reference {label_map[ch]}')

        # Mark peaks
        if len(f[peaks_gquux]) != 0:
            plt.scatter(f[peaks_gquux], y[peaks_gquux], s = 100, color = 'limegreen', marker = 'x', linewidths = 2.5)
            
            if frequency is not None:
                print(f'{title_map[ch]}:\n{f[peaks_gquux][0]:.2f} Hz \nAmpl: {y[peaks_gquux][0]:.3e}\n')
        else:
            print(f"No peaks in the {label_map[ch]} directions\n")

    ## ------------------------------------------------------------------------------------- ##

    ax = plt.gca()
    plt.legend(loc = 'lower left', fontsize = 14.5, ncol = 2)

    plt.title('FFT: ' + str(fft) + 's', fontsize = 18, loc = 'left',style = 'italic')
    plt.title('Overlap: ' + str(over_lap) + '%', fontsize = 18, loc = 'right',style = 'italic')
    plt.title(title, fontweight = 'bold', fontsize = 25)
    
    plt.xlabel('Frequency [Hz]', fontweight='bold', fontsize = 20)
    plt.ylabel(ylabel, fontweight = 'bold', fontsize = 20)

    plt.yticks(fontsize = 20, fontweight = "bold")
    ax.tick_params(axis='both', which='minor', labelsize = 20) 
    
    plt.xticks(fontsize = 20, fontweight = "bold")
    ax.tick_params(axis = 'both', which = 'minor', labelsize = 20)
    
    plt.ylim(ymin, ymax)
    plt.xlim(xmin, xmax)

    plt.grid(True, which = 'both', ls = '-')
    plt.tight_layout()
    plt.show()


################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------#
################################################################################################################################

x_max = 100 ## in terms of frequency
x_min = 0.1

x_max_p = 100
x_min_p = 0.1

## Velocity Y limits
y_max = 10e-6 ## in terms of ms⁻¹/√Hz
y_min = 10e-13

y_max_p = 10e-6 
y_min_p = 10e-13  

## Displacement Y Limits
my_max = 10e-7 ## in terms of m/√Hz
my_min = 10e-15

my_max_p = 10e-7
my_min_p = 10e-15

## fft length
fft_length = 128 ## in terms of seconds

fft_length_p = 128

## Precent FFT Overlap
overlap = 50 ## 50% fft overlap

overlap_p = 50

## Peak Promience
prom = 5

prom_p = 5

## Plot labels
v_title = 'Seismic Velocity Data ASD'
s_title = 'Seismic Dispacement Data ASD'
drctn_title = ['E Direction', 'N Direction', 'Z Direction']
v_label = 'Amplitude [ms⁻¹/√Hz]'
s_label = 'Amplitude [m/√Hz]'


#----------------------------------------------------- Plots Velocity ---------------------------------------------------------#
asd(z, y, x, sr, None, None, None, None, None, None, None, None, None,
        overlap, fft_length, prom, y_min, y_max, x_min, x_max, 'velocity', 'all')


#---------------------------------------------------- Plots Displacement ------------------------------------------------------#
asd(z, y, x, sr, None, None, None, None, None, None, None, None, None,
            overlap, fft_length, prom, my_min, my_max, x_min, x_max, 'displacement', 'north')


freq = 85
freq_min = freq - 1
freq_max = freq + 1



asd(z, y, x, sr, None, None, None, None, None, None, None, None, freq,
    overlap, fft_length, prom, y_min, y_max, freq_min, freq_max, "velocity", "north")
