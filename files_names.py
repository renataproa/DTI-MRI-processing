FA = 'dti_FA.nii.gz'
MD = 'dti_MD.nii.gz'
L1 = 'dti_L1.nii.gz' 
L2 = 'dti_L2.nii.gz'
L3 = 'dti_L3.nii.gz'

# inside folder 'FSL'
FSLseg = 'FSLmask_reg2_S0_linear.nii.gz' # DTI space (linear reg)
FSLseg_lnl = 'FSLmask_reg2_S0_linearnlinear.niinge' # DTI space (linear + nonlinear reg)
FSLseg_orig = 'T1_first_all_fast_firstseg_orig.nii.gz' # original space
FSLseg_mne = 'T1_first_all_fast_firstseg.nii.gz' # standard space

# inside folder 'FreeSurfer'
FSseg = 'aparc+aseg_diffspace_linear_BETfree.nii.gz' # DTI space (linear reg)
FSseg_lnl = 'aparc+aseg_diffspace_linearnlinear_BETfree.nii.gz' # DTI space (linear + nonlinear reg)
FSseg_orig = 'aparc+aseg_origspace.nii.gz' # original space
FSseg_mne = 'aparc+aseg.nii.gz' # standard space

def T1 (subject):
  return str('T1_' + subject + '.nii.gz')
  
