import nibabel as nib

def get_DTI_space_vox_dims(dti_file_path):
    """
    Calculates the dimentions of the DTI voxel in mm3 in the diffusion space.
    
    Parameters: 
    dti_file_path (str): path to a DTI compressed nii file (.nii.gz). Example: 'dti_FA.nii.gz'.
    Returns:
    vox_mm3 (float): voxel dimentions in mm3.
    
    """
    nii_data = nib.load(dit_file_path)
    header = nii_data.header
    vox_dims = header.get_zooms() #get the voxel sizes in millimeters in the DTI space
    vox_mm3 = vox_dims[0]*vox_dims[1]*vox_dims[2]
    
    return vox_mm3
