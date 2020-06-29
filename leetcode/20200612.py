# 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？
# 请你找出所有满足条件且不重复的三元组。
#
# 注意：答案中不可以包含重复的三元组。


class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        # a + b = -c

        nums_1 = nums[:]
        nums_2 = nums[:]

        for a in nums:
            code_1 = 0
            del nums_2[0]
            for b in nums_2:
                code_2 = 0



