import operator

l1 = [1,2,3,4]
l2 = [5,6,7,8]

print(list(zip(l1, l2)))

l3 = [(1,2),(4,4),(5,2)]
l4=[(1,2)]
maximo1 = max(l3, key=operator.itemgetter(0))
maximo2 = max(l3, key=operator.itemgetter(1))
print(maximo1)
print(maximo2)

l3.remove((1,2))
l4.remove((1,2))
print(l3)
if l3:
    print("Hola")

if l4:
    print("Adios")