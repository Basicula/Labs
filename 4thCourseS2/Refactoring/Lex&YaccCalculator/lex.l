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
rationalNumber  ([1-9][0-9]+|[0-9])?\.[0-9]+ 

%%
[a-z] {
  yylval.sIndex = *yytext - 'a';
  return VARIABLE;
  }

{rationalNumber} {
  yylval.rational_value = strtod(yytext, NULL);
  return RATIONAL;
  }
  
{intNumber}|{digit} {
  yylval.int_value = strtol(yytext, NULL, 10);
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