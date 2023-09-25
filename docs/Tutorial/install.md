# 安装LAMMPS

!!! tip
更多细节与选项请参考[手册](https://docs.lammps.org/Build.html)部分。本教程采用的操作系统为Ubuntu22.04 LTS，并且已经安装GPU相关驱动。

本教程中，我们将介绍如何从源码开始编译带有GPU加速的lammps。我们将分别介绍`cmake`与`GUN make`两种编译方式。

## step1: 下载源代码

使用git命令从Github上拉取代码

```
git clone https://github.com/lammps/lammps.git 
```

或者从网站下载源代码

在[官方网站](https://lammps.sandia.gov/download.html)上下载压缩包

## step2: 使用CMake编译LAMMPS

首先需要安装编译lammps所需的依赖。

``` sh
apt install build-essential
apt install cmake   
apt update
apt upgrade
```
这里可以使用[FFTW](https://www.fftw.org/download.html)作为快速傅里叶变换所需的库；如果没有安装，LAMMPS将会使用自带的KISS。CMake将会根据环境变量和路径自动配置。

``` sh
wget https://www.fftw.org/fftw-3.3.10.tar.gz
tar zxvf fftw-3.3.10.tar.gz
cd fftw
./configure
make -j8 && make install
```

安装并行框架[mpich](http://www.mpich.org/)或[OpenMPI](https://www.open-mpi.org/)

``` sh
wget https://www.mpich.org/static/downloads/4.1.2/mpich-4.1.2.tar.gz
tar -zxvf mpich-4.1.2.tar.gz #解压缩
./configure --enable-shared=yes #--enable-shared=yes是必不可少的参数；如果安装到其他路径，注意环境变量的问题。
make
make install
```

CMake支持源外编辑，因此我们可以在任意位置新建一个build文件夹作为编译工作区

``` sh
cd lammps #进入源码根目录
mkdir build
cd build
```

接下来需要选择需要编译的package。lammps预制了一些常用配置文件，位于根目录下的cmake文件夹的presets中，例如：

```
# lammps/cmake/presets/basic.cmake

set(ALL_PACKAGES KSPACE MANYBODY MOLECULE RIGID)

foreach(PKG ${ALL_PACKAGES})
  set(PKG_${PKG} ON CACHE BOOL "" FORCE)
endforeach()

```
`set()`声明了一个名为`ALL_PACKAGE` 的列表，并`foreach`循环中，将`ALL_PACKAGE`的包全部选中。对于不需要额外参数的包，可以直接添加到列表中。配置完成后，通过`-C`指定配置文件位置，如：

``` sh
cmake -C ../cmake/presets/basic.cmake ../cmake 
```
如果使lammps支持gpu加速，需要另行配置。系统需安装[Nvidia驱动]((https://www.nvidia.cn/Download/index.aspx?lang=cn))和[CUDA](https://developer.nvidia.com/cuda-downloads)，确保`nvidia-smi`和`nvcc -V`命令可以运行。

请在`cmake`的时候加上以下参数: 
```
-D PKG_GPU=on      # include GPU package
-D GPU_API=cuda    # value = opencl (default) or cuda
-D GPU_PREC=mixed  # precision setting
                   # value = double or mixed (default) or single
-D GPU_ARCH=value  # hardware choice for GPU_API=cuda
                   # value = sm_XX, see below
                   # default is Cuda-compiler dependent, but typically sm_20
-D CUDPP_OPT=value # optimization setting for GPU_API=cuda
                   # enables CUDA Performance Primitives Optimizations
                   # yes (default) or no
```
GPU的架构与参数可以在[这里](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)找到。例如: 
``` sh
cmake -C ../cmake/presets/basic.cmake -DPKG_GPU=on -DGPU_API=cuda -DGPU_ARCH=sm_61 ../cmake
```
在命令行中，如果需要指定编译某个包，请使用`-D`选项。

!!! tip

调用GPU来做加速，需要加入-sf -pk两个flag `mpirun -np 8 lmp_gpu -sf gpu -pk gpu 1 -in in.file`。`-sf`指在所有支持GPU加速的脚本命令前加上gpu前缀, `-pk gpu N`是GPU的数量

LAMMPS同时提供了通过ctypes到处的底层python接口和名为`pylammps`的高级接口。如果需要启用这个功能，需要编译名为python的包：

``` sh
cmake ../cmake -DPKG_MOLECULE=yes -DLAMMPS_EXCEPTIONS=yes -DBUILD_LIB=yes -DBUILD_SHARED_LIBS=yes ../cmake
make
```

可以通过修改presets下的预置文件来决定哪些包需要安装。更多的参数选择请[查看](https://github.com/lammps/lammps/blob/master/cmake/README.md)。待配置完成后会出现配置结果详情，确认后：
```sh
make 
make install
```
请注意，此时cmake 文件夹下会有一个名为lmp的可执行文件，此文件就是最终编译结果。如果您看这个名字不爽可以自行重命名，以后开始计算所调用命令就以新名称替换。教程以下均使用`lmp`/`lmp_mpi`/`lmp_serial`/`lmp_gpu`代指此文件。


## 使用kokkos加速

::: tip
本节教程定位到[手册](https://lammps.sandia.gov/doc/Packages_details.html#pkg-kokkos)和[安装详情](https://lammps.sandia.gov/doc/Build_extras.html#kokkos)两节。
:::

LAMMPS中很多的style, 都没有专门的cuda加速代码. 这时我们可以使用kokkos库, 将C++代码转化为`OpenMP`或者`CUDA`代码, 在多核系统运行. 在手册中, 所有带有`/kk`前缀的命令都可以通过这个库跑在并行系统上, 只需要在运行时像`CUDA`加上`-sf kk` 这样的参数即可. 

因为kokkos使用了大量的新特性, 因此前提是必须有`C++11`的编译器. 安装kokkos的方法很多, 我们从自动到手动来介绍. 在编译的过程中, 需要选择主机上是否并行和需要选择用来负责计算的设备(offload of calculations to a device). 默认这两个选项都是关闭的. 此外, 指定的硬件的架构必须要和本机匹配. 由于硬件都是向前兼容的, 所以老版本的编译出的文件可以跑在新架构上. 

首先是尽量保证kokkos的GPU架构和LAMMPS的GPU包一致; 如果不一致的话, 在计算开始时的初始化阶段会有一个延迟, 为新硬件编译GPU核心. 如果GPU的大版本不对, 例如5.2和6.0这样, 就会出问题. 简而言之, 好好设置重新编译一遍不费事, 别找麻烦.

为了简化安装, 在`cmake/presets`下有三个预配置文件:`kokkos-serial.cmake`, `kokkos-openmp.cmake`, `kokkos-cuda.cmake`. 可以连用cmake中的`-C`flage来叠加使用配置 
```
cmake -C ../cmake/presets/basic.cmake -C ../cmake/presets/kokkos-cuda.cmake ../cmake
```

编译配置完成后接着编译
```
make -j8
make install
```

This wraps an nvcc, allowing it to be treated as a real C++ compiler with all the usual flags.

## 使用传统的Make安装

使用`makefiles`编译需要和系统搭配的`Makefile.<machine>`文件, 比如说`src/MAKE`里的各种, 其中包含着编译时的选项和特性. `Make`方法是最传统的方法, 但是似乎相对于`CMake`没有优势. 

### 要求
以下的操作都是在GNU make下进行的, 如果不是GNU make的话最好是先安装或者转到`CMake`方法.
* 支持`C++11`的编译器. Linux下通常是GNU的编译器, 一些老的编译器可能需要`-std=c++11`切换到`C++11`模式; 

### 安装

在编译之前, 你需要手动指定需要编译的包, 使用`make yes-<package>`来添加. 其中`<package>`是需要的包名. 你可以用`make package`查看有哪些包需要编译. 

使用以下命令可以执行默认的LAMMPS编译, 在`lammps/src`下生成`lmp_serial`和`lmp_mpi`:

```
cd lammps/src
make <machine> -jN    # 命令格式, -jN指用N个核编译 
make serial           # 编译串行的LAMMPS执行文件
make mpi              # 编译并行的LAMMPS执行文件
make                  # 查看make帮助
```

编译需要很长时间, 因此可以使用`make <machine> -j N`来并行编译. 同时, 安装[ccache](https://ccache.dev/)可以在,例如代码开发重复编译时节省时间.

在第一遍编译完之后, 任何时候重新编辑了LAMMPS代码, 增添或删除文件, 都需要重新编译和重新链接LAMMPS可执行文件到同样的`make <machine>`命令上. `makefile`的追踪只保证那些需要重新编译的文件呗重新编译, 因此如果你改动了`makefile`, 你需要重新编译整个包. 清空环境需要用`make clean-<machine>`. 

::: tip

编译之前, LAMMPS会手机配置信息, 然后编入到应用程序中. 当你第一次编译LAMMPS时, 会编译一个收集各种依赖的工具. 这可以有效地检测到有哪些模块或者源代码需要重新编译.

:::

### 客制化编译和可选的makefiles

`src/MAKE`中有一些形如`Makefile.<machine>`的文件. 使用`make example`以使用`Makefile.example`. 因此, 以上的`make serial`和`make mpi`分别使用了`src/MAKE/Makefile.serial`和`src/MAKE/Makefile.mpi`. 其他的makefile在这些文件夹中: 

```
OPTIONS    # 关于可以用的特殊设置
MACHINES   # 针对特殊的机器
MINE       # 你自己的特殊设定
```
在makefile文件中, 包含了LAMMPS编译需要的参数和信息, 因此如果手动指定某些参数, 需要修改makefile. 

::: tip

本节教程定位到[手册](https://lammps.sandia.gov/doc/Build_settings.html)的 Optional build settings 一节.

:::

例如我需要指定int数据的字节数, 而不是默认的4比特(21字节). 打开需要用的makefile, 例如我将用`make mpi`命令编译, 就打开`Makefile.mpi`, 在31行找到`LMP_INC`关键字, 在其后加上`-DLAMMPS_BIGBIG`, 保存, 回到`src`下使用`make mpi`编译.
