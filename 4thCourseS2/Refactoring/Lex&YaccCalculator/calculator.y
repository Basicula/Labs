%{
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include "common.h"

#define BUFFER_SIZE 1024

/* prototypes */
nodeType *id(int i);
nodeType *make_operation(int oper, int nops, ...);
nodeType *make_integer(int value);
nodeType *make_rational(double value);
nodeType *make_boolean(int value);

void int_to_rational(nodeType* target);
void negative(nodeType* target);

nodeType* arithmetic_operation(nodeType* left, nodeType* right, int operation);
nodeType* boolean_operation(nodeType* left, nodeType* right, int operation);

void freeNode(nodeType *p);
nodeType* ex(nodeType *p, int depth);

int yylex(void);
struct yy_buffer_state;
typedef struct yy_buffer_state *YY_BUFFER_STATE;
extern YY_BUFFER_STATE yy_scan_string(const char *);
extern void yy_delete_buffer(YY_BUFFER_STATE);
void yyerror(char *s);
Value* sym; /* symbol table */
%}

%union {
 int int_value; /* integer value */
 double rational_value;
 char sIndex; /* symbol table index */
 nodeType *nPtr; /* node pointer */
};

%token <int_value> INTEGER
%token <rational_value> RATIONAL
%token <sIndex> VARIABLE
%token WHILE IF PRINT
%nonassoc IFX
%nonassoc ELSE
%left GE LE EQ NE '>' '<'
%left '+' '-'
%left '*' '/'
%nonassoc UMINUS
%type <nPtr> stmt expr stmt_list

%%
  
program:
 program function '\n' 
 | ;
 
function:
 function stmt { ex($2,0); freeNode($2); }
 | /* NULL */; 
  
stmt:
  ';'                                { $$ = make_operation(';', 2, NULL, NULL); }
  | expr ';'                           { $$ = $1; }
  | PRINT expr ';'                     { $$ = make_operation(PRINT, 1, $2); }
  | VARIABLE '=' expr ';'              { $$ = make_operation('=', 2, id($1), $3); }
  | WHILE '(' expr ')' stmt            { $$ = make_operation(WHILE, 2, $3, $5); }
  | IF '(' expr ')' stmt %prec IFX     { $$ = make_operation(IF, 2, $3, $5); }
  | IF '(' expr ')' stmt ELSE stmt     { $$ = make_operation(IF, 3, $3, $5, $7); }
  | '{' stmt_list '}'                  { $$ = $2; };
 
stmt_list:
  stmt               { $$ = $1; }
  | stmt_list stmt   { $$ = make_operation(';', 2, $1, $2); };
 
expr:
  RATIONAL                  { $$ = make_rational($1); }
  | INTEGER                   { $$ = make_integer($1); }
  | VARIABLE                  { $$ = id($1); }
  | '-' expr %prec UMINUS     { $$ = make_operation(UMINUS, 1, $2); }
  | expr '+' expr             { $$ = make_operation('+', 2, $1, $3); }
  | expr '-' expr             { $$ = make_operation('-', 2, $1, $3); }
  | expr '*' expr             { $$ = make_operation('*', 2, $1, $3); }
  | expr '/' expr             { $$ = make_operation('/', 2, $1, $3); }
  | expr '<' expr             { $$ = make_operation('<', 2, $1, $3); }
  | expr '>' expr             { $$ = make_operation('>', 2, $1, $3); }
  | expr GE expr              { $$ = make_operation(GE, 2, $1, $3); }
  | expr LE expr              { $$ = make_operation(LE, 2, $1, $3); }
  | expr NE expr              { $$ = make_operation(NE, 2, $1, $3); }
  | expr EQ expr              { $$ = make_operation(EQ, 2, $1, $3); }
  | '(' expr ')'              { $$ = $2; };

%%

#define SIZEOF_NODETYPE ((char *)&p->val - (char *)p)

nodeType *make_rational(double value)
  {
  printf("rational creation\n");
  nodeType *p;
  size_t nodeSize;
  /* allocate node */
  nodeSize = SIZEOF_NODETYPE + sizeof(Value);
  if ((p = malloc(nodeSize)) == NULL)
    yyerror("out of memory");
  /* copy information */
  p->type = typeValue;
  p->val.rational_value = value;
  p->val.type = Rational;
  return p;
  }

nodeType *make_integer(int value) 
  {
  printf("int creation\n");
  nodeType *p;
  size_t nodeSize;
  /* allocate node */
  nodeSize = SIZEOF_NODETYPE + sizeof(Value);
  if ((p = malloc(nodeSize)) == NULL)
    yyerror("out of memory");
  /* copy information */
  p->type = typeValue;
  p->val.int_value = value;
  p->val.type = Integer;
  return p;
  }
  
nodeType *make_boolean(int value) 
  {
  printf("int creation\n");
  nodeType *p;
  size_t nodeSize;
  /* allocate node */
  nodeSize = SIZEOF_NODETYPE + sizeof(Value);
  if ((p = malloc(nodeSize)) == NULL)
    yyerror("out of memory");
  /* copy information */
  p->type = typeValue;
  p->val.boolean_value = value;
  p->val.type = Boolean;
  return p;
  }
  
nodeType *id(int i) 
  {
  nodeType *p;
  size_t nodeSize;
  /* allocate node */
  nodeSize = SIZEOF_NODETYPE + sizeof(Variable);
  if ((p = malloc(nodeSize)) == NULL)
    yyerror("out of memory");
  /* copy information */
  p->type = typeName;
  p->id.i = i;
  return p;
  }

nodeType *make_operation(int oper, int nops, ...) 
  {
  printf("operation creation\n");
  va_list ap;
  nodeType *p;
  size_t nodeSize;
  int i;
  /* allocate node */
  nodeSize = SIZEOF_NODETYPE + sizeof(Operation) +
  (nops - 1) * sizeof(nodeType*);
  if ((p = malloc(nodeSize)) == NULL)
    yyerror("out of memory");
  /* copy information */
  p->type = typeOperator;
  p->opr.oper = oper;
  p->opr.operands_cnt = nops;
  va_start(ap, nops);
  for (i = 0; i < nops; i++)
    p->opr.operands[i] = va_arg(ap, nodeType*);
  va_end(ap);
  return p;
  }
  
void int_to_rational(nodeType* target)
  {
  if (target->type != typeValue || target->val.type != Integer)
    return;
  target->val.type = Rational;
  target->val.rational_value = target->val.int_value;
  target->val.int_value = 0;
  target->val.boolean_value = FALSE;
  }
  
void negative(nodeType* target)
  {
  if (target->type != typeValue)
    return;
  switch (target->val.type)
    {
    case Rational:
      target->val.rational_value *= -1;
    case Integer:
      target->val.int_value *= -1;
    }
  }
  
nodeType* arithmetic_operation(nodeType* left, nodeType* right, int operation)
  {
  printf("arithmetic operation\n");
  if (left->type != typeValue || right->type != typeValue)
    return NULL;
  nodeType* res;
  ValueType res_type;
  if (left->val.type == Rational || right->val.type == Rational)
    {
    res = make_rational(0.0);
    int_to_rational(left);
    int_to_rational(right);
    res_type = Rational;
    }
  else
    {
    res = make_integer(0);
    res_type = Integer;
    }
  switch(operation)
    {
    case '+':
      if (res_type == Rational)
        {
        printf("%f+%f\n",left->val.rational_value, right->val.rational_value);
        res->val.rational_value = left->val.rational_value + right->val.rational_value;
        }
      else
        {
        printf("%d+%d\n",left->val.int_value, right->val.int_value);
        res->val.int_value = left->val.int_value + right->val.int_value;
        }
      return res;
    case '-':                                          
      if (res_type == Rational)
        {
        printf("%f-%f\n",left->val.rational_value, right->val.rational_value);
        res->val.rational_value = left->val.rational_value - right->val.rational_value;
        }
      else
        {
        printf("%d-%d\n",left->val.int_value, right->val.int_value);
        res->val.int_value = left->val.int_value - right->val.int_value;
        }
      return res;
    case '*':
      if (res_type == Rational)
        {
        printf("%f*%f\n",left->val.rational_value, right->val.rational_value);
        res->val.rational_value = left->val.rational_value * right->val.rational_value;
        }
      else
        {
        printf("%d*%d\n",left->val.int_value, right->val.int_value);
        res->val.int_value = left->val.int_value * right->val.int_value;
        }
      return res;
    case '/':
      if (res_type == Rational)
        {
        if (right->val.rational_value == 0)
          yyerror("Divided by zero");
        else 
          {
          printf("%f/%f\n",left->val.rational_value, right->val.rational_value);
          res->val.rational_value = left->val.rational_value / right->val.rational_value;
          }
        }
      else 
        {
        if (right->val.int_value == 0)
          yyerror("Divided by zero");
        else
          {
          printf("%d/%d\n",left->val.int_value, right->val.int_value);
          res->val.int_value = left->val.int_value / right->val.int_value;
          }
        }
      return res;
    }
  return res;
  }
  
nodeType* boolean_operation(nodeType* left, nodeType* right, int operation)
  {
  nodeType* res = make_boolean(FALSE);
  int_to_rational(left);
  int_to_rational(right);
  switch (operation)
    {
    case '<': 
      res->val.boolean_value = left->val.rational_value < right->val.rational_value;
      return res;
    case '>': 
      res->val.boolean_value = left->val.rational_value < right->val.rational_value;
      return res;
    case GE: 
      res->val.boolean_value = left->val.rational_value >= right->val.rational_value;
      return res;
    case LE: 
      res->val.boolean_value = left->val.rational_value <= right->val.rational_value;
      return res;
    case NE: 
      res->val.boolean_value = left->val.rational_value != right->val.rational_value;
      return res;
    case EQ: 
      res->val.boolean_value = left->val.rational_value == right->val.rational_value;
      return res;
    }
  return res;
  }
  
void print_value(nodeType const* value)
  {
  if (value->type != typeValue)
    return;
  switch(value->val.type)
    {
    case Rational:
      printf("%f\n", value->val.rational_value);
      break;
    case Integer:
      printf("%d\n", value->val.int_value);
      break;
    case Boolean:
      if (value->val.boolean_value)
        printf("True");
      else 
        printf("False");
      break;
    }
  }
  
nodeType* ex(nodeType *p, int depth) 
  {
  printf("%d executing\n", depth);
  if (!p) 
    return NULL;
  nodeType* res;
  switch(p->type) 
    {
    case typeValue:
      printf("%d value case\n",depth);
      return p;
    //case typeName: 
      //return sym[p->id.i];
    case typeOperator:
      printf("%d operation case %c\n",depth,p->opr.oper);
      switch(p->opr.oper) 
        {
        case WHILE: 
          res = ex(p->opr.operands[0],depth+1);
          while(res->val.int_value)
            ex(p->opr.operands[1],depth+1); 
          return NULL;
        case IF:
          res = ex(p->opr.operands[0],depth+1);
          if (res->val.int_value)
            ex(p->opr.operands[1],depth+1);
          else if (p->opr.operands_cnt > 2)
            ex(p->opr.operands[2],depth+1);
          return NULL;
        case PRINT: 
          printf("%d print case\n",depth);
          print_value(ex(p->opr.operands[0],depth+1));
          return NULL;
        case ';': 
          ex(p->opr.operands[0],depth+1);
          return ex(p->opr.operands[1],depth+1);
        //case '=':   
          //return sym[p->opr.operands[0]->id.i] = ex(p->opr.operands[1]);
        case UMINUS: 
          res = ex(p->opr.operands[0],depth+1);
          negative(res);
          return res;
        case '+': 
        case '-': 
        case '*': 
        case '/': 
          return arithmetic_operation(ex(p->opr.operands[0],depth+1),ex(p->opr.operands[1],depth+1),p->opr.oper);
        case '<': 
        case '>': 
        case GE: 
        case LE: 
        case NE: 
        case EQ: 
          return boolean_operation(ex(p->opr.operands[0],depth+1), ex(p->opr.operands[1],depth+1), p->opr.oper);
        }
    }
  return NULL;
  } 
  
void freeNode(nodeType *p) 
  {
  int i;
  if (!p) return;
  if (p->type == typeOperator) 
    {
    for (i = 0; i < p->opr.operands_cnt; i++) 
      freeNode(p->opr.operands[i]);
    }
  free (p);
  }
  
void yyerror(char *s) 
  {
  fprintf(stdout, "%s\n", s);
  }
  
int main(void) 
  {
  yyparse();
  return 0;
  } 