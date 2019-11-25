with import <nixpkgs> {};

let

  unstable = import <nixos-unstable>{};

  tensorly = python35.pkgs.buildPythonPackage rec {

    pname = "tensorly";
    version = "0.1.6";
    name = "${pname}-${version}";

    src = fetchgit {
      url = "https://github.com/tensorly/tensorly";
      rev = "1bb217a077d6fa1d507f963a60da81adfd099d79";
      sha256 = "0cwlhd44dn1c52zd7czjqlfn8v3d5aapk175a19qmk30pfy3b1i8";
    };
  # src = python35.pkgs.fetchPypi {
  #   inherit pname version;
  #   sha256 = "1z0m08pgxzps9n97g0r0mhnr5lny0g2pkdng45h6nm3m5xi8lg62";
  # };

    propagatedBuildInputs = [
      python35.pkgs.numpy
      python35.pkgs.scipy
    ];

    doCheck = false;

    meta = {
      homepage = "http://tensorly.github.io/";
      description = "TensorLy is a fast and simple Python library for tensor learning. It builds on top of NumPy, SciPy and MXNet and allows for fast and straightforward tensor decomposition, tensor learning and tensor algebra.";
    };
    
  };

  mxnet = python35.pkgs.buildPythonPackage rec {

    pname = "mxnet";
    version = "0.11.0";
    name = "${pname}-${version}";

    src = fetchurl {
      name = "${pname}-${version}.tar.gz";
      url = "https://github.com/apache/incubator-mxnet/archive/${version}.tar.gz";
      sha256 = "1h1csgjxvnc9wacqswl77hrx2f1p59hxa94cdrhr9zrf9mxiac1s";
    };
    sourceRoot = "incubator-${name}/python";

    buildInputs = [
      unstable.mxnet
      python35.pkgs.numpy
      python35.pkgs.requests
      python35.pkgs.graphviz
    ];
    libPath = lib.makeLibraryPath [ unstable.mxnet ];
    preBuild = ''
      sed -e '31a\ \ \ \ return "${libPath}/libmxnet.so"' -i mxnet/libinfo.py
    '';

    doCheck = false;

    meta = {
      homepage = "https://mxnet.incubator.apache.org/";
      description = "A flexible and efficient library for deep learning.";
    };

  };

in

  (
    python35.withPackages (ps: with ps; [
      bootstrapped-pip
    # ggplot
      jupyter
      Keras
      matplotlib
    # mxnet
      numpy
      pandas
      scikitlearn
      scipy
      seaborn
      statsmodels
      tensorflow
      tensorly
      Theano
    ])
  ).env
