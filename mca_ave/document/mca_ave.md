# 実行の仕方
- 分割コンパイルが必要
- Makefile があるので terminal で $make としてみたところ、次のエラーが出た。
    - /usr/bin/ld: create_cdf.o:(.bss+0x0): multiple definition of `ave_EmxNum'; mca_ave.o:(.bss+0x0): first defined here
    - /usr/bin/ld: cannot find -lcdf: No such file or directory
        collect2: error: ld returned 1 exit status
    - make: *** [Makefile:7: bnd] Error 1

以下 '/usr/bin/ld: cannot find -lcdf: No such file or directory'を解決するために試行錯誤
## 環境
WSL, VScode

## やったこと
- cdf libarary を[ダウンロード](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html)
- ダウンロードしたファイルを解凍して、中にある README.install に従ってインストール
- インストール先は/usr/localの下  
ここまでやってコンパイルを試してみた。  
gcc file.c -lcdf  
同じエラーが出た。

- ライブラリ本体は .soとか .aとかの拡張子がついてるらしいのでlocate コマンドで探した。
- ここにあるらしい  
/home/onosawa/cdf38_1-dist/src/lib/libcdf.so  
/usr/local/cdf/lib/libcdf.so