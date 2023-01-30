# 実行の仕方
- 分割コンパイルが必要
- Makefile があるので terminal で $make としてみたところ、次のエラーが出た。
    - /usr/bin/ld: create_cdf.o:(.bss+0x0): multiple definition of `ave_EmxNum'; mca_ave.o:(.bss+0x0): first defined here
    - /usr/bin/ld: cannot find -lcdf: No such file or directory
collect2: error: ld returned 1 exit status
    - make: *** [Makefile:7: bnd] Error 1
