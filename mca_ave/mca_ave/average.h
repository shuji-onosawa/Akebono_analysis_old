/*
 *    average 用 ヘッダーファイル
 *    - ave_bndwdth フォルダー に対応しています。
 *
 *    By Y. Ozaki
 *
 *    2006. 1.10
 *
 *    最終更新日 : 2006. 1.10
 */

//***** 関数宣言 *****

//****** MCAave.c で宣言されている関数
// Status handler.
void StatusHandler();

//CDFファイルをオープンする
void openCDF( char ymd[][ 5 ] );

//CDFファイルをクローズする
void closeCDF();

//読んだCDFファイルの変数idをゲットする
void get_VarNum();

//読んだCDFファイルの CDF_UINT1型変数 の値をゲットする関数
void get_Data( int num , long record , long varNum , unsigned char data[] );

//読んだCDFファイルの 電界,磁界 変数の値をゲットする関数
void get_EB( int num , long record , long varNum , double data[] );

//読んだCDFファイルのEpoch値をゲットする関数
double get_Epoch( long record );

//読んだCDFファイルの PostGap の値をゲットする関数
int get_PostGap( long record );

//読んだCDFファイルの channel の値をゲットする関数
void get_channel();

//4chごとにかたまっているWIDAを1chずつに分ける
void get_wida( unsigned char wida[] , unsigned char ws[] );

//アンテナ実効長を求める(電界用)
double heffe( int i );

//アンテナ実効長を求める(磁界)
double heffb( int i );

//MCAデータの値から絶対値を求める(電界用)
void abs_E_dB( double E[] , unsigned char ws[] );

//MCAデータの値から絶対値を求める(磁界用)
void abs_B_dB( double B[] , unsigned char ws[] );

//n秒間のMCAデータの合計を求める
void data_total( double total[] , double data[] );

//n秒間のMCAデータの平均を求める
void data_ave( double total[] , unsigned char ave[] , int recsp );

//MCAデータを平均する
void ave_data( int sec );

//****** create_cdf.c で宣言されている関数
//平均したデータを保存するCDFファイルを作成する
void createCDF( char ymd[][ 5 ] );

//必要なz変数を作る関数
void create_zVAR();

//z変数 Epoch に値を格納する関数
void input_Epoch( double time , long record );

//z変数 channel に値を格納する関数
void input_channel();

//z変数 Emax に値を格納する関数
void input_Emax( unsigned char result[] , long record );

//z変数 Eave に値を格納する関数
void input_Eave( unsigned char result[] , long record );

//z変数 Bmax に値を格納する関数
void input_Bmax( unsigned char result[] , long record );

//z変数 Bave に値を格納する関数
void input_Bave( unsigned char result[] , long record );

//input_PostGap() : z変数 PostGap に値を格納する関数
void input_PostGap( int flag , long record );
  
//z変数 Emax に値をよむ 関数
//void read_Emax( long record );
/*******************************************************************/
//gattr_ave.c で宣言された関数

//gloal attribute を作る関数のmain
int global_attr( char ymd[][ 5 ] );

//g属性を作って、そのgエントリーに値を格納する関数
void input_gATTR( char* gAttrName , char* gEntryValue , long gEntryLen , long data_char);

//現在の年月日を知る
void get_date( char ymd[][ 5 ] );

/*******************************************************************/
//vattr_ave.c で宣言された関数

//valiable attribute を作る関数のmain
int valiable_attr();

//valiable attribute を作る関数
void input_vATTR( char* vAttrName , long* vAttrNum );

//各valiable attributeが必要なz変数に,エントリーを作る関数
void makeAVG_TYPE();
void makeCATDESC();
void makeDEPEND_0();
void makeDEPEND_1();
void makeDICT_KEY();
void makeDISPLAY_TYPE();
void makeFIELDNAM();
void makeFILLVAL();
void makeFORMAT();
void makeLABLAXIS();
void makeMONOTON();
void makeSCALETYP();
void makeUNITS();
void makeVALIDMAX();
void makeVALIDMIN();
void makeVAR_NOTE();
void makeVAR_TYPE();

//CDF_CHAR型のzエントリーをPUTする関数
void input_CHARzENTRY( long varNum , long vAttrNum , long zEntryLen , char* zEntryValue );

//CDF_FLOAT型のzエントリーをPUTする関数
void input_FLOATzENTRY( long varNum , long vAttrNum , long zEntryLen , float* zEntryValue );

//CDF_UINT1型のzエントリーをPUTする関数
void input_UINT1zENTRY( long varNum , long vAttrNum , long zEntryLen , unsigned char* zEntryValue );

//CDF_UINT4型のzエントリーをPUTする関数
void input_UINT4zENTRY( long varNum , long vAttrNum , long zEntryLen , int* zEntryValue );

//CDF_EPOCH型のzエントリーをPUTする関数
void input_EPOCHzENTRY( long varNum , long vAttrNum , long zEntryLen , double* zEntryValue );




//***** 定数宣言 *****
#define OPNAME "/remote/raid2/MCADB/CDF-H0/"

#define CRNAME "/remote/raid2/MCADB/CDF-H1/"

#define RESOLUTION       "h"
#define RESOLUTION_LARGE "H"
#define RESOLUTION_NUM    1 
#define VERSION           2

/* open cdf file name length */
// ex : /remote/raid1/usr/y-ozaki/CDFdata/1989/ak_h0_mca_19890311_v01
#define OPEN_LEN    63

/* create cdf file name length */
// ex : /remote/raid1/usr/y-ozaki/CDFdata/ave/1989/ak_h8_mca_19890311_v01.cdf
#define CREATE_LEN    72

//最初にコマンド入力されるべき定数の数
#define MAX_ARGC 5

//1日 = 0.25 間隔が 345600 個
#define DAYSPACE    345600

//1秒 = 0.25 間隔が 4 個
#define SECSPACE    4

//チャンネル数
#define NUM_CHANNEL 16

//WIDA のチャンネル数
#define NUM_WIDA    4

//status = 1001 はrecordに入ってる値がvirtual
#define VIRTUAL     1001

//Epoch の PAD値 は double型で 0 です。
#define EPOCH_PAD   0

//PostGapフラグ の立ち方
#define FLAG_MCA    1
#define FLAG_VTL    2
#define FLAG_BDR    16
#define FLAG_SMS    32
#define FLAG_BitM   64

#define         TTL_HOUR        3600
#define         TTL_MIN         60

