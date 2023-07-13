import os
import pandas as pd


def get_subject_freesurfer_stats(stats_file_path):
    """
    Extract volumetric information on the file 'aseg.stats' from a single subject freesurfer processed data
    
    Parameters:
    stats_file_path (str): path to aseg.stats file (usually is processed_data_dir/subject/stats/aseg.stats)
    Returns:
    df_stats (pandas dataframe): dataframe containing the volumetric measures of the subject's brain
    
    """
    
    cols = ['Index','SegId','NVoxels','Volume_mm3','StructName',
                'normMean','normStdDev', 'normMin','normMax','normRange']

    with open(stats_file_path) as f:
        lines = [line for line in f.readlines() if not line.startswith('#')]
    data = [line.split() for line in lines]
    df_subject_stats = pd.DataFrame(data, columns = cols)
    df_subject_stats = df_subject_stats.set_index(df_stats['SegId'])
    
    return df_subject_stats


def get_freesurfer_stats(data_dir, num_subjects = False, subject_list = False):
    """
    Extract volumetric information from Freesurfer processed data.
    
    Parameters:
    data_dir (str): folder where the freesurfer results are stored 
              (data structure should be: data_dir/subject/stats/aseg.stats)
    num_subjects (int or False): number of subjects to process, if False process all subjects (default: False)
    subject_list (list or False): list of subjects to process, if False process all subjects (default: False)
    Returns:
    subjects_stats (dict of dicts): dict containing the volumetric measures of all processed subjects                
                  
    """
    
    if subject_list:
        subjects = subject_list
    else:
        subjects = os.listdir(data_dir)
        subjects.sort()
        if num_subjects: 
            subjects = subjects[:num_subjects] 
            
    subjects_stats = []
    for subject in subjects:
        stats_file_path = os.path.join(data_dir, subject, 'stats', 'aseg.stats')
        subjects_stats.append([subject, get_subject_freesurfer_stats(stats_file_path).to_dict()])
    stats = {entry[0]: entry[1] for entry in subjects_stats}
             
    return stats
    
