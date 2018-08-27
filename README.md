# Intra-cranial-volume estimation

Estimation of intra-cranial volume, given a dataset of MRI images.

### Features

+ Written in Python 2.7
+ Tested with pytest 
+ Provided with an example based on the upcoming library DummyForMRI, a dummy multi-atlas generator.

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

The code is based on the paper:

Iglesias JE, Ferraris S, Modat M, Gsell W, Deprest J, van der Merwe JL, Vercauteren T: [Template-free estimation of intracranial volume: a preterm birth animal model study](http://www.nmr.mgh.harvard.edu/~iglesias/pdf/FIFI_2017_pre.pdf), MICCAI workshop: Fetal and Infant Image Analysis, 2017.

Please see the paper as code documentation and nomenclature.
(Note: paper results were not produced with this code.)

### Licencing and Copyright

Copyright (c) 2018, Sebastiano Ferraris, UCL. Intra-cranial-volume estimation is provided as it is and 
it is available as free open-source software under [MIT License](https://github.com/SebastianoF/intra-cranial-volume-estimation/blob/master/LICENCE.txt)

### Acknowledgements

+ This repository is developed within the [GIFT-surg research project](http://www.gift-surg.ac.uk).
+  Sebastiano Ferraris is supported by the EPSRC-funded UCL Centre for Doctoral Training in Medical Imaging (EP/L016478/1) and Doctoral Training Grant (EP/M506448/1). 
+ Please see the related publication for further fundings.
