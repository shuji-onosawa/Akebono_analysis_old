/*
 *    MCA用CDFファイルの n秒平均CDFファイル用 valiable Attributeを作るプログラム
 *    - valiable Attribute は 16種類 あります。
 *
 *    By Y. Ozaki     2005.12.14
 *
 *    最終更新日 : 2005.12.14
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "cdf.h"
#include "average.h"

//**************************************************************************
//valiable_attr() : valiable attribute を作る関数のmain

extern CDFid crid;
extern CDFstatus status;

//各変数の変数id
extern long ave_EmxNum;
extern long ave_EavNum;
extern long ave_BmxNum;
extern long ave_BavNum;
extern long ave_PGapNum;
extern long ave_EphNum;
extern long ave_chNum;

int valiable_attr()
{

  //===== CATDESC ==================================================
  makeAVG_TYPE();

  //===== CATDESC ==================================================
  makeCATDESC();

  //===== DEPEND_0 =================================================
  makeDEPEND_0();

  //===== DEPEND_1 =================================================
  makeDEPEND_1();

  //===== DICT_KEY =================================================
  makeDICT_KEY();

  //===== DISPLAY_TYPE =============================================
  makeDISPLAY_TYPE();

  //===== FIELDNAM =================================================
  makeFIELDNAM();

  //===== FILLVAL ==================================================
  makeFILLVAL();

  //===== FORMAT ===================================================
  makeFORMAT();

  //===== LABLAXIS =================================================
  makeLABLAXIS();

  //===== MONOTON ==================================================
  makeMONOTON();

  //===== SCALETYP =================================================
  makeSCALETYP();

  //===== UNITS ====================================================
  makeUNITS();

  //===== VALIDMAX =================================================
  makeVALIDMAX();

  //===== VALIDMIN =================================================
  makeVALIDMIN();

  //===== VAR_NOTE =================================================
  makeVAR_NOTE();

  //===== VAR_TYPE =================================================
  makeVAR_TYPE();
   
}

//**************************************************************************
//makeAVG_TYPE() : AVG_TYPE属性を作り、必要なz変数にエントリーを作る関数

void makeAVG_TYPE()
{

  long Avg_typeNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "AVG_TYPE" , &Avg_typeNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "log" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "log" );

  input_CHARzENTRY( ave_EmxNum , Avg_typeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "log" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "log" );

  input_CHARzENTRY( ave_EavNum , Avg_typeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "log" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "log" );

  input_CHARzENTRY( ave_BmxNum , Avg_typeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "log" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "log" );

  input_CHARzENTRY( ave_BavNum , Avg_typeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}
//**************************************************************************
//makeCATDESC() : CATDESC属性を作り、必要なz変数にエントリーを作る関数

void makeCATDESC()
{

  long CatdescNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "CATDESC" , &CatdescNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "Electric field maximum intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Electric field maximum intensity" );

  input_CHARzENTRY( ave_EmxNum , CatdescNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "Electric field average intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Electric field average intensity" );

  input_CHARzENTRY( ave_EavNum , CatdescNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "Magnetic field maximum intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Magnetic field maximum intensity" );

  input_CHARzENTRY( ave_BmxNum , CatdescNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "Magnetic field average intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Magnetic field average intensity" );

  input_CHARzENTRY( ave_BavNum , CatdescNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "Time recorded in the original raw data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Time recorded in the original raw data" );

  input_CHARzENTRY( ave_EphNum , CatdescNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "Frequency" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Frequency" );

  input_CHARzENTRY( ave_chNum , CatdescNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "Post Gap Quality Flag" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Post Gap Quality Flag" );

  input_CHARzENTRY( ave_PGapNum , CatdescNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeDEPEND_0() : DEPEND_0属性を作り、必要なz変数にエントリーを作る関数

void makeDEPEND_0()
{

  long DEPEND0Num;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "DEPEND_0" , &DEPEND0Num );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Epoch" );

  input_CHARzENTRY( ave_EmxNum , DEPEND0Num , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Epoch" );

  input_CHARzENTRY( ave_EavNum , DEPEND0Num , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Epoch" );

  input_CHARzENTRY( ave_BmxNum , DEPEND0Num , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Epoch" );

  input_CHARzENTRY( ave_BavNum , DEPEND0Num , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Epoch" );

  input_CHARzENTRY( ave_PGapNum , DEPEND0Num , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================
}


//**************************************************************************
//makeDEPEND_1() : DEPEND_1属性を作り、必要なz変数にエントリーを作る関数

void makeDEPEND_1()
{

  long DEPEND1Num;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "DEPEND_1" , &DEPEND1Num );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "channel" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "channel" );

  input_CHARzENTRY( ave_EmxNum , DEPEND1Num , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "channel" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "channel" );

  input_CHARzENTRY( ave_EavNum , DEPEND1Num , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "channel" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "channel" );

  input_CHARzENTRY( ave_BmxNum , DEPEND1Num , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "channel" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "channel" );

  input_CHARzENTRY( ave_BavNum , DEPEND1Num , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeDICT_KEY() : DICT_KEY属性を作り、必要なz変数にエントリーを作る関数

void makeDICT_KEY()
{

  long DictkeyNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "DICT_KEY" , &DictkeyNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "ELECTRIC_FIELD > antenna" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "ELECTRIC_FIELD > antenna" );

  input_CHARzENTRY( ave_EmxNum , DictkeyNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "ELECTRIC_FIELD > antenna" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "ELECTRIC_FIELD > antenna" );

  input_CHARzENTRY( ave_EavNum , DictkeyNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "MAGNETIC_FIELD > antenna" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "MAGNETIC_FIELD > antenna" );

  input_CHARzENTRY( ave_BmxNum , DictkeyNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "MAGNETIC_FIELD > antenna" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "MAGNETIC_FIELD > antenna" );

  input_CHARzENTRY( ave_BavNum , DictkeyNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "time > Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "time > Epoch" );

  input_CHARzENTRY( ave_EphNum , DictkeyNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "FREQUENCY > channel" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "FREQUENCY > channel" );

  input_CHARzENTRY( ave_chNum , DictkeyNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "FLAG > post_gap" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "FLAG > post_gap" );

  input_CHARzENTRY( ave_PGapNum , DictkeyNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeDISPLAY_TYPE() : DISPLAY_TYPE属性を作り、必要なz変数にエントリーを作る関数
void makeDISPLAY_TYPE()
{

  long DisplaytypeNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "DISPLAY_TYPE" , &DisplaytypeNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "time_series" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "time_series" );

  input_CHARzENTRY( ave_EmxNum ,  DisplaytypeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "time_series" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "time_series" );

  input_CHARzENTRY( ave_EavNum , DisplaytypeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "time_series" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "time_series" );

  input_CHARzENTRY( ave_BmxNum , DisplaytypeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "time_series" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "time_series" );

  input_CHARzENTRY( ave_BavNum , DisplaytypeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "time_series" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "time_series" );

  input_CHARzENTRY( ave_PGapNum , DisplaytypeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeFIELDNAM() : FIELDNAM属性を作り、必要なz変数にエントリーを作る関数

void makeFIELDNAM()
{

  long FieldnamNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "FIELDNAM" , &FieldnamNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "electric field maximum intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "electric field maximum intensity" );

  input_CHARzENTRY( ave_EmxNum , FieldnamNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "electric field average intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "electric field average intensity" );

  input_CHARzENTRY( ave_EavNum , FieldnamNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "magnetic field maximum intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "magnetic field maximum intensity" );

  input_CHARzENTRY( ave_BmxNum , FieldnamNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "magnetic field average intensity" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "magnetic field average intensity" );

  input_CHARzENTRY( ave_BavNum , FieldnamNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "Time since 0 AD" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Time since 0 AD" );

  input_CHARzENTRY( ave_EphNum , FieldnamNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "channel" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "channel" );

  input_CHARzENTRY( ave_chNum ,FieldnamNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "Post Gap Quality Flag" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Post Gap Quality Flag" );

  input_CHARzENTRY( ave_PGapNum ,FieldnamNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeFILLVAL() : FILLVAL属性を作り、必要なz変数にエントリーを作る関数

void makeFILLVAL()
{

  long FillvalNum;

  //zエントリーに必要な変数
  long zEntryLen = 1;            // 代入する文字列の文字数

  unsigned char zEntryValue[ 1 ];            // 代入する文字列をいれる配列
  double EpochValue[ 1 ];
  float channelValue[ 1 ];
  int PostgapValue[ 1 ];

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "FILLVAL" , &FillvalNum );

  //===== Emax =====================================================
  zEntryLen = 1;
  zEntryValue[ 0 ] = ( unsigned char )255;

  input_UINT1zENTRY( ave_EmxNum , FillvalNum , zEntryLen , zEntryValue );  
  //================================================================

  //===== Eave =====================================================
  //  zEntryLen = 1;
  //  zEntryValue[ 0 ] = ( unsigned char )255;

  input_UINT1zENTRY( ave_EavNum , FillvalNum , zEntryLen , zEntryValue );  
  //================================================================

  //===== Bmax =====================================================
  //  zEntryLen = 1;
  //  zEntryValue[ 0 ] = ( unsigned char )255;

  input_UINT1zENTRY( ave_BmxNum , FillvalNum , zEntryLen , zEntryValue );  
  //================================================================

  //===== Bave =====================================================
  //  zEntryLen = 1;
  //  zEntryValue[ 0 ] = ( unsigned char )255;

  input_UINT1zENTRY( ave_BavNum , FillvalNum , zEntryLen , zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = 1;

  EpochValue[ 0 ] = 0.0;

  input_EPOCHzENTRY( ave_EphNum , FillvalNum , zEntryLen , EpochValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = 1;
  channelValue[ 0 ] = -1.0e15;

  input_FLOATzENTRY( ave_chNum , FillvalNum , zEntryLen , channelValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = 1;
  PostgapValue[ 0 ] = 0;

  input_UINT4zENTRY( ave_PGapNum , FillvalNum , zEntryLen , PostgapValue );
  //================================================================
}

//**************************************************************************
//makeFORMAT() : FORMAT属性を作り、必要なz変数にエントリーを作る関数

void makeFORMAT()
{

  long FormatNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "FORMAT" , &FormatNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "%3d" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "%3d" );

  input_CHARzENTRY( ave_EmxNum , FormatNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "%3d" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "%3d" );

  input_CHARzENTRY( ave_EavNum , FormatNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "%3d" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "%3d" );

  input_CHARzENTRY( ave_BmxNum , FormatNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "%3d" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "%3d" );

  input_CHARzENTRY( ave_BavNum , FormatNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "%5.2f" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "%5.2f" );

  input_CHARzENTRY( ave_chNum , FormatNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "%3d" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "%3d" );

  input_CHARzENTRY( ave_PGapNum , FormatNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeLABLAXIS() : LABLAXIS属性を作り、必要なz変数にエントリーを作る関数

void makeLABLAXIS()
{

  long LablaxisNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "LABLAXIS" , &LablaxisNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "E field" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "E field" );

  input_CHARzENTRY( ave_EmxNum , LablaxisNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "E field" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "E field" );

  input_CHARzENTRY( ave_EavNum , LablaxisNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "B field" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "B field" );

  input_CHARzENTRY( ave_BmxNum , LablaxisNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "B field" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "B field" );

  input_CHARzENTRY( ave_BavNum , LablaxisNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "Epoch" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Epoch" );

  input_CHARzENTRY( ave_EphNum , LablaxisNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "frequency" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "frequency" );

  input_CHARzENTRY( ave_chNum , LablaxisNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "PostGap" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "PostGap" );

  input_CHARzENTRY( ave_PGapNum , LablaxisNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================
}

//**************************************************************************
//makeMONOTON() : MONOTON属性を作り、必要なz変数にエントリーを作る関数

void makeMONOTON()
{

  long MonotonNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "MONOTON" , &MonotonNum );

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "INCREASE" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "INCREASE" );

  input_CHARzENTRY( ave_EphNum , MonotonNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "INCREASE" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "INCREASE" );

  input_CHARzENTRY( ave_chNum , MonotonNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeSCALETYP() : SCALETYP属性を作り、必要なz変数にエントリーを作る関数

void makeSCALETYP()
{

  long ScaletypNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "SCALETYP" , &ScaletypNum );

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "linear" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "linear" );

  input_CHARzENTRY( ave_EphNum , ScaletypNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "log" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "log" );

  input_CHARzENTRY( ave_chNum , ScaletypNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}


//**************************************************************************
//makeUNITS() : UNITS属性を作り、必要なz変数にエントリーを作る関数

void makeUNITS()
{

  long UnitsNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "UNITS" , &UnitsNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "dB" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_EmxNum , UnitsNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "dB" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_EavNum , UnitsNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "dB" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_BmxNum , UnitsNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "dB" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_BavNum , UnitsNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "s" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "s" );

  input_CHARzENTRY( ave_EphNum , UnitsNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "Hz" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "Hz" );

  input_CHARzENTRY( ave_chNum , UnitsNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

}

//**************************************************************************
//makeVALIDMAX() : VALIDMAX属性を作り、必要なz変数にエントリーを作る関数

void makeVALIDMAX()
{

  long ValidmaxNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  unsigned char max255[ 1 ];
  double EpochValue[ 1 ];
  float channelValue[ 1 ];
  int PostgapValue[ 1 ];


  //***** v属性を作る関数を呼ぶ
  input_vATTR( "VALIDMAX" , &ValidmaxNum );

  //===== Emax =====================================================
  zEntryLen = 1L;
  max255[ 0 ] = ( char )255;

  input_UINT1zENTRY( ave_EmxNum , ValidmaxNum , zEntryLen , max255 );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = 1L;
  max255[ 0 ] = ( char )255;

  input_UINT1zENTRY( ave_EavNum , ValidmaxNum , zEntryLen , max255 );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = 1L;
  max255[ 0 ] = ( char )255;

  input_UINT1zENTRY( ave_BmxNum , ValidmaxNum , zEntryLen , max255 );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = 1L;
  max255[ 0 ] = ( char )255;

  input_UINT1zENTRY( ave_BavNum , ValidmaxNum , zEntryLen , max255 );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = 1;

  EpochValue[ 0 ] = computeEPOCH( 2015L , 12L , 31L , 23L , 59L , 59L , 999L );

  input_EPOCHzENTRY( ave_EphNum , ValidmaxNum , zEntryLen , EpochValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = 1;
  channelValue[ 0 ] = 17800.0;

  input_FLOATzENTRY( ave_chNum , ValidmaxNum , zEntryLen , channelValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = 1;
  PostgapValue[ 0 ] = 243;

  input_UINT4zENTRY( ave_PGapNum , ValidmaxNum , zEntryLen , PostgapValue );
  //================================================================

}

//**************************************************************************
//makeVALIDMIN() : VALIDMIN属性を作り、必要なz変数にエントリーを作る関数

void makeVALIDMIN()
{

  long ValidminNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  unsigned char min0[ 1 ];
  double EpochValue[ 1 ];
  float channelValue[ 1 ];
  int PostgapValue[ 1 ];


  //***** v属性を作る関数を呼ぶ
  input_vATTR( "VALIDMIN" , &ValidminNum );

  //===== Emax =====================================================
  zEntryLen = 1L;
  min0[ 0 ] = ( char )0;

  input_UINT1zENTRY( ave_EmxNum , ValidminNum , zEntryLen , min0 );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = 1L;
  min0[ 0 ] = ( char )0;

  input_UINT1zENTRY( ave_EavNum , ValidminNum , zEntryLen , min0 );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = 1L;
  min0[ 0 ] = ( char )0;

  input_UINT1zENTRY( ave_BmxNum , ValidminNum , zEntryLen , min0 );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = 1L;
  min0[ 0 ] = ( char )0;

  input_UINT1zENTRY( ave_BavNum , ValidminNum , zEntryLen , min0 );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = 1;

  EpochValue[ 0 ] = computeEPOCH( 1989L , 1L , 1L , 0L , 0L , 0L , 0L );

  input_EPOCHzENTRY( ave_EphNum , ValidminNum , zEntryLen , EpochValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = 1;
  channelValue[ 0 ] = 3.16;

  input_FLOATzENTRY( ave_chNum , ValidminNum , zEntryLen , channelValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = 1;
  PostgapValue[ 0 ] = 0;

  input_UINT4zENTRY( ave_PGapNum , ValidminNum , zEntryLen , PostgapValue );
  //================================================================
}

//**************************************************************************
//makeVAR_NOTE() : VAR_NOTE属性を作り、必要なz変数にエントリーを作る関数

void makeVAR_NOTE()
{

  long VarnoteNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "VAR_NOTE" , &VarnoteNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "dB" );

  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );

  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_EmxNum , VarnoteNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "dB" );

  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );

  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_EavNum , VarnoteNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "dB" );

  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );

  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_BmxNum , VarnoteNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "dB" );

  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );

  strcpy( zEntryValue , "dB" );

  input_CHARzENTRY( ave_BavNum , VarnoteNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "The Quality flag of MCA data.\n 0  : normal\n 1  : MCA off\n 2  : data is noisy\n 16  : BDR on\n 32  : SMS on\n 64  : Bitrate of date is 'M'\n 128 : PWS on\n" );

  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );

  strcpy( zEntryValue , "The Quality flag of MCA data.\n 0  : normal\n 1  : MCA off\n 2  : data is noisy\n 16  : BDR on\n 32  : SMS on\n 64  : Bitrate of date is 'M'\n 128 : PWS on\n" );

  input_CHARzENTRY( ave_PGapNum , VarnoteNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================
}

//**************************************************************************
//makeVAR_TYPE() : VAR_TYPE属性を作り、必要なz変数にエントリーを作る関数

void makeVAR_TYPE()
{

  long VartypeNum;

  //zエントリーに必要な変数
  long zEntryLen = 0;            // 代入する文字列の文字数
  char* zEntryValue;             // 代入する文字列をいれる配列

  //***** v属性を作る関数を呼ぶ
  input_vATTR( "VAR_TYPE" , &VartypeNum );

  //===== Emax =====================================================
  zEntryLen = ( long )strlen( "data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "data" );

  input_CHARzENTRY( ave_EmxNum , VartypeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Eave =====================================================
  zEntryLen = ( long )strlen( "data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "data" );

  input_CHARzENTRY( ave_EavNum , VartypeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bmax =====================================================
  zEntryLen = ( long )strlen( "data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "data" );

  input_CHARzENTRY( ave_BmxNum , VartypeNum , zEntryLen , zEntryValue );  
  free( zEntryValue );
  //================================================================

  //===== Bave =====================================================
  zEntryLen = ( long )strlen( "data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "data" );

  input_CHARzENTRY( ave_BavNum , VartypeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== Epoch ====================================================
  zEntryLen = ( long )strlen( "support_data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "support_data" );

  input_CHARzENTRY( ave_EphNum , VartypeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== channel ==================================================
  zEntryLen = ( long )strlen( "support_data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "support_data" );

  input_CHARzENTRY( ave_chNum , VartypeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================

  //===== PostGap ==================================================
  zEntryLen = ( long )strlen( "data" );
  zEntryValue = ( char * )calloc( zEntryLen + 1 , sizeof( char ) );
  strcpy( zEntryValue , "data" );

  input_CHARzENTRY( ave_PGapNum , VartypeNum , zEntryLen , zEntryValue );
  free( zEntryValue );
  //================================================================
}

//***************************************************************
//input_vATTR() : v属性を作る関数

void input_vATTR( vAttrName , vAttrNum )
     char* vAttrName;
     long* vAttrNum;
{

  //v属性を作るための変数
  long v_scope = VARIABLE_SCOPE;

  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** g属性を作る
  status = CDFlib( CREATE_ , ATTR_ , vAttrName , v_scope , vAttrNum ,
		   NULL_ );
  
  if ( status != CDF_OK ) StatusHandler( status );

}

//***************************************************************
//input_CHARzENTRY() : CHAR型のzエントリーを格納する関数

void input_CHARzENTRY( zEntryNum , vAttrNum , zEntryLen , zEntryValue )
     long  zEntryNum;
     long  vAttrNum;
     long  zEntryLen;               // 代入する文字列の文字数
     char* zEntryValue;             // 代入する文字列をいれる配列
{

  char res[ 1000 ];
  
  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 書き込みたいz変数,v属性を選択して、zエントリーにデータを代入する
  status = CDFlib(  SELECT_ , ATTR_ , vAttrNum ,
                              zENTRY_ , zEntryNum ,
                    PUT_ , zENTRY_DATA_ , CDF_CHAR , zEntryLen , zEntryValue ,
		    //                    GET_ , zENTRY_DATA_ , res ,
                    NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  //  printf("%s \n",res);

}

//***************************************************************
//input_FLOATzENTRY() : FLOAT型のzエントリーを格納する関数

void input_FLOATzENTRY( zEntryNum , vAttrNum , zEntryLen , zEntryValue )
     long  zEntryNum;
     long  vAttrNum;
     long  zEntryLen;               // 代入する文字列の文字数
     float* zEntryValue;             // 代入する文字列をいれる配列
{

  float res[ 1 ];
  
  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 書き込みたいz変数,v属性を選択して、zエントリーにデータを代入する
  status = CDFlib(  SELECT_ , ATTR_ , vAttrNum ,
                              zENTRY_ , zEntryNum ,
                    PUT_ , zENTRY_DATA_ , CDF_FLOAT , zEntryLen , zEntryValue ,
		    //                    GET_ , zENTRY_DATA_ , res ,
                    NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  //  printf("%f \n",res[ 0 ] );

}

//***************************************************************
//input_UINT1zENTRY() : UINT1型のzエントリーを格納する関数

void input_UINT1zENTRY( zEntryNum , vAttrNum , zEntryLen , zEntryValue )
     long  zEntryNum;
     long  vAttrNum;
     long  zEntryLen;               // 代入する文字列の文字数
     unsigned char* zEntryValue;             // 代入する文字列をいれる配列
{

  unsigned char res[ 1 ];
  
  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 書き込みたいz変数,v属性を選択して、zエントリーにデータを代入する
  status = CDFlib(  SELECT_ , ATTR_ , vAttrNum ,
                              zENTRY_ , zEntryNum ,
                    PUT_ , zENTRY_DATA_ , CDF_UINT1 , zEntryLen , zEntryValue ,
		    //                    GET_ , zENTRY_DATA_ , res ,
                    NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  //  printf("%d \n",res[ 0 ] );

}

//***************************************************************
//input_UINT4zENTRY() : UINT4型のzエントリーを格納する関数

void input_UINT4zENTRY( zEntryNum , vAttrNum , zEntryLen , zEntryValue )
     long  zEntryNum;
     long  vAttrNum;
     long  zEntryLen;               // 代入する文字列の文字数
     int*  zEntryValue;             // 代入する文字列をいれる配列
{

  int res[ 1 ];
  
  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 書き込みたいz変数,v属性を選択して、zエントリーにデータを代入する
  status = CDFlib(  SELECT_ , ATTR_ , vAttrNum ,
                              zENTRY_ , zEntryNum ,
                    PUT_ , zENTRY_DATA_ , CDF_UINT4 , zEntryLen , zEntryValue ,
		    //                    GET_ , zENTRY_DATA_ , res ,
                    NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );
  
  //  printf("%d \n",res[ 0 ] );

}

//***************************************************************
//input_EPOCHzENTRY() : EPOCH型のzエントリーを格納する関数

void input_EPOCHzENTRY( zEntryNum , vAttrNum , zEntryLen , zEntryValue )
     long  zEntryNum;
     long  vAttrNum;
     long  zEntryLen;               // 代入する文字列の文字数
     double* zEntryValue;             // 代入する文字列をいれる配列
{

  double res;

  long year;
  long month;
  long day;
  long hour;
  long min;
  long sec;
  long msec;
  
  
  //***** 書き込みたいCDFファイルを選択
  status = CDFlib( SELECT_ , CDF_ , crid ,
		   NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //***** 書き込みたいz変数,v属性を選択して、zエントリーにデータを代入する
  status = CDFlib(  SELECT_ , ATTR_ , vAttrNum ,
                              zENTRY_ , zEntryNum ,
                    PUT_ , zENTRY_DATA_ , CDF_EPOCH , zEntryLen , zEntryValue ,
		    //                    GET_ , zENTRY_DATA_ , &res ,
                    NULL_ );

  if ( status != CDF_OK ) StatusHandler( status );

  //  EPOCHbreakdown( res , &year , &month , &day , &hour , &min , &sec , &msec );

  //  printf("%d/%d/%d %d:%d:%d.%d\n" , year , month , day , hour , min , sec , msec );

}

