import os
import numpy as np

from icv.icv_estimator import IcvEstimator
from icv.test_icv_basics import get_volume
from icv.test_icv_basics import num_subjects, list_pfi_sj, list_pfi_sj_segm, pfo_icv_output


if __name__ == '__main__':

    # --- RUN ----

    if not os.path.exists(pfo_icv_output):
        print('This example uses the same dataset employed for the test obtained with continuous integration.')
        print('Please run the icv.test_icv_basics first, or run pytest or nosetests in the repository.')

    else:
        print('\nCompute the ground truth ICV from the segmentation of a set of Dannies.')
        print('(See data_examples folder to see a Danny)\n')

        v_ground = np.zeros(num_subjects, dtype=np.float)

        for j, pfi_segm_j in enumerate(list_pfi_sj_segm):
            df_vols = get_volume(pfi_segm_j)
            v_ground[j] = df_vols
            print('Subject {}, volume: {}'.format(j + 1, v_ground[j]))

        m_average = np.mean(v_ground)
        m_std     = np.std(v_ground)

        print('Mean and standard deviation computed from the ground truth: {}, {}'.format(m_average, m_std))
        print('\n\nCompute the ICV using the icv estimator, initialised with an average ICV from literature')

        danny_average_icv = m_average + m_std  * np.random.randn()

        print('Mean ICV from literature for a Danny is {}'.format(danny_average_icv))
        print('Difference in percentage between Mean ICV from literature and ground mean ICV for this dataset is '
              ' {} %'.format(100 * np.abs(danny_average_icv - m_average) / ((danny_average_icv + m_average)/2)))
        print('(Run multiple times to check for robustness to the initialised mean)')

        my_icv_estimator = IcvEstimator(list_pfi_sj, pfo_icv_output)

        my_icv_estimator.graph_connections = [[i, j] for i in range(num_subjects) for j in range(i + 1, num_subjects)]

        my_icv_estimator.m = danny_average_icv
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

        # import matplotlib.pyplot as plt
        #
        # plt.plot(v_ground, v_est, '.')
        # plt.plot(v_ground, v_ground, 'r')
        #
        # plt.xlabel('Ground')
        # plt.ylabel('Estimated')
        #
        # plt.show()
