sum2:
params 2
param int a`2
param int b`2



~t0 = a`2 + b`2

return ~t0
#L6:
return 0

fun1:
params 4
param int n`3
param int a`3
param int b`3
param int c`3



#L14:
param n`3
param a`3
~t2 = call sum2, 2



#L16:
param b`3
param c`3
~t3 = call sum2, 2

#L12:
param ~t2
param ~t3
~t1 = call sum2, 2

return ~t1
#L10:
return 0

pp:
params 3
param char c1`4
param char c2`4
param char c3`4

output char, c1`4

#L24:
output char, c2`4

#L22:
output char, c3`4

#L20:
return 

start:
params 0

char cc`5[3]
cc`5[0] = 'a'
cc`5[1] = 'b'
cc`5[2] = 'c'

#L29:
~t4 = 0

~t5 = ~t4 * 1

~t6 = ~t5 * 1
~t7 = cc`5[~t6]

~t8 = 1

~t9 = ~t8 * 1

~t10 = ~t9 * 1
~t11 = cc`5[~t10]

~t12 = 2

~t13 = ~t12 * 1

~t14 = ~t13 * 1
~t15 = cc`5[~t14]

#L33:
#L31:
param ~t7
param ~t11
param ~t15
call pp, 3

#L27:
return 

#L26:

#L18:
#L8:
#L4: