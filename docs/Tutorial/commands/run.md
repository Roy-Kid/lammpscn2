# run

> run或许是lammps中最简单的命令之一，所有的分子动力学模拟都将从这一命令开始。`run N`难道是唯一的用法吗？

```bash
run N keyword values
    N = # of timesteps
    upto value = none
    start value = N1
    N1 = timestep at which 1st run started
    stop value = N2
    N2 = timestep at which last run will end
    pre value = no or yes
    post value = no or yes
    every values = M c1 c2 ...
    M = break the run into M-timestep segments and invoke one or more commands between each segment
    c1,c2,...,cN = one or more LAMMPS commands, each enclosed in quotes
    c1 = NULL means no command will be invoked
```

`upto`设置了模拟步数的上限。例如当前一共运行了n步，而命令设置为`run N upto`，则实际将会运行`N-n`步。这条命令在继续运行模拟的时候特别有用。例如，大多数的超算中心都有任务运行时间限制，超出时间则强制把任务终止。重启任务的脚本读取`.restart`文件之后，就不必手动计算剩下需要跑多少步长，从而可以使用相同的脚本多次运行。

`start`和`stop`命令可以将多个`run`视为一组。考虑如下的例子：
```
fix  1  all nvt 200 300 1.0
run  1000 start 0 step 10000
run  1000 start 0 step 10000
...
run  1000 start 0 step 10000
```
如果仅仅运行`run 1000`，则每一次`run`都会从200升温到300。而如果使用`start`和`stop`命令，从0到10000步的模拟将会被视为一组，只会从200升温到300一次。

!!! 重新计算的参数
    * 倒空间参数：由于倒空间参数在运行中不会改变，多次运行可以重新计算参数，以防止出现`cannot compute PPPM`的错误

`pre`和`post`用于简化运行前后所输出设置。连续多次执行`run`命令时可以大大增加log文件的可读性。例如，当LAMMPS被作为MD引擎被其他库调用。默认情况下（`pre` & `post` = yes），每次运行之前会创建邻近表、计算力并施加修复约束；每次运行后，会收集并打印计时统计数据。如果一次运行只是前一次运行的延续（即没有修改参数），则不需要初始计算； 旧的邻近表仍然有效，力也是如此。如果 `pre` 指定为`no`，则跳过初始设置，但打印热力学信息。即便在执行的第一次运行中将`pre`设置为`no`，也会强制完成初始设置计算。如果 `post` 指定为`no`，则跳过完整的时间统计部分，仅打印一行摘要。

`every`可以将`run`命令分为多个较短的运行阶段，两个阶段之间可以执行一个或多个简单的命令（`if`等复杂命令不被支持）。如：

```
variable q equal x[100]
run 6000 every 2000 "print 'Coord = $q'"
```
等价于
```
variable q equal x[100]
run 2000
print "Coord = $q"
run 2000
print "Coord = $q"
run 2000
print "Coord = $q"
```
如果需要执行多个命令，则可以使用换行符`&`将其连接起来：
```
run 100000 every 1000 &
  "print 'Minimum value = $a'" &
  "print 'Maximum value = $b'" &
  "print 'Temp = $c'" &
  "print 'Press = $d'"
```
`run N every n NULL`表示为如果没有命令需要执行。

由于`every`具有可变个数的参数，因此当有多个关键词时，`every`必须是最后一个。与此类似的命令还有`fix halt`。


