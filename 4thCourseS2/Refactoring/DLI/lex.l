%{
#include <string>

#define YYSTYPE std::string

#include "yacc.tab.hpp"

void yyerror(char *);
%}

%option yylineno
%option noyywrap

%%

"dlet"                | 
"get next"            | 
"gn"                  | 
"get next in parent"  | 
"gnp"                 |
"get unique"          | 
"gu"                  | 
"insert"              | 
"isrt"                | 
"position"            | 
"pos"                 |           
"replace"             | 
"repl"                | 
"retrieve"            | 
"schedule"            | 
"schd"                |
"terminate"           | 
"term"                | 
"accept"              | 
"checkpoint"          | 
"chkp"                |
"deq"                 |  
"load"                | 
"log"                 | 
"query"               | 
"refresh"             |
"rolb"                | 
"roll"                | 
"rols"                | 
"sets"                |   
"setu"                | 
"statistics"          |
"stat"                | 
"symchkp"             | 
"xrst" {
  yylval = yytext;
  return FUNCTIONVALUE;
}

[0-9] | 
[1-9][0-9]+ {
  yylval = yytext;
  return INTEGER;
}

[a-zA-Z] {
  yylval = yytext;
  return SYMBOL;
}

[ \t\n]+ ; /* ignore whitespace */
. yyerror("Unknown character");
%%