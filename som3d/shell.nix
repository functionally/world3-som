with import <nixpkgs> {};

let

  unstable = import <nixos-unstable>{};

  tensorly = python37.pkgs.buildPythonPackage rec {

    pname = "tensorly";
    version = "0.1.6";
    name = "${pname}-${version}";

    src = fetchgit {
      url = "https://github.com/tensorly/tensorly";
      rev = "1bb217a077d6fa1d507f963a60da81adfd099d79";
      sha256 = "0cwlhd44dn1c52zd7czjqlfn8v3d5aapk175a19qmk30pfy3b1i8";
    };
  # src = python37.pkgs.fetchPypi {
  #   inherit pname version;
  #   sha256 = "1z0m08pgxzps9n97g0r0mhnr5lny0g2pkdng45h6nm3m5xi8lg62";
  # };

    propagatedBuildInputs = [
      python37.pkgs.numpy
      python37.pkgs.scipy
    ];

    doCheck = false;

    meta = {
      homepage = "http://tensorly.github.io/";
      description = "TensorLy is a fast and simple Python library for tensor learning. It builds on top of NumPy, SciPy and MXNet and allows for fast and straightforward tensor decomposition, tensor learning and tensor algebra.";
    };
    
  };

in

  (
    python37.withPackages (ps: with ps; [
#     bootstrapped-pip
    # ggplot
#     jupyter
#     Keras
#     matplotlib
    # mxnet
      numpy
      pandas
      scikitlearn
      scipy
#     seaborn
#     statsmodels
#     tensorflow
      tensorly
#     Theano
    ])
  ).env
