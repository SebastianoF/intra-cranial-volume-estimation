import os
import numpy as np
from os.path import join as jph

from icv.icv_estimator import IcvEstimator
from icv.test_icv_basics import get_volume


if __name__ == '__main__':

    # --- PATH MANAGER ----

    subjects_list = ['04', '05', '06', '18', '20', '38', '41', '42', '43', '44', '45', '46', '47']
    num_subjects = len(subjects_list)

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    pfo_root_study    = jph(root_dir, 'data_examples', 'brain_web')
    list_pfi_sj       = [jph(pfo_root_study, 'BW{}_T1W.nii.gz'.format(sj)) for sj in subjects_list]
    list_pfi_sj_segm  = [jph(pfo_root_study, 'BW{}_MASK.nii.gz'.format(sj)) for sj in subjects_list]

    # --- PARAMETERS CONTROLLER ----

    use_mask_brains          = True
    generate_transformations = False
    complete_graph           = True

    if use_mask_brains:
        list_pfi_reg_mask = list_pfi_sj_segm  # use the brain tissue as input mask
        pfo_icv_output    = jph(root_dir, 'data_examples', 'brain_web_output_mask')
    else:
        list_pfi_reg_mask = None
        pfo_icv_output    = jph(root_dir, 'data_examples', 'brain_web_output_no_mask')

    # --- RUN ----

    if not os.path.exists(pfo_icv_output):
        print('This example uses the 20 subjects downloaded for the brainweb dataset.')
        print('Please download the raw data from BrainWeb website and convert them to nifti format.')
        print('then binarise the segmentations to obtain a ground truth of the ICV.')

    else:
        print('\nCompute the ground truth ICV from the segmentation of a set of synthetic data generated with BrainWeb.')

        v_ground = np.zeros(num_subjects, dtype=np.float)

        for j, pfi_segm_j in enumerate(list_pfi_sj_segm):
            df_vols = get_volume(pfi_segm_j)
            v_ground[j] = df_vols
            print('Subject {}, volume: {}'.format(j + 1, v_ground[j]))

        m_average = np.mean(v_ground)
        m_std     = np.std(v_ground)

        print('Mean and standard deviation computed from the ground truth: {}, {}'.format(m_average, m_std))
        print('\n\nCompute the ICV using the icv estimator, initialised with an average ICV from literature')

        brain_average_icv_from_literature = 2000333.76  # modulate this hyperparameters to check robustness.

        print('Mean ICV from literature for a newborn rabbit in mm^3 is {}'.format(brain_average_icv_from_literature))
        print('Difference in percentage between Mean ICV from literature and ground mean ICV for this dataset is '
              ' {} %'.format(100 * np.abs(brain_average_icv_from_literature - m_average) / ((brain_average_icv_from_literature + m_average) / 2)))
        print('(Run multiple times to check for robustness to the initialised mean)')

        my_icv_estimator = IcvEstimator(list_pfi_sj, pfo_icv_output, list_pfi_registration_masks=list_pfi_reg_mask)

        if complete_graph:
            my_icv_estimator.graph_connections = [[i, j] for i in range(num_subjects) for j in range(i + 1, num_subjects)]
        else:
            # All the node are connected to the first one, and no more connections!
            my_icv_estimator.graph_connections = [[i, j] for i in [0] for j in range(i + 1, num_subjects)]

        my_icv_estimator.m = brain_average_icv_from_literature

        if generate_transformations:
            my_icv_estimator.generate_transformations()

        my_icv_estimator.compute_S()

        print
        print my_icv_estimator.S
        print

        v_est = my_icv_estimator.estimate_icv()
        # Comparison
        av = (np.abs(v_ground + v_est) / float(2))
        err = np.abs(v_ground - v_est)
        relative_error = err / av

        print('\n\n Subject :  Ground     Estimated        Average          Abs_diff         Relative_error ')
        for j in range(num_subjects):
            print('      {0}  :  {1:<10} {2:<16} {3:<16} {4:<16} {5:<16}'.format(
                j+1, v_ground[j], v_est[j],  av[j],  err[j], relative_error[j]))

        print('\n Average relative error {}'.format(np.mean(relative_error)))

        import matplotlib.pyplot as plt

        plt.plot(v_ground, v_est, '.')
        plt.plot(v_ground, v_ground, 'r')

        plt.xlabel('Ground')
        plt.ylabel('Estimated')
        plt.title('All nodes connected to only one')
        plt.tight_layout()

        plt.show()
