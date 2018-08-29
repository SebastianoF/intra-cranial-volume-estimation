# intra-cranial-volume-estimation

<p align="center"> 
<img src="https://github.com/SebastianoF/intra-cranial-volume-estimation/blob/master/logo.jpg" width="550">
</p>


Template free estimation of intra-cranial volume (ICV), for a dataset of MRI images when no template is available.

### Features

+ Written in Python 2.7
+ Based on [nibabel](http://nipy.org/nibabel/), [numpy](http://www.numpy.org/) and [scipy](https://www.scipy.org/).
+ Provided with an example based on the multi-atlas generator [DummyForMRI](https://github.com/SebastianoF/DummyForMRI), version 0.0.2.
+ Tested with [pytest](https://docs.pytest.org/en/latest/) and on the dataset generated with [DummyForMRI](https://github.com/SebastianoF/DummyForMRI).

### How to install (in development mode) 

+ Install [NiftyReg](https://github.com/KCL-BMEIS/niftyreg)
+ Install in development mode in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with:
```
cd <folder where to clone the code>
git clone https://github.com/SebastianoF/intra-cranial-volume-estimation.git
cd intra-cranial-volume-estimation
pip install -e .
```
+ Install python requirements in requirements.txt with
    `pip install -r requirements.txt`

### Documentation

+ The code is based on the paper:

    Iglesias JE, Ferraris S, Modat M, Gsell W, Deprest J, van der Merwe JL, Vercauteren T: [Template-free estimation of intracranial volume: a preterm birth animal model study](http://www.nmr.mgh.harvard.edu/~iglesias/pdf/FIFI_2017_pre.pdf), MICCAI workshop: Fetal and Infant Image Analysis, 2017.

```
@incollection{iglesias2017template,
  title={Template-free estimation of intracranial volume: A preterm birth animal model study},
  author={Iglesias, Juan Eugenio and Ferraris, Sebastiano and Modat, Marc and Gsell, Willy and Deprest, Jan and van der Merwe, Johannes L and Vercauteren, Tom},
  booktitle={Fetal, Infant and Ophthalmic Medical Image Analysis},
  pages={3--13},
  year={2017},
  publisher={Springer}
}
```

+ The code no(ta)tions are intended to be as in the paper.
+ **Note:** results shown in the paper were produced with MATLAB code and libraries. Contact the first author for the original code.

### Tests

For testing and datastet examples generator:
```bash
pytest -s
```

### Licencing and Copyright

+ Copyright (c) 2018, Sebastiano Ferraris, UCL. Intra-cranial-volume estimation is provided as it is and 
it is available as free open-source software under [MIT License](https://github.com/SebastianoF/intra-cranial-volume-estimation/blob/master/LICENCE.txt)
+ Brains in the logo are from the synthetic MRI dataset [BrainWeb](http://brainweb.bic.mni.mcgill.ca/brainweb/) converted to nifti with [BrainWebRawToNifti](https://github.com/SebastianoF/BrainWebRawToNifti).

### Acknowledgements

+ This repository is developed within the [GIFT-surg research project](http://www.gift-surg.ac.uk).
+  Sebastiano Ferraris is supported by the EPSRC-funded UCL Centre for Doctoral Training in Medical Imaging (EP/L016478/1) and Doctoral Training Grant (EP/M506448/1). 
+ Please see the [related publication](http://www.nmr.mgh.harvard.edu/~iglesias/pdf/FIFI_2017_pre.pdf) for the full acknowledgements list.
