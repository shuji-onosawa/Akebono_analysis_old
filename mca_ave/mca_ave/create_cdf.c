/*    
 *    平均したMCAデータを保存するCDFファイルを作成するための各種関数
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cdf.h"
#include "average.h"

//CDFファイルのid
extern CDFid crid;
extern CDFstatus status;

extern char input[ 20 ];

extern float freq[ NUM_CHANNEL ];

extern long f_year;
extern long f_month;
extern long f_day;

//各変数の変数id
long ave_EmxNum;
long ave_EavNum;
long ave_BmxNum;
long ave_BavNum;
long ave_PGapNum;
long ave_EphNum;
long ave_chNum;

//**************************************************************************
//createCDF() : 平均したMCAデータを保存するCDFファイルを作成する関数
void createCDF( ymd )
     char ymd[][ 5 ];
{
  int k;

  char *createfile;
  char *rmfile;

  char name_sec[ 3 ];

  long numDims = 0;
  static long dimSizes[1] = {0};
  long encoding = HOST_ENCODING;
  long majority = ROW_MAJOR;
  long format = SINGLE_FILE;

  createfile = ( char * )calloc( CREATE_LEN , sizeof( char ) );

  //***** 生成するファイル名を作成
  sprintf( createfile , "%s%s/ak_%s%d_mca_%s%s%s_v0%d" , CRNAME , ymd[ 0 ] , RESOLUTION , RESOLUTION_NUM , ymd[ 0 ] , ymd[ 1 ] , ymd[ 2 ] , VERSION); 

  rmfile = ( char * )calloc( CREATE_LEN , sizeof( char ) );
  sprintf( rmfile , "%s.cdf" , createfile );

  remove( rmfile );       /* 既にCDFが存在するならば削除 */

  printf("createfile =  %s\n" , createfile );

  /***** Create CDF *****/
  status = CDFlib( CREATE_ , CDF_ , createfile , numDims , dimSizes , &crid ,
		   PUT_ , CDF_ENCODING_ , encoding , 
		   CDF_MAJORITY_ , majority , 
		   CDF_FORMAT_ , format ,
		   NULL_ );
  
  if ( status != CDF_OK ) StatusHandler( status );
  free( rmfile );
  free( createfile );

  //***** global属性を作る関数を呼ぶ
  global_attr( ymd );

  //***** z変数を作る関数を呼ぶ
  create_zVAR();

  //***** valiable属性を作る関数を呼ぶ
  valiable_attr();

}

//**************************************************************************
//create_zVAR() : 必要なz変数を作る関数
void create_zVAR()
{

  //datatype用変数
  long data_char = CDF_CHAR;
  long data_uint1 = CDF_UINT1;
  long data_uint4 = CDF_UINT4;
  long data_epoch = CDF_EPOCH;
  long data_float = CDF_FLOAT;


  //nochar型は必ず1 ,  char型の変数には1文字しか保存しないので1
  long numElements = 1;

  //次元は1次元
  long numDim1 = 1;
  long numDim0 = 0;

  //次元サイズは 1 か 16
  long dimSize1[] = { 1 };
  long dimSize16[] = { 16 };

  //レコード変化は channel 以外はVARY
  long recVary = VARY;
  long recNoVary = NOVARY;

  //次元変化は全変数 VARY = 次元に沿って変化する
  long dimVarys[] = { VARY };


  //***** 書き込みたいCDFファイルを選ぶ *****
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  //***** 変数 Emax を作成
  status = CDFlib( CREATE_ , zVAR_ , "Emax" , data_uint1 , numElements , numDim1 , dimSize16 , recVary , dimVarys , &ave_EmxNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 変数 Eave を作成
  status = CDFlib( CREATE_ , zVAR_ , "Eave" , data_uint1 , numElements , numDim1 , dimSize16 , recVary , dimVarys , &ave_EavNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 変数 Bmax を作成
  status = CDFlib( CREATE_ , zVAR_ , "Bmax" , data_uint1 , numElements , numDim1 , dimSize16 , recVary , dimVarys , &ave_BmxNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 変数 Bave を作成
  status = CDFlib( CREATE_ , zVAR_ , "Bave" , data_uint1 , numElements , numDim1 , dimSize16 , recVary , dimVarys , &ave_BavNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 変数 PostGap を作成
  status = CDFlib( CREATE_ , zVAR_ , "PostGap" , data_uint4 , numElements , numDim0 , dimSize1 , recVary , dimVarys , &ave_PGapNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );
  
  if ( status != CDF_OK ) StatusHandler( status );
  
  //***** 変数 Epoch を作成
  status = CDFlib( CREATE_ , zVAR_ , "Epoch" , data_epoch , numElements , numDim0 , dimSize1 , recVary , dimVarys , &ave_EphNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 変数 channel を作成
  status = CDFlib( CREATE_ , zVAR_ , "channel" , data_float , numElements , numDim1 , dimSize16 , recNoVary , dimVarys , &ave_chNum ,
		   PUT_ , zVAR_SPARSERECORDS_ , PAD_SPARSERECORDS ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  input_channel();
}
//**************************************************************************
//input_channel() : z変数 channel に値を格納する関数

void input_channel()
{

  int i;
  long indices[ 1 ];
  long record = 0;

  float res[ NUM_CHANNEL ];

  get_channel();

  //生CDFの間違いのための応急処置
  freq[ 0 ]= 3.16;

  //***** 各チャンネルの周波数の値を変数 channel に格納する
  for( i = 0 ; i < 16 ; i ++ ) {
    indices[ 0 ] = ( long )i;
    status = CDFlib( SELECT_ , CDF_             , crid ,
		               zVAR_            , ave_chNum ,
		               zVAR_RECNUMBER_  , record ,
		               zVAR_DIMINDICES_ , indices ,
		     PUT_    , zVAR_DATA_       , &freq[ i ] ,
		     NULL_ );
    
    if ( status != CDF_OK ) StatusHandler( status );
  }


  //***** 各チャンネルの周波数の値を変数 channel から取り出す
  //***** - データチェックのため
  /*
  for( i = 0 ; i < 16 ; i++ ) {
    status = CDFlib( SELECT_ , zVAR_ , ave_chNum ,
		     zVAR_RECNUMBER_ , record ,
		     zVAR_DIMINDICES_ , &indices[ i ] ,
		     GET_ , zVAR_DATA_ , &res[ i ] , 
		     NULL_ );
    
   if ( status != CDF_OK )printf("STATUS=%d\n",status);   
    if ( status != CDF_OK ) StatusHandler( status );
    printf("%d   %f\n",i,res[i]);
  }
  */
}


//**************************************************************************
//input_Epoch() : z変数 Epoch に値を格納する関数

void input_Epoch( time , record )
     double time;
     long record;
{
  //データチェック用変数  
  //  double res;

  long year;
  long month;
  long day;
  long hour;
  long min;
  long sec;
  long msec;
  

  msec = ( long )( time * 1000.0 );
  msec = msec % 1000;
  time = ( long )time;
  hour = ( long )( time / TTL_HOUR );
  time = time - ( hour * TTL_HOUR );
  min = ( long )( time /TTL_MIN );
  time = time - ( min * TTL_MIN );
  sec = ( long )time;

  time = computeEPOCH( f_year , f_month , f_day , hour , min , sec , msec );
  
  //***** 時刻データを変数 Epoch に格納する
  status = CDFlib( SELECT_ , CDF_            , crid ,
		             zVAR_           , ave_EphNum ,
		             zVAR_RECNUMBER_ , record ,
		   PUT_    , zVAR_DATA_      , &time ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 時刻データを変数 Epoch から取り出す
  //***** - データチェックのため
  /*
  status = CDFlib( SELECT_ , zVAR_           , ave_EphNum ,
		             zVAR_RECNUMBER_ , record ,
		   GET_    , zVAR_DATA_      , &res , 
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  EPOCHbreakdown( res , &year , &month , &day , &hour , &min , &sec , &msec );

    printf("%d = %d/%d/%d %d:%d:%d.%d\n" , record , year , month , day , hour , min , sec , msec );
  */
}

//**************************************************************************
//input_Emax() : z変数 Emax に値を格納する関数
void input_Emax( result , record )
     unsigned char result[];
     long record;
{

  int i;
  long recS;
  long recC;
  long recI;
  long indices[1];
  long counts[1];
  long intervals[1];
  unsigned char tmp[ NUM_CHANNEL ];

  unsigned char res[ NUM_CHANNEL ];

  recS = record;
  recC = 1;
  recI = 1;
  indices[0]=0;
  counts[0]=(long)NUM_CHANNEL;
  intervals[0]=1;
 
  for( i = 0 ; i < NUM_CHANNEL ; i ++ ) {
    tmp[ i ] = result[ i ];
  } 
  //***** 電界ピーク値データを変数 Emax に格納する
   status = CDFlib( SELECT_ , CDF_              , crid ,
		   zVAR_             , ave_EmxNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   PUT_    , zVAR_HYPERDATA_   , &tmp , 
		   NULL_ );
  if ( status != CDF_OK ) StatusHandler( status ); 

  //***** 電界ピーク値データを変数 Emax から取り出す
  //***** - データチェックのため
  /*
  for( i = 0 ; i < 16 ; i++ ) {
    indices[ 0 ] = ( long )i;
    status = CDFlib( SELECT_ , zVAR_ , ave_EmxNum ,
		     zVAR_RECNUMBER_ , record ,
		     zVAR_DIMINDICES_ , indices ,
		     GET_ , zVAR_DATA_ , &res[ i ], 
		     NULL_ );

    //printf("STATUS=%d\n",status);   
    if ( status != CDF_OK ) StatusHandler( status );
  }
  printf("\n");
  */
}

//**************************************************************************
//***** - データチェックのため
//read_Emax() : z変数 Emax に値を格納する関数
/*
void read_Emax( record )
     long record;
{

  int i;
  long indices[1];
  long counts[1];
  long intervals[1];

  unsigned char res[ NUM_CHANNEL ];

  indices[0]=0;
  counts[0]=(long)NUM_CHANNEL;
  intervals[0]=1;
 
  //***** 電界ピーク値データを変数 Emax から取り出す
  //***** - データチェックのため
  
  for( i = 0 ; i < 16 ; i++ ) {
    indices[ 0 ] = ( long )i;
    status = CDFlib( SELECT_ , zVAR_ , ave_EmxNum ,
		     zVAR_RECNUMBER_ , record ,
		     zVAR_DIMINDICES_ , indices ,
		     GET_ , zVAR_DATA_ , &res[ i ], 
		     NULL_ );

    printf("STATUS=%d\n",status);   
   }
  printf("\n");
  
}
*/

//**************************************************************************
//input_Eave() : z変数 Eave に値を格納する関数

void input_Eave( result , record )
     unsigned char result[];
     long record;
{
  int i;
  long recS;
  long recC;
  long recI;
  long indices[1];
  long counts[1];
  long intervals[1];
  unsigned char tmp[ NUM_CHANNEL ];

  unsigned char res[ NUM_CHANNEL ];

  recS = record;
  recC = 1;
  recI = 1;
  indices[0]=0;
  counts[0]=(long)NUM_CHANNEL;
  intervals[0]=1;
 
  for( i = 0 ; i < NUM_CHANNEL ; i ++ ) {
    tmp[ i ] = result[ i ];
  } 

  //***** 電界平均値データを変数 Eave に格納する
  status = CDFlib( SELECT_ , CDF_              , crid ,
		   zVAR_             , ave_EavNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   PUT_    , zVAR_HYPERDATA_   , &tmp , 
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status ); 
  
  //***** 電界平均値データを変数 Eave から取り出す
  //***** - データチェックのため
  /*
  for( i = 0 ; i < 16 ; i++ ) {
    indices[ 0 ] = ( long )i;
    status = CDFlib( SELECT_ , zVAR_ , ave_EavNum ,
		     zVAR_RECNUMBER_ , record ,
		     zVAR_DIMINDICES_ , indices ,
		     GET_ , zVAR_DATA_ , &res[ i ], 
		     NULL_ );
    if ( status != CDF_OK )printf("STATUS=%d\n",status);   
 
    printf("%d " ,(int)res[ i ] );  
  }
  printf("\n");  
  */
}

//**************************************************************************
//input_Bmax() : z変数 Bmax に値を格納する関数

void input_Bmax( result , record )
     unsigned char result[];
     long record;
{
  int i;
  long recS;
  long recC;
  long recI;
  long indices[1];
  long counts[1];
  long intervals[1];
  unsigned char tmp[ NUM_CHANNEL ];

  //  unsigned char res[ NUM_CHANNEL ];

  recS = record;
  recC = 1;
  recI = 1;
  indices[0]=0;
  counts[0]=(long)NUM_CHANNEL;
  intervals[0]=1;
 
  for( i = 0 ; i < NUM_CHANNEL ; i ++ ) {
    tmp[ i ] = result[ i ];
  } 

  //***** 磁界ピーク値データを変数 Bmax に格納する
  status = CDFlib( SELECT_ , CDF_              , crid ,
		   zVAR_             , ave_BmxNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   PUT_    , zVAR_HYPERDATA_   , &tmp , 
		   NULL_ );
  if ( status != CDF_OK ) StatusHandler( status ); 

  //***** 磁界ピーク値データを変数 Bmax から取り出す
  //***** - データチェックのため
  /*  
  for( i = 0 ; i < 16 ; i++ ) {
    indices[ 0 ] = ( long )i;
    status = CDFlib( SELECT_ , zVAR_ , ave_BmxNum ,
		     zVAR_RECNUMBER_ , record ,
		     zVAR_DIMINDICES_ , indices ,
		     GET_ , zVAR_DATA_ , &res[ i ], 
		     NULL_ );
    
    if ( status != CDF_OK ) StatusHandler( status );
   if ( status != CDF_OK )printf("STATUS=%d\n",status);   
    printf("%d " ,res[ i ] );
  }
  printf("\n");
  */ 
}


//**************************************************************************
//input_Bave() : z変数 Bave に値を格納する関数

void input_Bave( result , record )
     unsigned char result[];
     long record;
{
  int i;
  long recS;
  long recC;
  long recI;
  long indices[1];
  long counts[1];
  long intervals[1];
  unsigned char tmp[ NUM_CHANNEL ];

  //  unsigned char res[ NUM_CHANNEL ];

  recS = record;
  recC = 1;
  recI = 1;
  indices[0]=0;
  counts[0]=(long)NUM_CHANNEL;
  intervals[0]=1;
 
  for( i = 0 ; i < NUM_CHANNEL ; i ++ ) {
    tmp[ i ] = result[ i ];
  } 

  //***** 磁界平均値データを変数 Bave に格納する
  status = CDFlib( SELECT_ , CDF_              , crid ,
		   zVAR_             , ave_BavNum ,
		   zVAR_RECNUMBER_   , recS ,
		   zVAR_RECCOUNT_    , recC ,
		   zVAR_RECINTERVAL_ , recI ,
		   zVAR_DIMINDICES_  , indices ,
		   zVAR_DIMCOUNTS_   , counts ,
		   zVAR_DIMINTERVALS_, intervals ,
		   PUT_    , zVAR_HYPERDATA_   , &tmp , 
		   NULL_ );
  if ( status != CDF_OK ) StatusHandler( status ); 

  //***** 磁界平均値データを変数 Bave から取り出す
  //***** - データチェックのため
  /* 
  for( i = 0 ; i < 16 ; i++ ) {
    indices[ 0 ] = ( long )i;
    status = CDFlib( SELECT_ , zVAR_ , ave_BavNum ,
		     zVAR_RECNUMBER_ , record ,
		     zVAR_DIMINDICES_ , indices ,
		     GET_ , zVAR_DATA_ , &res[ i ], 
		     NULL_ );
   
    if ( status != CDF_OK ) StatusHandler( status );
    if ( status != CDF_OK )printf("STATUS=%d\n",status);    
    printf("%d " ,res[ i ] );

  }
  printf("\n");
  */ 
}

//**************************************************************************
//input_PostGap() : z変数 PostGap に値を格納する関数
//    = 1  : MCA 観測器 OFF
//    = 2  : ノイジーデータ入り
//    = 16 : BDR(データレコーダー) ON
//    = 32 : SMS(粒子観測器) ON
//    = 64 : bitrate M

void input_PostGap( flag , record )
     int flag;
     long record;
{

    int res;

  //***** ポストギャップフラグデータを変数 PostGap に格納する
  status = CDFlib( SELECT_ , CDF_            , crid ,
		             zVAR_           , ave_PGapNum ,
		             zVAR_RECNUMBER_ , record ,
		   PUT_ , zVAR_DATA_ , &flag ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** ポストギャップフラグデータを変数 PostGap から取り出す
  //***** - データチェックのため
  /*
  status = CDFlib( SELECT_ , zVAR_ , ave_PGapNum ,
		             zVAR_RECNUMBER_ , record ,
			     GET_ , zVAR_DATA_ , &res, 
			     NULL_ );

   if ( status != CDF_OK )printf("STATUS=%d\n",status);   
  if ( status != CDF_OK ) StatusHandler( status );

  printf("%d %d postgap = %d\n",ave_PGapNum,record, res );
  */
}
