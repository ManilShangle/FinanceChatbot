% member function.
member(X, [X|_]).
member(X, [A|T]) :- A \= X, member(X, T).

neg_member(X, []).
neg_member(X, [Y|T]) :- X \= Y, neg_member(X, T).

% merge function.
merge([], A, A).
merge([H|T], B, C) :- member(H, B), merge(T, B, C).
merge([H|T], B, D) :- neg_member(H, B), append(B, [H], C), merge(T, C, D).

next_query(X) :- query(X), not req_s(X).
next_query(X) :- new_query(X).
next_require(Attr, Value) :- require(Attr, Value), not new_not_require(Attr, Value).
next_require(Attr, Value) :- new_require(Attr, Value), Value \= 'any'.
next_not_require(Attr, Value) :- not_require(Attr, Value), not new_require(Attr, Value).
next_not_require(Attr, Value) :- new_not_require(Attr, Value).
next_require('income level', 'low') :- new_require('income level', 'any').
next_require('income level', 'moderate') :- new_require('income level', 'any').
next_require('income level', 'high') :- new_require('income level', 'any').
next_require('risk level', 'low') :- new_require('risk level', 'any').
next_require('risk level', 'moderate') :- new_require('risk level', 'any').
next_require('risk level', 'high') :- new_require('risk level', 'any').
next_not_require('sector', 'none') :- new_require('income level', 'any').
next_not_require('sector', 'energy') :- new_require('income level', 'any').
next_not_require('sector', 'tech') :- new_require('income level', 'any').
next_not_require('sector', 'healthcare') :- new_require('income level', 'any').
next_not_require('sector', 'consumer_goods') :- new_require('income level', 'any').
next_prefer(X) :- prefer(X), not new_not_prefer(X).
next_prefer(X) :- new_prefer(X).
next_not_prefer(X) :- not_prefer(X), not new_prefer(X).
next_not_prefer(X) :- new_not_prefer(X).

next_another_option(X) :- another_option(X), no_new_request.
next_answer_current(X) :- another_option(X), new_query.

change_req(Attr, Value) :- require(Attr, Value), not require(Attr, Value1), new_require(Attr, Value1).
change_req(Attr, Value1) :- new_require(Attr, Value), require(Attr, Value), require(Attr, Value1), not new_require(Attr, Value1).
change_prefer(X) :- prefer(X), not prefer(X1), new_prefer(X1).

all_require('income level') :- require('income level', 'low'), require('income level', 'moderate'), require('income level', 'high').
all_require('risk level'):- require('risk level', 'low'), require('risk level', 'moderate'), require('risk level', 'high').
all_require('sector'):- require('sector', 'none'), require('sector', 'energy'), require('sector', 'tech'), require('sector', 'healthcare'), require('sector', 'consumer_goods').

req_s(Attr) :- new_require(Attr, _).
req_s(Attr) :- new_not_require(Attr, _).

new_query :- findall(query(X), query(X), L1), findall(next_query(X), next_query(X), L2), de_new(L2, Ll2), not same_list(L1, Ll2).

no_new_request :- 
    findall(require(A, V), require(A, V), L1), findall(next_require(A, V), next_require(A, V), L2), de_new(L2, Ll2), same_list(L1, Ll2),
    findall(not_require(A, V), not_require(A, V), L3), findall(next_not_require(A, V), next_not_require(A, V), L4), de_new(L4, Ll4), same_list(L3, Ll4),
    findall(prefer(X), prefer(X), L5), findall(next_prefer(X), next_prefer(X), L6), de_new(L6, Ll6), same_list(L5, Ll6),
    findall(not_prefer(X), not_prefer(X), L7), findall(next_not_prefer(X), next_not_prefer(X), L8), de_new(L8, Ll8), same_list(L7, Ll8).

de_new([], []).
de_new([next_query(X)|R1], [query(X)|R2]) :- de_new(R1, R2).
de_new([next_require(A, V)|R1], [require(A, V)|R2]) :- de_new(R1, R2).
de_new([next_not_require(A, V)|R1], [not_require(A, V)|R2]) :- de_new(R1, R2).
de_new([next_prefer(X)|R1], [prefer(X)|R2]) :- de_new(R1, R2).
de_new([next_not_prefer(X)|R1], [not_prefer(X)|R2]) :- de_new(R1, R2).

same_list(L1, L2) :- merge(L1, L2, L2), merge(L2, L1, L1).

%?- change_req(Attr, Value).