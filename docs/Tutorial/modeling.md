# 内置建模功能

当我们迈出进行分子动力学模拟的第一步之前，必须首先对系统进行建模。建模的范围涵盖了分子结构的创建，以及力场参数和系统参数的配置。在这个教程中，我们将专注于体系结构的创建，也就是如何获得一个初始构象。这一步骤对于成功的模拟至关重要，因为它不仅影响了弛豫时间，有时还可能阻碍系统的正常运行。

体系建模的思路可以概括为以下三个关键步骤：规则、模板和优化。规则指的是确定分子如何被排列的方法。模板用于生成多个分子的蓝图。优化阶段依据分子间距等指标来度量体系结构，从而调整以使其更加均匀和自然。例如，生物体系中常用的初始化构象生成工具packmol，它接受PDB格式的分子模板，将模板复制并摆放到指定的区域，然后基于分子间距离进行优化，从而得到合理的初始构象。

举例来说，如果想生成晶体结构，首先需要确定晶格类型和晶格参数，这些规则将成为构建晶体的基础。然后，通过在晶格点上复制和平移摆放分子或原子，可以使用模板生成晶体的初始结构。

在 LAMMPS 中内置了一系列通用的规则和分子模板等功能，可以用来方便地构建常见的初始构象。本教程将按照这个顺序逐一介绍这些关键步骤，理解和应用 LAMMPS 的内置建模工具。

## 规则

LAMMPS中的规则分为几类，如一系列的晶体结构，随即摆放以及基于物理的摆放等等。

让我们从最简单的规则入手，即如何生成一个晶体结构。在这个规则中，我们需要指定一个区域，在这个区域中绘制一个晶格结构，将我们提供的模板复制并摆放到每一个格点上。lammps中，选中一个区域是通过`region`命令实现的：

``` bash
region ID style args keywords args ...
    ID = user-assigned name for the region
    style = delete or block or cone or cylinder or ellipsoid or plane or prism or sphere or union or intersect
    keyword = side or units or move or rotate or open
```

!!! tip RTFM
    更多`region`的用法和参数细节，请参考[手册](https://docs.lammps.org/region.html)

例如，如果我们想选中一个球形区域，命令可以写作`region NAME sphere 0 0 0 4.1`，即以原点为中心，选中一个半径为`4.1`的球形区域。同理，可以选择其他的几何形状，例如圆锥圆柱，并且对这些区域进行旋转。甚至甚至可以通过“交并补”的集合操作更加精细地修剪区域形状。

现在，我们选中了一个区域，其名称为`NAME`。接下来，我们需要在区域内添加格点。lammps内置了多种晶格类型，我们可以通过`lattice`命令进行操作：

``` bash
lattice style scale keyword values ...
    style = none or sc or bcc or fcc or hcp or diamond or sq or sq2 or hex or custom
    scale = scale factor between lattice and simulation box
    keyword = origin or orient or spacing or a1 or a2 or a3 or basis
```

!!! tip RTFM
    更多`lattice`的用法和参数细节，请参考[手册](https://docs.lammps.org/lattice.html)

`lattice fcc 3.52`建立了一个`fcc`晶格。注意，如果此时体系选择的单位为LJ单位，则约化密度为3.52；如果选择其他单位，3.52则是这种单位制下的晶格常数。

基本的建模规则我们已经定义完成。我们首先选中了一个区域，指定以fcc的晶型向其中添加原子，最后需要做的就是将原子摆放到晶格上。由于我们这里仅仅是向晶格上摆放一个原子，因此可以使用`create_atoms 1 region NAME`，其中1是指我们摆放的原子类型总数为1。

以上是使用lammps对体系建模的基本流程，我们可以对其中的某些步骤进行替换。如果我们对晶体不感兴趣，我们可以用其他的规则，如：

* create_atoms提供的一系列方法：
    * single：在某个坐标点新建一个原子
    * mesh：通过(STL)[https://www.adobe.com/creativecloud/file-types/image/vector/stl-file.html#:~:text=The%20name%20STL%20is%20an,a%203D%20model%20or%20object.]文件提供网格
    * random: 将分子在空间中随机摆放
* fix pour 模拟倾倒的方式填充体系
* fix deposit 模拟沉积以固定间隔将分子插入到体系中
* fix gcmc 通过蒙特卡洛的方式插入分子

`create_atoms`提供了将分子随机放入体系的方法。例如，`create_atoms 1 random 100 12345 NULL`将在体系中随机放入100个类型为1的原子，其中`12345`是随机数种子，`NULL`代指在整个体系中随机放置，也可以用`region-ID`指定特定的区域。如果需要将一个具有多个原子和拓扑连接的分子作为模板放入体系，需要用到`molecule`命令和分子模板功能。我们将在下一节中详细介绍。

如果已经完成了对一个模拟盒子的建模，可以使用`replicate`命令对整个盒子进行整体的复制。例如，`replicate 2 2 2`将整个盒子复制8份，即体系中的原子数与体积将增加8倍。需要注意的是，如果你的体系是周期性的，且分子跨过了边界，此时复制的体系会出现断键的问题。一种行之有效的方式是在随机向盒子中摆放分子时，将分子的初始位置限制在盒子的中心区域，在盒子的四周留出足够的空白区域，从而避免分子跨边界。

`create_atoms`甚至支持采用[STL](https://en.wikipedia.org/wiki/STL_(file_format))格式的文件作为输入。在CAD软件中完成对网格的编辑，生成STL文件，然后通过`create_atoms`命令将网格导入到lammps中。这种方法在建模复杂的几何形状时非常有用，例如在模拟微流控芯片时，可以直接将芯片的几何形状导入到lammps中，而不需要手动输入每一个原子的坐标。

在data文件中，我们会在文件头的部分指定原子、键、角的数量以及类型数量，之后lammps会在根据这些数量分配相应的内存。但是，当使用`create_atoms`新建原子时，lammps并不知道我们需要多少内存，更不知道此时模拟盒子的尺寸。因此需要我们通过`create_box`命令实现：，例如`create_box 1 box`将为类型为1的原子建立一个盒子。如果需要在盒子中添加其他类型的原子，

```
create_box N region-ID keyword value ...
    * N = # of atom types to use in this simulation
    * region-ID = ID of region to use as simulation domain
    * zero or more keyword/value pairs may be appended
    * keyword = bond/types or angle/types or dihedral/types or improper/types or extra/bond/per/atom or extra/angle/per/atom or extra/dihedral/per/atom or extra/improper/per/atom or extra/special/per/atom
```

!!! tip RTFM
    更多`create_box`的用法和参数细节，请参考[手册](https://docs.lammps.org/create_box.html)