def check_files(data_dir, files_list):
    """
    Checks which subjects have the desired files.
    
    Parameters: 
    data_dir (str): folder containing the data organized in folders by subject.
    files_list (list): files to check (obs: is the file is in a subfolder, then it should be on the path.
                       For example: 'Freesurfer/dti_FA.nii.gz'). For T1 just use 'T1'.
  
    Returns:
    subjects_list list): list of subjects that have all the files in the files_list.
    
    """
    subjects = os.listdir(data_dir)
    subjects_list = []
    
    for subject in subjects:
        subject_files = []
        for file in files_list:
            if (file == 'T1'):
                file_path = os.path.join(data_dir, subject, files_names.T1(subject))
            else:
                file_path = os.path.join(data_dir, subject, file)
            if (os.path.isfile(file_path)): subject_files.append(file)
        if (len(subject_files) == len(files_list)):
            subjects_list.append(subject)
    
    return subjects_list
