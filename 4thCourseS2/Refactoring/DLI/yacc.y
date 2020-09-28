%{
#include <iostream>
#include <memory>
#include "utils.h"

void yyerror(char *s);

extern int yylineno;
extern int yylex();
%}

%token INTEGER SYMBOL FUNCTIONVALUE FUNCTION SINGLEFUNCTION
%type<str> INTEGER SYMBOL FUNCTIONVALUE FUNCTION SINGLEFUNCTION
%type<node> ARG
%type<args> ARGS

%%

PROGRAM: 
  PROGRAM EXEC-DLI-OBJECT { std::cout<<"finish\n"; }
  | ;

EXEC-DLI-OBJECT:
  FUNCTIONVALUE                       { std::cout<<"Function value: "<<$1<<std::endl; }
  | FUNCTION "(" ARGS ")"             { std::cout<<"Function: "<<$1<<std::endl; }
  | SINGLEFUNCTION                    { std::cout<<"Single function: "<<$1<<std::endl; }
  ;

ARGS:
  ARG                                 { $$ = std::make_shared<Args>($1); std::cout<<"Arg: "<<$1<<std::endl; }
  | ARG "," ARGS                      { $3->Append($1); $$ = $3; }
  ;
  
ARG:                                  
  INTEGER                             { $$ = std::make_shared<Value>($1); std::cout<<"Integer: "<<$1<<std::endl; }
  | SYMBOL                            { $$ = std::make_shared<Value>($1); std::cout<<"Symbol: "<<$1<<std::endl; }
  ;

%%

void yyerror(char *s) 
  {
  std::cout<< s << ", line " << yylineno << std::endl;
  }
  
int main(void) 
  {
  std::cout<<"main"<<std::endl;
  yyparse();
  return 0;
  }
