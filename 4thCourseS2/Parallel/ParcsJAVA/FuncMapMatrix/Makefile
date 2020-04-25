all: run

clean:
	rm -f src/*.class out/Matrix.jar

Matrix.jar: out/parcs.jar src/*.java
	@javac -cp out/parcs.jar src/*.java
	@jar cf out/Matrix.jar -C src .
	@rm -f src/*.class

run: Matrix.jar
	@cd out && java -cp 'parcs.jar:Matrix.jar' Matrix
