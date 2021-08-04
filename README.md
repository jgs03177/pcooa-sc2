Predicting Combat Outcomes and Optimizing Armies in StarCraft II by Deep Learning
---------------------------------------------------------------------------------

Coded with
+ [Python3](https://www.python.org/)
+ [PyTorch](https://pytorch.org/)

### Prerequisite

+ [git](https://git-scm.com/downloads)
+ [anaconda](https://www.anaconda.com/products/individual)

### Instructions

```
git clone https://github.com/jgs03177/pcooa-sc2.git && cd pcooa-sc2
tar -xf data.zip
conda env create -f environment.yml
conda activate pytorch
jupyter notebook main.ipynb
```

From the anaconda console, type the commands above, which:
1. Clone this repository and change the working directory.
1. Unzip `data.zip` which includes a dataset and saved results.
1. Create PyTorch environment using environment.yml.
1. Activate the created PyTorch environment.
1. Run `main.ipynb` from Jupiter.

### Paper

+ [Predicting Combat Outcomes and Optimizing Armies in StarCraft II by Deep Learning](https://authors.elsevier.com/c/1dUHX3PiGTH-G1) 

```
@article{Lee2021,
  doi = {10.1016/j.eswa.2021.115592},
  url = {https://doi.org/10.1016/j.eswa.2021.115592},
  year = {2021},
  month = dec,
  publisher = {Elsevier {BV}},
  volume = {185},
  pages = {115592},
  author = {Donghyeon Lee and Man-Je Kim and Chang Wook Ahn},
  title = {Predicting combat outcomes and optimizing armies in {StarCraft} {II} by deep learning},
  journal = {Expert Systems with Applications}
}
```

### Link

+ [StarCraft II Combat Simulator](https://github.com/jgs03177/sc2combatsim)
