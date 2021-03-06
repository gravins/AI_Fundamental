`ac3_ac4.py` contains the implementation, with examples, of the algorithms AC3 and AC4
in order to solve CSP.

A **Constraint Satisfation Problem** is composed of:
- finite set of variables,
- finite domain that specify the values that can be assigned to each variable,
- set of constraints that restrict the values that variable can simultaneously take.

The task is to assign a value to each variable satisfying all the constraint. In
general this task is NP hard in the worst cases.

An assignmet is a list of tuple A={(variable<sub>i</sub>, value<sub>i</sub>), (variable<sub>j</sub>, value<sub>j</sub>), ...}
with value<sub>i</sub> in Dom of variable<sub>i</sub>, and it is complete if exist an assignment to
any variable of the problem.

A constraint on a set of variable is a set of possible assignments for those variables,
and can be represented as a pair <scope,rel> where:
- scope is a tuple of variable that partecipating in the constraint,
- rel is a relation that defines all the allowable combination of values for those
variables, taken from their respective domains.

A solution to the problem is a consistent, complete assignment (sotisfies all the
constraints and every the variable is assigned).

A **binary CSP** may be represented as an unidirected graph where nodes corresponds
to variables and edge correspond to binary constraints among variables.

Problem reduction means removing from the constraints those assignments which appears
in no solution. Problem reduction is also called consistency checking/maintenance
since it relies on establishing local consistency properties. Some of those properties
are:
- node consistency
- arc consistency
- path consistency
- etc...


**Arc consistency**

A variable in a CSP is arc-consistent if every value in its domain satisfies the
binary constraints on this variable. Arc consistency doesn’t guarantee a solution.
One of the algorithm for arc consistency is **AC-3**, that mantains a queue of arcs
to consider. Initially all the arcs in the list, AC-3 pops off an arc (x<sub>i</sub>, x<sub>j</sub>)
from the queue and makes x<sub>i</sub> arc consistent with respect to x<sub>j</sub>:
- if the step leaves D<sub>i</sub> unchanged, the algo. Moves on to the next arc-consistency
- if D<sub>i</sub> is made smaller, then we need to add the queue all arcs (x<sub>k</sub>, x<sub>i</sub>)
where x<sub>k</sub> is a neighbor of x<sub>i</sub> diferent from x<sub>j</sub>
- if D<sub>i</sub> becomes empty, then we conclude that the whole CSP has no solution.

When there are no more arcs to consider, we are left with a CSP that is equivalent
to the original CSP, but simpler.
Given a CSP with n variables, each with a domain size at most d, and with c binary
constraints we have a complexity of O(cd<sup>3</sup>) because each arc (x<sub>k</sub>, x<sub>i</sub>) can be
inserted in the queue only d times because x<sub>i</sub> has at most d value to delete, and
checking the consistency of an arc can be done in O(d<sup>2</sup>) time so O(cd<sup>3</sup>) time in
worst case.

**AC4** is an arc consistency algorithm that improves on AC3. AC4 is based on notion
of support, and given a value a for the variable x<sub>i</sub>, we said that a is supported
by x<sub>j</sub> if there is at least one value b in Domain(x<sub>j</sub>) such that x<sub>i</sub> = a and x<sub>j</sub> = b
are compatible. Values that aren’t supported are redundant and can be removed.
AC4 maintain 2 additional data structures:
- counter: for each arc-value pair there is a counter that counts the number of
supports that each variable receives from each binary-constraint involving the
subject variable. Whenever the conunter become 0 that value can be removed from
its domain.
- support set:  for each value of every variable there is a support set that contain
all the variable-value pairs that it supports.

AC4 algorithm consist of two part:
- support sets and counters are constructed and initialized, and redundant values
are removed;
- value removals are processed to update the relevant counters (this may generate
an additional set of redundant values which then have to be removed).
If there is a maximum of d values in the domains, then there are a maximum d<sup>2</sup>
pairs to consider per constraint. If there are a maximum of c constraints in the
problem the first step require O(cd<sup>2</sup>) time. In the second step, the number of
iteration in the while loop don’t exceed the summation of the value in the conunters,
so the complexity of this step is again O(cd<sup>2</sup>) time. Combining the complexity of
step1 and 2 we obtain a complexity of O(cd<sup>2</sup>), lower than AC-3. However, a large
amount of space is required to record the support lists, that is dominated by the
support sets, that causes a complexity in space of O(cd<sup>2</sup>), larger than AC-3.
