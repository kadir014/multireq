These are the results I measured on my computer:

```
1 request                   4 requests (group of 5)
------------------------    --------------------------
max: 1109ms                 max: 1264ms
avg: 841ms (50 iters)       avg: 909ms (50 iters)
min: 711ms                  min: 705ms
opt: 0%                     opt: 68.8%

5 requests (group of 5)     10 requests (group of 5)
------------------------    --------------------------
max: 1114ms                 max: 1147ms
avg: 1011ms (50 iters)      avg: 996ms (50 iters)
min: 697ms                  min: 813ms
opt: 68.7%                  opt: 84.2%

15 requests (group of 5)    30 requests (group of 10)
-------------------------   --------------------------
max: 1347ms                 max: 3175ms
avg: 1045ms (50 iters)      avg: 1322 (50 iters)
min: 868ms                  min: 1067ms
opt: 88.9%                  opt: %92.3

50 requests (group of 12)   100 requests (group of 15)
-------------------------   --------------------------
max: 2347ms                 max: 3453ms
avg: 1709ms (50 iters)      avg: 3136ms (50 iter)
min: 1506ms                 min: 2724ms
opt: 94.8%                  opt: 94.6%
```
