def LCS(s1,s2,i1,i2):
	if i1 == len(s1) or i2 == len(s2):
		return ""
	if s1[i1] == s2[i2]:
		return s1[i1] + LCS(s1,s2,i1+1,i2+1)
	resultA = LCS(s1,s2,i1+1,i2)
	resultB = LCS(s1,s2,i1,i2+1)
	if len(resultA) > len(resultB):
		return resultA
	else:
		return resultB