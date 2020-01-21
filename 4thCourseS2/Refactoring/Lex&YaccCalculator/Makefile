YFLAGS = -d
CXXFLAGS  = -Wall -Werror

calculator: calculator.o lex.o

calculator.o: common.h

lex.o: common.h

.PHONY: clean
clean:
	rm -f *.o calculator y.tab.h

