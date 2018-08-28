import os
from os.path import join as jph
import numpy as np
import nibabel as nib

import DummyForMRI as dfm

from icv.icv_estimator import ICV_estimator


# Path manager:
root_dir     = os.path.dirname(os.path.abspath(__file__))
pfo_examples = jph(root_dir, 'data_examples')

pfo_icv_estimation     = ''
pfo_icv_brains         = ''
pfo_icv_segmentations  = ''
pfo_output             = ''

# Subjects parameters:
num_subjects = 7

list_pfi_sj      = [jph(pfo_icv_brains, 'Danny{}_modGT.nii.gz'.format(j + 1)) for j in range(num_subjects)]
list_pfi_sj_segm = [jph(pfo_icv_segmentations, 'Danny{}_segmGT.nii.gz'.format(j + 1)) for j in range(num_subjects)]


# plain decorator for the dataset creation:
def create_data_set_for_tests(test_func):
    def wrap():

        if not os.path.exists(ldg.pfo_multi_atlas):
            print('Generating dummy dataset for testing part 1. May take some minutes.')
            for j in range(1, num_subjects + 1):
                pass

        if not os.path.exists(pfo_icv_segmentations):
            print('Co-registering dummy dataset for testing part 3. May take 1 min.')
            os.system('mkdir -p {}'.format(pfo_icv_segmentations))
            my_icv_estimator = ICV_estimator(list_pfi_sj, pfo_output)
            my_icv_estimator.generate_transformations()


        test_func()

    return wrap


def get_volume(pfi_input_segm):
    im_segm = nib.load(pfi_input_segm)
    return 0.0


# --- TESTING ---


@create_data_set_for_tests
def test_compute_ground_truth_m_and_estimated_m():
    # Ground:
    v_ground = np.zeros(num_subjects, dtype=np.float)
    for j in range(1, num_subjects + 1):
        pfi_segmGT = jph(pfo_icv_segmentations, 'e00{}_segmGT.nii.gz'.format(j))
        df_vols    = get_volume(pfi_segmGT)
        v_ground[j - 1] = np.sum(df_vols['Volume'])
        print('Subject {}, volume: {}'.format(j, v_ground[j - 1]))
    m_ground = np.mean(v_ground)
    print('Average volume {}'.format(m_ground))
    # Estimated:

    icv_estimator = lab.icv(list_pfi_sj, pfo_output)
    icv_estimator.compute_m_from_list_masks(list_pfi_sj_segm, correction_volume_estimate=0)
    print('Average volume estimated with ICV {}'.format(icv_estimator.m))
    # Comparison
    assert cmp(icv_estimator.m, m_ground) == 0

@create_data_set_for_tests
def test_compute_ground_truth_v_and_estimated_v():
    # Ground:
    v_ground = np.zeros(num_subjects, dtype=np.float)
    for j in range(1, num_subjects + 1):
        pfi_segmGT = jph(pfo_icv_segmentations, 'e00{}_segmGT.nii.gz'.format(j))
        df_vols = get_volume(pfi_segmGT)
        v_ground[j - 1] = np.sum(df_vols['Volume'])
        print('Subject {}, volume: {}'.format(j, v_ground[j - 1]))
    # Estimated:
    my_icv_estimator = ICV_estimator(list_pfi_sj, pfo_output)
    my_icv_estimator.compute_S()
    my_icv_estimator.compute_m_from_list_masks(list_pfi_sj_segm, correction_volume_estimate=0)
    v_est = my_icv_estimator.estimate_icv()
    # Comparison
    av = (np.abs(v_ground + v_est) / float(2))
    err = np.abs(v_ground - v_est)
    for e in list(err / av):
        assert e < 1.0  # assert the error in % is below 1%.
