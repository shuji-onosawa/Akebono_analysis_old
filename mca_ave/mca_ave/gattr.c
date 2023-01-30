/*
 *    MCA用CDFファイルの n秒平均CDFファイル のglobal Attributeを作るプログラム
 *    - global Attribute は 20個 あります。
 *
 *    By Y. Ozaki     2005.11.04
 *
 *    最終更新日 : 2005.11.04
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "cdf.h"
#include "average.h"
//**************************************************************************
//global_attr() : gloal attribute を作る関数のmain

extern CDFid crid;
extern CDFstatus status;

int global_attr( ymd )
     char ymd[][ 5 ];
{

  char gAttrName[ 30 ];

  char date[ 3 ][ 5 ];
  int i;

  //gエントリーに必要な変数
  long data_char = CDF_CHAR;     // データ型
  long gEntryLen = 0;            // 代入する文字列の文字数
  char gEntryValue[ 150 ] = "";  // 代入する文字列をいれる配列
  char* Rule;                    // Rules_of_use 用代入する文字列をいれる配列
                                 // - 文字数が多いから

  //===== Acknowledgement =========================================

  //***** g属性名をgAttrName[]に代入
  strcpy( gAttrName , "Acknowledgement" );

  //***** gエントリーをgEntryValue[]に代入
  strcpy( gEntryValue , "AKEBONO VLF-MCA data were provided by Akebono VLF team through the data archive system at Kanazawa University in Japan." );

  //***** 代入する文字列の文字数を調べる
  gEntryLen = ( long )strlen( gEntryValue );

  if( gEntryLen > 150 ) printf("over string!!\n");

  //***** g属性を作って、そのgエントリーに値を格納する関数を呼ぶ
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );

  //================================================================

  //===== ADID_ref ==========================================
  strcpy( gAttrName , "ADID_ref" );
  strcpy( gEntryValue , "NSSD0241 " );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Data_type ================================================

  //***** g属性名をgAttrName[]に代入
  strcpy( gAttrName , "Data_type" );

  //***** gエントリーをgEntryValue[]に代入
  sprintf( gEntryValue , "%s%d > High Resolution data" , RESOLUTION_LARGE , RESOLUTION_NUM );

  //***** 代入する文字列の文字数を調べる
  gEntryLen = ( long )strlen( gEntryValue );

  if( gEntryLen > 150 ) printf("over string!!\n");

  //***** g属性を作って、そのgエントリーに値を格納する関数を呼ぶ
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );

  //================================================================

  //===== Data_version =============================================
  strcpy( gAttrName , "Data_version" );

  //***** CDFファイル作成日(今日の日付)を調べる

  sprintf( gEntryValue , "%d" , VERSION ); 

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Descriptor ===============================================
  strcpy( gAttrName , "Descriptor" );
  strcpy( gEntryValue , "MCA > multi channel analyzer" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Discipline ===============================================
  strcpy( gAttrName , "Discipline" );
  strcpy( gEntryValue , "Space Physics > Magnetospheric Science" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 100 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Generated_by =============================================
  strcpy( gAttrName , "Generated_by" );
  strcpy( gEntryValue , "KANAZAWA University" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Generation_date ==========================================
  strcpy( gAttrName , "Generation_date" );

  //***** CDFファイル作成日(今日の日付)を調べる
  get_date( date );

  strcpy( gEntryValue , date[ 0 ]);
  for( i = 1 ; i < 3 ; i ++ ) {
    strcat( gEntryValue , date[ i ] );
  }

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Instrument_type ==========================================
  strcpy( gAttrName , "Instrument_type" );
  strcpy( gEntryValue , "Radio and Plasma Waves(space)" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Logical_file_id ==========================================
  strcpy( gAttrName , "Logical_file_id" );

  sprintf( gEntryValue , "AK_%s%d_MCA_%s%s%s_V0%d" , RESOLUTION_LARGE , RESOLUTION_NUM , ymd[ 0 ] , ymd[ 1 ] , ymd[ 2 ] , VERSION);

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Logical_source ===========================================
  strcpy( gAttrName , "Logical_source" );

  sprintf( gEntryValue , "AK_%s%d_MCA" , RESOLUTION_LARGE , RESOLUTION_NUM );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Logical_source_description ===============================
  strcpy( gAttrName , "Logical_source_description" );
  strcpy( gEntryValue , "Akebono Radio and Plasma Waves High Resolution data" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Mission_group ============================================
  strcpy( gAttrName , "Mission_group" );
  strcpy( gEntryValue , "Akebono" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== MODS =====================================================
  strcpy( gAttrName , "MODS" );
  strcpy( gEntryValue , " " );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== PI_affiliation ===========================================
  strcpy( gAttrName , "PI_affiliation" );
  strcpy( gEntryValue , "KANAZAWA University" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== PI_name ==================================================
  strcpy( gAttrName , "PI_name" );
  strcpy( gEntryValue , "I. Nagano" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Project ==================================================
  strcpy( gAttrName , "Project" );
  strcpy( gEntryValue , " " );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== Rules_of_use =============================================
  strcpy( gAttrName , "Rules_of_use" );

  Rule = ( char * )calloc( 1000 , sizeof( char ) );

  strcpy( Rule , " In order to confirm the reliability of the data, you are requested to contact the VLF PI, Prof. Isamu Nagano before using the VLF-MCA data in oral/poster presentations. In the publishment, you should contact to the VLF PI and contact person before the submission for the confirmation of the principle of authorship/aknowledgement. You are also requested to send reprints to AKEBONO Project Office and the VLF PI:\n" );
  strcat( Rule , "\nAKEBONO Project Office:\n  Prof. Toshifumi Mukai (Project Scientist),\n  Institute of Space and Astronautical Science,\n  3-1-1 Yoshinodai, Sagamihara, Kanagawa 229-8510, Japan\n  E-mail: mukai@stp.isas.jaxa.jp\n  FAX: +81-42-759-8456\n");
  strcat( Rule , "\nVLF PI:\n  Prof. Isamu Nagano,\n  Kanazawa University,\n  Kakuma, Kanazawa 920-1192, Japan\n  E-mail: nagano@is.t.kanazawa-u.ac.jp\n  FAX: +81-76-234-4859\n");
  strcat( Rule , "\nFor further information, please contact with:\n  Dr. Yoshiya Kasahara\n  Kanazawa University,\n  Kakuma, Kanazawa 920-1192, Japan\n  E-mail: kasahara@is.t.kanazawa-u.ac.jp\n  FAX: +81-76-234-4952\n");

  gEntryLen = ( long )strlen( Rule );
  if( gEntryLen > 1000 ) printf("over string!!\n");
  input_gATTR( gAttrName , Rule , gEntryLen , data_char );

  free( Rule );
  //================================================================

  //===== source_name ==============================================
  strcpy( gAttrName , "source_name" );
  strcpy( gEntryValue , "Akebono > Akebono satellite" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== TEXT =====================================================
  strcpy( gAttrName , "TEXT" );

  Rule = ( char * )calloc( 250 , sizeof( char ) );

  sprintf( Rule , "Kimura, I., K. Hashimoto, I. Nagano, T. Okada, M. Yamamoto, T. Yoshino, H. Matsumoto, M. Ejiri, and K. Hayashi,\nVLF observations by the Akebono (EXOS-D) satellite,\nJ. Geomagn. Geoelectr., 42(4), pp.459-478, 1990\n" );

  gEntryLen = ( long )strlen( Rule );
  if( gEntryLen > 250 ) printf("over string!!\n");
  input_gATTR( gAttrName , Rule , gEntryLen , data_char );

  free( Rule );
  //================================================================

  //===== Time_resolution ==========================================
  strcpy( gAttrName , "Time_resolution" );

  sprintf( gEntryValue , "%ss" , ymd[ 3 ] );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== TITLE ====================================================
  strcpy( gAttrName , "TITLE" );
  strcpy( gEntryValue , "Akebono MCA High resolution data" );

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== ST  ==========================================
  strcpy( gAttrName , "Start_time" );

  sprintf( gEntryValue , "%s_%s/%s_0:0:0:0" , ymd[ 0 ] , ymd[ 1 ] , ymd[ 2 ]);

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //================================================================

  //===== ET  ==========================================
  strcpy( gAttrName , "End_time" );

  sprintf( gEntryValue , "%s_%s/%s_23:59:59:999" , ymd[ 0 ] , ymd[ 1 ] , ymd[ 2 ]);

  gEntryLen = ( long )strlen( gEntryValue );
  if( gEntryLen > 150 ) printf("over string!!\n");
  input_gATTR( gAttrName , gEntryValue , gEntryLen , data_char );
  //===============================================================
}


//***************************************************************
//input_gATTR() : g属性を作って、そのgエントリーに値を格納する関数

void input_gATTR( gAttrName , gEntryValue , gEntryLen , dataType )
     char* gAttrName;
     char* gEntryValue;
     long  gEntryLen;
     long dataType;
{
  CDFstatus status;

  //g属性を作るための変数
  long g_scope = GLOBAL_SCOPE;
  long gAttrNum;

  long gEntryNum = 0L;

  char res[ 1000 ];

  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** g属性を作る
  status = CDFlib( CREATE_ , ATTR_ , gAttrName , g_scope , &gAttrNum ,
		   NULL_ );
  
  if ( status != CDF_OK ) StatusHandler( status );


  //***** デフォルトのg属性エントリーを選択し、gエントリー番号を獲得する
  status = CDFlib( SELECT_ , gENTRY_ , gEntryNum ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** g属性を選択して、gエントリーにデータを代入する
  //- GETは必要ないので、最終的に消す!!
  status = CDFlib(  SELECT_ , ATTR_ , gAttrNum ,
		              gENTRY_ , gEntryNum ,
		    PUT_ , gENTRY_DATA_ , dataType , gEntryLen , gEntryValue ,
		    //		    GET_ , gENTRY_DATA_ , res ,
		    NULL_ );

   if ( status != CDF_OK ) StatusHandler( status );

   //   printf("\n%s \n",res);

}

//***************************************************************
//get_date() : 現在の年月日を知る
void get_date( date )
     char date[][ 5 ];
{
  struct tm *lt;
  time_t now;
  int year , month , day;
  
  time( &now );
  lt = localtime(&now);
  year = lt -> tm_year + 1900;
  month = lt -> tm_mon + 1;
  day = lt -> tm_mday;

  //***** year を int型 から char型 に変換する
  sprintf( date[ 0 ] , "%4d" , year );

  //***** month を int型 から char型 に変換する
  date[ 1 ][ 0 ] = ( int )( month / 10 ) + '0';
  date[ 1 ][ 1 ] = ( int )( month % 10 ) + '0';
  date[ 1 ][ 2 ] = '\0';

  //***** day を int型 から char型 に変換する
  date[ 2 ][ 0 ] = ( int )( day / 10 ) + '0';
  date[ 2 ][ 1 ] = ( int )( day % 10 ) + '0';
  date[ 2 ][ 2 ] = '\0';

}
