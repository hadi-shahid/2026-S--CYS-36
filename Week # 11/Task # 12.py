s1 = {1,2,3}
s2 = {1,4,5}
s3 = {1,6,7}
s = (set.union(s1,s2,s3))
s.remove(1)
print(s)
# Or
s1 = {1,2,3}
s2 = {1,4,5}
s3 = {1,6,7}
s = set.union(s1,s2,s3)
s1.intersection_update(s1,s2,s3)
print(s1)
s.remove(1)
print(s)