import os
from os.path import join as jph
import numpy as np
import nibabel as nib

from DummyForMRI.building_blocks import headlike_phantom

from icv.icv_estimator import IcvEstimator


# Path manager:
root_dir     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pfo_examples = jph(root_dir, 'data_examples')

pfo_icv_brains         = jph(pfo_examples, 'dummy_brains')
pfo_icv_output         = jph(pfo_examples, 'dummy_icv_output')

# Subjects parameters:
num_subjects = 7

list_pfi_sj      = [jph(pfo_icv_brains, 'Danny{}_mod.nii.gz'.format(k + 1)) for k in range(num_subjects)]
list_pfi_sj_segm = [jph(pfo_icv_brains, 'Danny{}_segm.nii.gz'.format(k + 1)) for k in range(num_subjects)]


# simple decorator for the dataset creation:
def create_data_set_for_tests(test_func):
    def wrap(*args, **kwargs):

        if not os.path.exists(pfo_icv_brains):
            os.system('mkdir -p {}'.format(pfo_icv_brains))
            os.system('mkdir -p {}'.format(pfo_icv_output))
            print('\n\nICV Testing: \nGenerating dummy dataset for testing part 1. May take some minutes.')
            for sj_id, [pfi_sj, pfi_segm] in enumerate(zip(list_pfi_sj, list_pfi_sj_segm)):
                print('\nSubject {}/{}...'.format(sj_id + 1, num_subjects))
                sj, segm = headlike_phantom((71, 71, 71), intensities=(0.9, 0.3, 0.6, 0.8), random_perturbation=.4)
                im_sj   = nib.Nifti1Image(sj, affine=np.eye(4))
                im_segm = nib.Nifti1Image(segm, affine=np.eye(4))
                nib.save(im_sj, pfi_sj)
                nib.save(im_segm, pfi_segm)

        if not os.path.exists(jph(pfo_icv_output, 'warped')):
            print('\n\nICV Testing: \nGenerate the transformations for the complete graph. May take again some minutes')
            my_icv_estimator = IcvEstimator(list_pfi_sj, pfo_icv_output)
            my_icv_estimator.generate_transformations()

        test_func(*args, **kwargs)

    return wrap


def get_volume(pfi_input_segm):
    im_segm = nib.load(pfi_input_segm)
    return np.prod(np.diag(im_segm.affine)) * np.count_nonzero(im_segm.get_data())


# --- TESTING ---


@create_data_set_for_tests
def test_compute_ground_truth_m_and_estimated_m():
    # Ground:
    v_ground = np.zeros(num_subjects, dtype=np.float)
    for j_id, pfi_segm_j in enumerate(list_pfi_sj_segm):
        df_vols    = get_volume(pfi_segm_j)
        v_ground[j_id] = df_vols
        print('Subject {}, volume: {}'.format(j_id + 1, v_ground[j_id]))
    m_ground = np.mean(v_ground)
    print('Average volume {}'.format(m_ground))
    # Estimated:
    my_icv_estimator = IcvEstimator(list_pfi_sj, pfo_icv_output)
    my_icv_estimator.compute_m_from_list_masks(list_pfi_sj_segm, correction_volume_estimate=0)
    print('Average volume estimated with ICV {}'.format(my_icv_estimator.m))
    # Comparison
    np.testing.assert_equal(my_icv_estimator.m, m_ground)


@create_data_set_for_tests
def test_compute_ground_truth_v_and_estimated_v():
    # Ground:
    v_ground = np.zeros(num_subjects, dtype=np.float)
    for j, pfi_segm_j in enumerate(list_pfi_sj_segm):
        df_vols = get_volume(pfi_segm_j)
        v_ground[j] = df_vols
        print('Subject {}, volume: {}'.format(j + 1, v_ground[j]))
    m_average = np.mean(v_ground)
    # Estimated:
    my_icv_estimator = IcvEstimator(list_pfi_sj, pfo_icv_output)
    my_icv_estimator.m = m_average
    my_icv_estimator.compute_S()
    v_est = my_icv_estimator.estimate_icv()
    # Comparison
    av = (np.abs(v_ground + v_est) / float(2))
    err = np.abs(v_ground - v_est)
    for e in list(err / av):
        assert e < 1.5  # assert the error in % is below 1.5%.


@create_data_set_for_tests
def test_compute_ground_truth_v_and_estimated_v_non_full_graph():
    # Ground:
    v_ground = np.zeros(num_subjects, dtype=np.float)
    for j_id, pfi_segm_j in enumerate(list_pfi_sj_segm):
        df_vols = get_volume(pfi_segm_j)
        v_ground[j_id] = df_vols
        print('Subject {}, volume: {}'.format(j_id + 1, v_ground[j_id]))
    m_average = np.mean(v_ground)
    # Estimated:
    my_icv_estimator = IcvEstimator(list_pfi_sj, pfo_icv_output)

    my_icv_estimator.graph_connections = [[i, j] for i in [0, 3, 5] for j in range(i + 1, num_subjects)]
    my_icv_estimator.compute_S()
    my_icv_estimator.m = m_average
    my_icv_estimator.compute_S()
    v_est = my_icv_estimator.estimate_icv()
    # Comparison
    av = (np.abs(v_ground + v_est) / float(2))
    err = np.abs(v_ground - v_est)
    for e in list(err / av):
        assert e < 1.5  # assert the error in % is below 1.5%.


if __name__ == '__main__':
    test_compute_ground_truth_m_and_estimated_m()
    test_compute_ground_truth_v_and_estimated_v()
    test_compute_ground_truth_v_and_estimated_v_non_full_graph()
