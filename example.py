'''
example to collect 2-port S-parameters with switch terms.
You can modify it to your needs.
'''

import numpy as np
import skrf as rf
import os
import zipfile

# my script to control the VNA
import zva as vna
# import zna as vna

def export_s2p(meas, f, folder_path, filename, skip_dir=False):
    # meas: array of multiple iteration. index [iter, para, freq]
    # f: array of the frequency (common to all data)
    if not skip_dir:
        os.mkdir(folder_path + '\\' + filename)
        
    freq = rf.Frequency.from_f(f, unit='Hz')
    freq.unit = 'GHz'
    N = len(freq.f)
    for inx, data in enumerate(meas):
        S_para = np.array([[s11,s12], [s21,s22]] for s11,s12,s21,s22 in zip(data[0],data[1],data[2],data[3]))
        Switch_terms = np.array([[0,Gamma12], [Gamma21,0]] for Gamma21,Gamma12 in zip(data[4],data[5]))

        NW = rf.Network(s=S_para, frequency=freq, name = filename + f'_S_param_{inx+1:0{len(str(N))}d}')
        NW.write_touchstone(filename = filename + f'_S_param_{inx+1:0{len(str(N))}d}', 
                            dir = folder_path + '\\' + filename + '\\', skrf_comment=False)

        NW = rf.Network(s=Switch_terms, frequency=freq, name = filename + f'_switch_{inx+1:0{len(str(N))}d}')
        NW.write_touchstone(filename = filename + f'_switch_{inx+1:0{len(str(N))}d}', 
                            dir = folder_path + '\\' + filename + '\\', skrf_comment=False)
        
def compress_folder(folder_path, filename):
    # compress the folder
    zip_filename = folder_path + filename + '.zip'
    if os.path.isfile(zip_filename):
        print(f'The file {zip_filename} already exists.')
        return None
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(folder_path + filename):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.basename(file_path))


if __name__=='__main__':
    folder_path = os.path.dirname(os.path.realpath(__file__))
    
    filename = 'measurement_name'
    
    os.mkdir(folder_path + '\\' + filename)

    #######---NOTE---######
    '''
    For this example, for the reconstruction of the collected data to look correctly, you need to make sure
    that the traces on the VNA in following definition, creation order, and in channel 1: 
    Tr1: S11
    Tr2: S12
    Tr3: S21
    Tr4: S22
    Tr5: a2/b2 | P1  (forward switch term)
    Tr6: a1/b1 | P2  (reverse switch term)

    You can check the definition of the traces and order from the variable "trace_definitions" below.
    '''
    #######---////---######

    frequencies, measurements, trace_definitions = vna.read_traces(address='TCPIP::192.168.0.30::INSTR', 
                                                                   num_sweeps=100, turn_fact_cal_off=True)
    f = frequencies[0]     # take data only from first listed channel
    meas = measurements[0] # take data only from first listed channel

    export_s2p(meas, f, folder_path=folder_path, filename=filename, skip_dir=True)

    compress_folder(folder_path + '\\', filename)  # compress all touchstone files to a zip file
