import pandas as pd
import numpy as np
import wfdb
from wfdb import processing

import sys
sys.path.append("/home/singuyen/project_biosignal/scripts/c-labpl.qrs_detector.master")

from QRSDetectorOffline import QRSDetectorOffline


class QRSeeker(object):
    def __init__(self, record_path, channels, findpeaks_limit, findpeaks_spacing_factor, 
                 verbose=True, log_data=False, plot_data=False, show_plot=False):
        
        self.record_path = record_path
        self.channels = channels
        
        self.signal = None
        self.record_fields = None
        self.data = None
        self.data_length = None
        self.sampling_freq = None
        self.time = None
        self.file = pd.DataFrame()
        self.file_name = '/tmp/' + self.record_path.split("/")[-1] + ".csv"
        
        self.findpeaks_limit = findpeaks_limit
        self.findpeaks_spacing_factor = findpeaks_spacing_factor
        self.detector_configs = [verbose, log_data, plot_data, show_plot]
        
        self.qrs_detector = None
        self.detected_inds = None
                       
        self.ref_annotator = wfdb.rdann(self.record_path, 'atr')
        self.ref_annotation = self.ref_annotator.sample
        
        self.qrs_validator = None 

        self.matched_ref_inds = np.nan
        self.matched_test_inds = np.nan
        self.unmatched_ref_inds = np.nan
        self.unmatched_test_inds = np.nan

        self.true_positive = np.nan
        self.false_positive = np.nan
        self.false_negative = np.nan

        self.specificity = np.nan
        self.positive_predictivity = np.nan
        self.fpr = np.nan
        
        self.write_data_2csv()
        
        self.qrs_seeking()
        
        if (self.detected_inds is None) | (len(self.qrs_detector.qrs_peaks_indices) == 0):
            print("No peak was detected !")
            
        elif len(self.detected_inds) < (len(self.ref_annotation)*0.85):
            print("Insufficient number of peaks detected - less than 85% of reference peaks !")
            
        else:
            print("Number of peaks detected >= 85% of number of reference peaks \m/")
            self.validation()
    
    def write_data_2csv(self):
        self.signal, self.record_fields = wfdb.rdsamp(self.record_path, channels=self.channels) 
        self.data = np.mean(self.signal, axis=1)
        self.sampling_freq = self.record_fields['fs']
        self.data_length = self.record_fields['sig_len']

        self.time = np.linspace(0, self.data_length/self.sampling_freq, self.data_length)
        
        self.file['timestamp'] = self.time
        self.file['ecg_measurement'] = self.data
        self.file.to_csv(self.file_name, index=False)
    
    def qrs_seeking(self):
        self.qrs_detector = QRSDetectorOffline(ecg_data_path = self.file_name, fs = self.sampling_freq, 
                                               findpeaks_limit = self.findpeaks_limit, 
                                               findpeaks_spacing_factor = self.findpeaks_spacing_factor,
                                               verbose = self.detector_configs[0], log_data = self.detector_configs[1], 
                                               plot_data = self.detector_configs[2], show_plot = self.detector_configs[3])
        
        self.detected_inds = self.qrs_detector.qrs_peaks_indices
        
    def validation(self):
        self.qrs_validator = processing.compare_annotations(ref_sample = self.ref_annotation,
                                                            test_sample = np.array(self.detected_inds),
                                                            window_width = int(0.1 * self.sampling_freq),
                                                            signal = self.signal)
        
        self.matched_ref_inds = self.qrs_validator.matched_ref_inds
        self.matched_test_inds = self.qrs_validator.matched_test_inds
        self.unmatched_ref_inds = self.qrs_validator.unmatched_ref_inds
        self.unmatched_test_inds = self.qrs_validator.unmatched_test_inds

        self.true_positive = self.qrs_validator.tp
        self.false_positive = self.qrs_validator.fp
        self.false_negative = self.qrs_validator.fn

        self.specificity = self.qrs_validator.specificity
        self.positive_predictivity = self.qrs_validator.positive_predictivity
        self.fpr = self.qrs_validator.false_positive_rate
        
