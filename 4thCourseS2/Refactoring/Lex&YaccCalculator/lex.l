%{
#include <stdlib.h>
#include "common.h"
#include "y.tab.h"
void yyerror(char *);
%}

letter          [a-zA-Z]    
digit           [0-9]
digits          {digit}+
intNumber       [1-9]{digits}
rationalNumber  {intNumber}?\.{digits}

%%
[a-z] {
  yylval.sIndex = *yytext - 'a';
  return VARIABLE;
  }

{intNumber}|{digit} {
  yylval.iValue = atoi(yytext);
  return INTEGER;
  }

[-()<>=+*/;{}.] {
  return *yytext;
  }

">=" return GE;
"<=" return LE;
"==" return EQ;
"!=" return NE;
"while" return WHILE;
"if" return IF;
"else" return ELSE;
"print" return PRINT;
[ \t\n]+ ; /* ignore whitespace */
. yyerror("Unknown character");
%%

int yywrap(void) {
 return 1;
} 