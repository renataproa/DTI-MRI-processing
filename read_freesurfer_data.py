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

def calculate_brain_vol_T1(T1_file_path):
    """
    Calculates the brain volume using the T1 image.
    
    Parameters: 
    T1_file_path (str): path to a T1 image nii file (.nii.gz). 
    Returns:
    total_brain_vol_T1 (float): calculated brain volume in mm3 from T1 image.
    
    """
    nii_data = nib.load(T1_file_path) 
    data_T1 = nii_data.get_fdata()
    
    empty = len(np.where(data_T1 == 0)[0]) 
    total = data_T1.shape[0]*data_T1.shape[1]*data_T1.shape[2]
    mask = total - empty
    header = nii_data.header
    T1_vox_dims = header.get_zooms() #get the voxel sizes in millimeters in T1 space
    T1_vox_mm3 = T1_vox_dims[0]*T1_vox_dims[1]*T1_vox_dims[2]
    total_brain_vol_T1 = mask*T1_vox_mm3    
    
    return total_brain_vol_T1


def calculate_brain_vol_FSmask(FSseg_file_path, vox_dims):
    """
    Calculates the brain volume using the FreeSurfer segmentation mask.
    
    Parameters: 
    FSseg_file_path (str): path to the FreeSurfer segmentation nii file (.nii.gz).
    vox_dims: voxel dimensions in mm3 (depends on what space the segmentation is in. 
              For example: if the segmenation is in the diffusion space, the vox_dims 
              is the voxel dimension in the diffusion space).  
    Returns:
    total_brain_vol (float): calculated brain volume in mm3 from the FreeSurfer segmentation mask.
    
    """
    nii_data = nib.load(FSseg_file_path) 
    FSseg = nii_data.get_fdata().squeeze() #volume
    
    empty = len(np.where(FSseg == 0)[0])
    total = FSseg.shape[0]*FSseg.shape[1]*FSseg.shape[2]
    mask = total - empty
    total_brain_vol = mask*vox_dims
    
    return total_brain_vol


def int_to_onehot(matrix, onehot_type=np.dtype(np.float32)):
    #Thanks to Gustavo
    
    labels = np.unique(matrix)
    vec_len = len(labels)
    onehot = np.zeros((vec_len,) + matrix.shape, dtype=onehot_type)  
    for i, label in enumerate(labels):
        onehot[i] = (matrix == label)   
    return labels, onehot

def get_freesurfer_masks(FSseg_file_path):
    """
    Gets the ROIs' masks from the Freesurfer Segmentation.
    
    Parameters: 
    FSseg_file_path (str): path to the FreeSurfer sugmentation nii file (.nii.gz).
  
    Returns:
    FSseg_onehot (numpy array): onehot encoded masks for ROIs
    labels (numpy array): list of ROIs' labels
    
    """
    
    nii_data = nib.load(FSseg_file_path)
    FS_seg = nii_data.get_fdata().squeeze() #volume
    labels, FSseg_onehot = int_to_onehot(FS_seg, onehot_type=np.dtype(np.bool))
    
    return FSseg_onehot, labels





    
