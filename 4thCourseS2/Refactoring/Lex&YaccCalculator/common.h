#define BOOL int
#define FALSE 0
#define TRUE 1

typedef enum 
  { 
  typeValue, 
  typeName, 
  typeOperator 
  } nodeEnum;

typedef enum
  {
  Integer,
  Rational,
  Boolean
  } ValueType;

typedef struct 
  {
  int int_value;
  double rational_value;
  BOOL boolean_value;
  ValueType type;
  } Value;
  
/* identifiers */
typedef struct 
  {
  int i; /* subscript to sym array */
  char* name;
  } Variable;
  
/* operators */
typedef struct 
  {
  int oper; /* operator */
  int operands_cnt; /* number of operands */
  struct nodeTypeTag *operands[1]; /* operands (expandable) */
  } Operation;
  
typedef struct nodeTypeTag 
  {
  nodeEnum type; /* type of node */
  /* union must be last entry in nodeType */
  /* because operNodeType may dynamically increase */
  union 
    {
    Value val; /* constants */
    Variable id; /* identifiers */
    Operation opr; /* operators */
    };
  } nodeType;
  
extern Value* sym; 