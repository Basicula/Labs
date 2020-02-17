triangle(S1, S2, S3, T) :-
    valid_triangle( S1, S2, S3) ->
    	(
    	equilateral(S1, S2, S3, T);
    	isosceles(S1, S2, S3, T);
        right_angled(S1, S2, S3, T);
        acute(S1, S2, S3, T);
        obtuse(S1, S2, S3, T)
    	);
    degenerate_triangle(S1, S2, S3, T).

valid_triangle(S1, S2, S3) :-
    S1 > 0, S2 > 0, S3 > 0,
    S1 + S2 > S3,
    S1 + S3 > S2,
    S2 + S3 > S1.

degenerate_triangle(S1, S2, S3, "degenerate") :-
    S1 > 0, S2 > 0, S3 > 0,
    (
    S3 is S1 + S2;
    S2 is S1 + S3;
    S1 is S2 + S3
    ), !.

equilateral(S1, S2, S3, "equilateral") :-
    S1 == S2, 
    S2 == S3.

isosceles(S1, S2, S3, "isosceles") :-
    (
    S1 == S2;
    S1 == S3;
    S2 == S3
    ), !.

pythagoras_theorem(X, Y, Z) :-
    X * X + Y * Y =:= Z * Z.

right_angled(S1, S2, S3, "right-angled") :-
    (   
    pythagoras_theorem(S1, S2, S3);
    pythagoras_theorem(S2, S3, S1);
    pythagoras_theorem(S3, S2, S1)
    ), !.

acute(S1, S2, S3, "acute") :-
    S1 * S1 + S2 * S2 > S3 * S3,
    S2 * S2 + S3 * S3 > S1 * S1,
    S3 * S3 + S1 * S1 > S2 * S2.

obtuse(S1, S2, S3, "obtuse") :-
    (
    S1 * S1 + S2 * S2 < S3 * S3;
    S2 * S2 + S3 * S3 < S1 * S1;
    S3 * S3 + S1 * S1 < S2 * S2
    ), !.

%triangle(3,4,5,X). 		- right-angled
%triangle(3,3,4,X). 		- isosceles
%triangle(3,3,3,X). 		- equilateral
%triangle(3,4,7,X). 		- degenerate
%triangle(0,0,0,X). 		- false
%triangle(9,2,3,X). 		- false
%triangle(1,1.1,1.2, X). 	- acute
%triangle(3, 4, 6, X).		- obtuse