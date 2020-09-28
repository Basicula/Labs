all: dli

dli: lex.yy.cpp yacc.tab.cpp
	g++ -D_GLIBCXX_USE_CXX11_ABI=0 -w -o dli lex.yy.cpp yacc.tab.cpp

lex.yy.cpp: lex.l
	flex -o lex.yy.cpp lex.l

yacc.tab.cpp: yacc.y
	bison -o yacc.tab.cpp -d yacc.y

clean:
	rm -rf *.o dli