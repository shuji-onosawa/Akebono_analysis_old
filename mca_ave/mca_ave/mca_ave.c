 /*
 *    MCAデータのCDFファイル(0.25秒間隔)をn秒平均する。
 *    そして、それを新しいCDFファイルに保存する。
 *    n 秒 1 レコードにする。
 *
 *    By Y. Ozaki
 *
 *    2005.11.3
 *
 *    - 実行コマンド ave yyyy mm dd n
 *    - Epoch は Spacerecord にしませんでした(描画の都合上)。
 *                                                2005.12.19
 *    - 実効長の求め方間違ってたの修正しました。
 *                                                2006. 1. 6
 *    - 帯域幅で割った値を結果とします。
 *                                                2006. 1.10
 *
 *    hyper access を導入して高速化をはかりました。
 *    variable attributes の不具合を直しました。
 *    global attributes にST ET を追加しました。
 *
 *                         by Masanori Aoki       2007. 1.31
 *
 *    最終更新日 : 2007. 1.31
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "cdf.h"
#include "average.h"
long ave_EmxNum;

CDFid opid;
CDFid crid;
CDFstatus status;

char input[ 20 ];

//各変数の変数id
long EmaxNum;
long EaveNum;
long BmaxNum;
long BaveNum;
long E_WIDANum;
long B_WIDANum;
long PostGapNum;
long EpochNum;
long channelNum;

long f_year;
long f_month;
long f_day;

float freq[ NUM_CHANNEL ];
float bfact[ NUM_CHANNEL ];

int main( int argc , char *argv[] )
{
  clock_t start,end;
  int sec;
  int k;

  int len_ymd[ 4 ];
  char ymd[ 4 ][ 5 ];

  if( argc != MAX_ARGC ) {
    printf("Input ERROR.\n");
    exit(1);
  }

  //***** 入力された年 月 日 の文字列の長さを調べる
  /*
  for( k = 1 ; k < argc ; k++ ) {
    len_ymd[ k - 1 ] = strlen( argv[ k ] );
  } 
  if( len_ymd[ 0 ] != 4 ) {
    printf("Input ERROR of YEAR.\n");
    exit(1);
  }
  if( len_ymd[ 1 ] !=  1 && len_ymd[ 1 ] != 2 ) {
    printf("Input ERROR of MONTH.\n");
    exit(1);
  }
  if( len_ymd[ 2 ] !=  1 && len_ymd[ 2 ] != 2 ) {
    printf("Input ERROR of MONTH.\n");
    exit(1);
  }
  if( len_ymd[ 3 ] !=  1 && len_ymd[ 3 ] != 2 ) {
    printf("Input ERROR of SECONT.\n");
    exit(1);
  }
  */
  
  //***** 入力された年 月 日 と 平均の秒 を 配列ymd[] に保存
  //year
  strcpy( ymd[ 0 ] ,argv[ 1 ] );

  //month & day & sec
  for( k = 1 ; k <= 2 ; k++ ) {
    if( strlen( argv[ k + 1 ] ) == 1 ) {
      ymd[ k ][ 0 ] = '0';
      ymd[ k ][ 1 ] = argv[ k + 1 ][ 0 ];
      ymd[ k ][ 2 ] = '\0';
    }
    else {
      strcpy( ymd[ k ] , argv[ k + 1 ] );
    }
  }

  strcpy( ymd[ 3 ] ,argv[ 4 ] );

  sec = atoi( ymd[ 3 ] );
  /*  if( sec < 1 || sec > 60 ){
    printf("!!!!! input error !!!!!\n");
    exit( 1 );
  }
  */

  start=clock();

  openCDF( ymd );
  get_VarNum();

  f_year = ( long )atoi( ymd[ 0 ] );
  f_month = ( long )atoi( ymd[ 1 ] );
  f_day = ( long )atoi( ymd[ 2 ] );

  createCDF( ymd );

  ave_data( sec );

  closeCDF();

  end =clock();

  printf(" success!! \n");
  printf("time = %f [sec]\n",(double)(end-start)/CLOCKS_PER_SEC);

}


//**************************************************************************
//openCDF() : MCAデータのCDFファイルを開く関数
void openCDF( ymd )
     char ymd[][ 5 ];
{
  char fpname[ OPEN_LEN + 1 ];

  int k;

  //***** オープンするファイル名を作成

  sprintf( fpname , "%s%s/ak_h0_mca_%s%s%s_v01" , OPNAME , ymd[ 0 ] , ymd[ 0 ] , ymd[ 1 ] , ymd[ 2 ] );

  //  sprintf( fpname , "%s%s/%s%s%sMCA_H0" , OPNAME , ymd[ 0 ] , ymd[ 0 ] , ymd[ 1 ] , ymd[ 2 ] );

  //  printf("open = %s\n",fpname);

  status = CDFlib( OPEN_ , CDF_ , fpname , &opid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
}

//**************************************************************************
//closeCDF() : 読んだCDFファイルを閉じる関数
void closeCDF()
{
  status = CDFclose ( opid );

  if (status != CDF_OK) StatusHandler (status);

  status = CDFclose ( crid );

  if (status != CDF_OK) StatusHandler (status);

}

//**************************************************************************
//get_VarNum() : 読んだCDFファイルの変数idをゲットする関数
void get_VarNum()
{
  status = CDFlib( SELECT_ , CDF_ , opid ,
		   GET_ , zVAR_NUMBER_ , "Emax"    , &EmaxNum ,
		          zVAR_NUMBER_ , "Eave"    , &EaveNum ,
		          zVAR_NUMBER_ , "Bmax"    , &BmaxNum ,
		          zVAR_NUMBER_ , "Bave"    , &BaveNum ,
		          zVAR_NUMBER_ , "E_WIDA"  , &E_WIDANum ,
		          zVAR_NUMBER_ , "B_WIDA"  , &B_WIDANum ,
		          zVAR_NUMBER_ , "PostGap" , &PostGapNum ,
		          zVAR_NUMBER_ , "Epoch"   , &EpochNum ,
		          zVAR_NUMBER_ , "channel" , &channelNum ,
		   NULL_ );

  if (status != CDF_OK) StatusHandler (status);
}

//**************************************************************************
//get_Data() : 読んだCDFファイルの CDF_UINT1型変数 の値をゲットする関数
void get_Data( num , record , varNum , data )
     int num;
     long record;
     long varNum;
     unsigned char data[];
{
  int k;
  long recS;
  long recC;
  long recI;
  long indices[1];
  long counts[1];
  long intervals[1];
  unsigned char value[num];
  recS=record;
  recC=1;
  recI=1;
  indices[0]=0;
  counts[0]=(long)num;
  intervals[0]=1;

  status = CDFlib( SELECT_ , CDF_              , opid ,
		   zVAR_             , varNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   GET_    , zVAR_HYPERDATA_   , &value , 
		   NULL_ );
  if ( status != CDF_OK ) StatusHandler( status );
  for(k=0;k<num;k++){
    data[k]=value[k];
  }
  
  
}
//**************************************************************************
//get_EB() : 読んだCDFファイルの 電界,磁界 の値をゲットする関数
void get_EB( num , record , varNum , data )
     int num;
     long record;
     long varNum;
     double data[];
{
  int k;
  long recS;
  long recC;
  long recI;
  long indices[1];
  long counts[1];
  long intervals[1];
  unsigned char value[num];

  recS=record;
  recC=1;
  recI=1;
  indices[0]=0;
  counts[0]=(long)num;
  intervals[0]=1;
  
  status = CDFlib( SELECT_ , CDF_              , opid ,
		   zVAR_             , varNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   GET_    , zVAR_HYPERDATA_   , &value , 
		   NULL_ );
  if ( status != CDF_OK ) StatusHandler( status );
  for( k = 0 ; k < num ; k++ ) {
    data[ k ] = ( double )value[ k ];
  }
}

//**************************************************************************
//get_Epoch() : 読んだCDFファイルのEpoch値をゲットする関数
double get_Epoch( record )
     long record;
{
  double time;

  status = CDFlib( SELECT_ , CDF_            , opid ,
		             zVAR_           , EpochNum ,
		             zVAR_RECNUMBER_ , record ,
		   GET_    , zVAR_DATA_      , &time, 
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  return time;
}

//**************************************************************************
//get_PostGap() : 読んだCDFファイルの PostGap の値をゲットする関数
int get_PostGap( record )
     long record;
{
  int flag;

  status = CDFlib( SELECT_ , CDF_            , opid ,
		             zVAR_           , PostGapNum ,
		             zVAR_RECNUMBER_ , record ,
		   GET_    , zVAR_DATA_      , &flag, 
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  return flag;
}

//**************************************************************************
//get_channel() : 読んだCDFファイルの channel の値をゲットする関数
void get_channel()
{ 
  long record = 0L;
  int k;
  long recS = 0L;
  long recC = 1;
  long recI = 1;
  long indices[ 1 ];
  long counts[ 1 ];
  long intervals[ 1 ];

  //各チャンネルの周波数を取得(変数 channel の値を GET する)
  indices[0]=0;
  counts[0]=NUM_CHANNEL;
  intervals[0]=1;
  status = CDFlib( SELECT_ , CDF_              , opid ,
		   zVAR_             , channelNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   GET_    , zVAR_HYPERDATA_   , &freq , 
		   NULL_ );
  if ( status != CDF_OK ) StatusHandler( status );
  printf("\n");

  for( k = 0 ; k < NUM_CHANNEL ; k++ ) {
    bfact[ k ] = sqrt( freq[ k ] * 0.6 );
  }
}

//**************************************************************************
//get_wida() : 4chごとにかたまっているWIDAを1chずつに分ける関数
void get_wida( wida , ws )
     unsigned char wida[];
     unsigned char ws[];
{
  unsigned char c;
  int i , j;

  for( j = 0 ; j < NUM_WIDA ; j ++ ){
      c = wida[ j ];
    for( i = 0 ; i < NUM_WIDA ; i ++ ){
      ws[ (4 * j) + i ] = c & 0x03;
      c >>= 2;
    }
  }
}

//**************************************************************************
//heffe() : アンテナ実効長を求める関数(電界用)
double heffe( i )
     int i;
{

  double pi;
  double rs = 500.0E3;
  double cs = 250.0e-12;
  double cin = 100.0e-12;
  double preg = -2.2;
  double heff;
  double heffe;

  double omega , denom , real , image;
  /*
    denom : Z の分母
    real  : Z の実部
    image : Z の虚部
   */
  double zabs;    // Z の大きさ
  double jwcs , jwcin;
  double pregain;

  pi = atan( 1.0 ) * 4;
  //  printf(" pi = %lf \n" , pi );

  heff = 60.0 / 2.0;
  pregain = pow( 10.0 , preg / 20.0 );

  omega = 2.0 * pi * freq[ i ];
  jwcs = omega * cs;
  jwcin = omega * cin;

  denom = pow( 1.0 / rs , 2.0 ) + pow( jwcin + jwcs , 2.0 );
  real = ( pow( 1.0 / rs , 2.0 ) + jwcin * jwcs + pow( jwcs , 2.0 ) ) / denom;
  image = ( jwcin / rs ) / denom;

  zabs = sqrt( pow( real , 2.0 ) + pow( image , 2.0 ) );
  heffe = heff * zabs * pregain;

  return( heffe );

}

//**************************************************************************
//heffb() : アンテナ実効長を求める関数(磁界用)
double heffb( i )
     int i;
{

  double length , a;

  //各チャンネルのアンテナ実効長を求める
  if( freq[ i ] <= 164.4 ){
    a = ( log10( ( double )freq[ i ] ) - 1.0 ) * 0.8921 - 1.699;
    length = pow( 10 , a );
  }
  else if( freq[ i ] <= 800.0 ){
    length = 0.243;
  }
  else if( freq[ i ] <= 7407.0 ){
    a = ( log10( ( double )freq[ i ] ) - 3.0 ) * 1.0588 - 0.9208;
    length = pow( 10 , a );
  }
  else if( freq[ i ] <= 10000.0 ){
    length = 1.0;
  }
  else{
    a = ( 4.2504 - log10( ( double )freq[ i ] ) ) * 0.88591 - 0.22185;
    length = pow( 10 , a );
  }

  return( length );

}

//**************************************************************************
//abs_E_dB() : MCAデータの値から絶対値を求める関数(電界用)
void abs_E_dB( E , ws )
     double E[];
     unsigned char ws[];
{
  double dBV;
  int i;
  double abs;
  unsigned char cabs;

  for( i = 0 ; i < NUM_CHANNEL ; i++ ){
    if( E[ i ] == 0 ){
      E[ i ] = 0.0;
    }
    else{
      dBV = 20.0 * log10( E[ i ] ) - 25.0 * (double)ws[ i ] - 48.0 - 20.0;
      abs = pow( 10.0 , dBV / 20.0 ) / heffe( i );
      abs = abs * 1.0e3;
      //帯域幅を考慮
      abs = abs / bfact[ i ];
      E[ i ] = abs * abs;
    } 
  }
}

//**************************************************************************
//abs_B_dB() : MCAデータの値から絶対値を求める関数(磁界用)
void abs_B_dB( B , ws )
     double B[];
     unsigned char ws[];
{
  double dBV;
  int i;
  double abs;
  unsigned char cabs;

  double zzz = 120.0 * 3.141592;

  for( i = 0 ; i < NUM_CHANNEL ; i++ ){
    if( B[ i ] == 0 ){
      B[ i ] = 0;
    }
    else{
      if( i <= 9 ){
	dBV = 20.0 * log10( B[ i ] ) - 25.0 * (double)ws[ i ] - 48.0 - 25.0;
      }
      else{
	dBV = 20.0 * log10( B[ i ] ) - 25.0 * (double)ws[ i ] - 48.0 - 30.0;
      }
      abs = pow( 10.0 , dBV / 20.0 ) / heffb( i ) / zzz;
      abs = abs * 1.26 * 1.0e6;
      //帯域幅を考慮
      abs = abs / bfact[ i ];
      B[ i ] = abs * abs;
    } 
  }
}

//**************************************************************************
//data_total() : n秒間のMCAデータの合計を求める関数
void data_total( total , data )
     double total[];
     double data[];
{
  int i;

  for( i = 0 ; i < NUM_CHANNEL ; i ++ ) {
    total[ i ] += data[ i ];
  }
}

//**************************************************************************
//data_ave() : n秒間のMCAデータの平均を求める関数
void data_ave( total , ave , recsp )
     double total[];
     unsigned char ave[];
     int recsp;
{
  int i;
  double rms;

  for( i = 0 ; i < NUM_CHANNEL ; i ++ ) {
    rms = total[ i ] / ( double )recsp;
    rms = sqrt( rms );
    //    rms = 20.0 * log10( rms ) + 120.0;
    //    ave[ i ] = ( unsigned char )rms;
    ave[ i ] = ( unsigned char )( ( 20.0 * log10( rms ) ) + 120.0 );

  }
}

//**************************************************************************
//ave_data() : MCAデータを平均する関数
void ave_data( sec )
     int sec;
{

  int recsp;
  int half_recsp;
  int i , j , k;
  long m;
  int i_max;
 
  double max[ NUM_CHANNEL ];
  double ave[ NUM_CHANNEL ];
  unsigned char wida[ NUM_WIDA ];

  int rec_vtl = 0;

  unsigned char ws[ NUM_CHANNEL ];

  double Emax_total[ NUM_CHANNEL ];
  double Eave_total[ NUM_CHANNEL ];
  double Bmax_total[ NUM_CHANNEL ];
  double Bave_total[ NUM_CHANNEL ];

  unsigned char Emax_ave[ NUM_CHANNEL ];
  unsigned char Eave_ave[ NUM_CHANNEL ];
  unsigned char Bmax_ave[ NUM_CHANNEL ];
  unsigned char Bave_ave[ NUM_CHANNEL ];

  double time;

  long hour;
  long min;
  long s;
  long msec;

  int flag;
  int MCAflag = 0;
  int VTLflag = 0;      //レコードが VIRTUAL なものが含まれていたか
  int BDRflag = 0;
  int SMSflag = 0;
  int BitMflag = 0;

  int brHb = 0 , brHa = 0;    //仮想なら 1

  recsp = SECSPACE * sec;
  half_recsp = recsp / 2;
  i_max = DAYSPACE - half_recsp;

  /**************************************************************************/
  //  half_recsp = 86400;
  //  i_max = 98400;
 
  for( i =  half_recsp , m = 0 ; i <= i_max ; i += recsp , m ++ ) {

    //***** 変数の初期化 *****
    rec_vtl = 0;

    MCAflag = 0;
    VTLflag = 0;
    BDRflag = 0;
    SMSflag = 0;
    BitMflag = 0;

    for( k = 0 ; k < NUM_CHANNEL ; k++ ) {
      Emax_total[ k ] = 0;
      Eave_total[ k ] = 0;
      Bmax_total[ k ] = 0;
      Bave_total[ k ] = 0;
    }
    //*************************

    //Epoch が何個 Virtual か調べる  
    for( j = ( -1 ) * half_recsp ; j < half_recsp ; j++ ) {
      time = get_Epoch( ( long )( i + j ));
      
      //レコードが2つ以上連続で仮想になっているかを調べる
      if( time == EPOCH_PAD ) {
	rec_vtl ++;
	brHa = 1;
      }
      else{
	brHa = 0;
      }
      if( brHb == 1 && brHa == 1 )
	VTLflag = 2;
      brHb = brHa;
    }

    //Epoch
    time = ( ( ( double )m + 1.0 ) * ( double )sec ) - ( double )sec / 2.0 ;
    input_Epoch( time , m );

    //PostGapを取得 , 判定
    for( j = ( -1 ) * half_recsp ; j < half_recsp ; j++ ) {
      flag = get_PostGap( ( long )( i + j ) );

      if( MCAflag != FLAG_MCA ) MCAflag = flag & 0x01;
      if( BDRflag != FLAG_BDR ) BDRflag = flag & 0x10;
      if( SMSflag != FLAG_SMS ) SMSflag = flag & 0x20;
      if( BitMflag != FLAG_BitM ) BitMflag = flag & 0x40;
      flag = MCAflag + BDRflag + SMSflag + BitMflag;
    }
    //    printf("%d %d\n",m,flag);
    //ビットレートM なのに、レコードが一個でも仮想なら ノイジーフラグ を立てる
    if( BitMflag == FLAG_BitM && rec_vtl != 0 )
      VTLflag = 2;
    
    //PostGap
    flag += VTLflag;
    if((flag & 0x01) == FLAG_MCA) flag=0x01;

    //n 秒間のレコードが全て仮想なら continue
    if( rec_vtl == recsp ) {
      flag=0x01;
      input_PostGap( flag , m );
      //      read_Emax( m );
      continue;
    } 
    else if(flag == FLAG_MCA){
      input_PostGap( flag , m );
      continue;
    }
    else {
      input_PostGap( flag , m );
    }
    for( j = ( -1 ) * half_recsp ; j < half_recsp ; j++ ) {

      //電界について
      //E_WIDAを取得
      get_Data( NUM_WIDA , ( long )( i + j ) , E_WIDANum , wida );
      get_wida( wida , ws );
	
      //E_maxを取得
      get_EB( NUM_CHANNEL , ( long )( i + j ) , EmaxNum , max );
      abs_E_dB( max , ws );
      data_total( Emax_total , max );
      
      //E_aveを取得
      get_EB( NUM_CHANNEL , ( long )( i + j ) , EaveNum , ave );
      abs_E_dB( ave , ws );
      data_total( Eave_total , ave );
      
      //磁界について
      //B_WIDAを取得
      get_Data( NUM_WIDA , ( long )( i + j ) , B_WIDANum , wida );
      get_wida( wida , ws );
      
      //B_maxを取得
      get_EB( NUM_CHANNEL , ( long )( i + j ) , BmaxNum , max );
      abs_B_dB( max , ws );
      data_total( Bmax_total , max );
      
      //B_aveを取得
      get_EB( NUM_CHANNEL , ( long )( i + j ) , BaveNum , ave );
      abs_B_dB( ave , ws );
      data_total( Bave_total , ave );
    }

    data_ave( Emax_total , Emax_ave , recsp );
    data_ave( Eave_total , Eave_ave , recsp );
    data_ave( Bmax_total , Bmax_ave , recsp );
    data_ave( Bave_total , Bave_ave , recsp );
    
    input_Emax( Emax_ave , m );
    input_Eave( Eave_ave , m );
    input_Bmax( Bmax_ave , m );
    input_Bave( Bave_ave , m );
    

    //    if( ( i % 100 < 10 ) )printf("continue...%d\n",i);

  }
}

/******************************************************************************
 * Status handler.
 *
 *    average用仕様になってます!!
 ******************************************************************************/

void StatusHandler (status)
     CDFstatus status;
{
  char message[CDF_ERRTEXT_LEN+1];
  
  if (status < CDF_WARN) {
    printf ("An error has occurred, halting...\n");
    CDFerror (status, message);
    printf ("%s\n", message);
    exit (status);
  }
  else
    if (status < CDF_OK) {
      printf ("Warning, function may not have completed as expected...\n");
      CDFerror (status, message);
      printf ("%s\n", message);
    }
    else
      if (status > CDF_OK) {
	if( status == VIRTUAL ){
	  //	  printf("virtual\n");
	}
	else {
	  printf ("Function completed successfully, but be advised that...\n");
	  CDFerror (status, message);
	  printf ("%s\n", message);
	}
      }       
  return;
}
