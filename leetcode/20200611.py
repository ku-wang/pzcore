class Solution(object):

    def dailyTemperatures(self, T):
        """
        :type T: List[int]
        :rtype: List[int]
        """

        new_t = T[:]
        output_t = []

        for t1 in T:
            raises = 0
            del new_t[0]
            if len(new_t) > 1:
                for t2 in new_t:
                    raises = raises + 1
                    if t1 < t2 and raises > 0:
                        break
                    if t1 == t2 and raises :
                        pass
            output_t.append(raises)

        print(output_t)

if __name__ == "__main__":

    Solution().dailyTemperatures([89,62,70,58,47,47,46,76,100,70])