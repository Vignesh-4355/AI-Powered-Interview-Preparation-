"""Management command to populate DSA coding questions - Clean version"""
from django.core.management.base import BaseCommand
from coding_practice.models import CodingQuestion


class Command(BaseCommand):
    help = 'Populate database with most asked DSA interview questions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating DSA questions...')

        questions = [
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.',
                'difficulty': 'Easy',
                'topic': 'Arrays',
                'sample_input': 'nums = [2,7,11,15], target = 9',
                'sample_output': '[0,1]',
                'explanation': 'Use a hash map to store the complement of each number. For each number, check if its complement (target - num) exists in the map. If yes, return the indices. Time: O(n), Space: O(n).',
                'youtube_link': 'https://www.youtube.com/watch?v=KLlXCFG5TnA',
                'constraints': '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9',
            },
            {
                'title': 'Reverse Linked List',
                'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
                'difficulty': 'Easy',
                'topic': 'Linked List',
                'sample_input': 'head = [1,2,3,4,5]',
                'sample_output': '[5,4,3,2,1]',
                'explanation': 'Use three pointers (prev, current, next). Traverse the list, reversing the direction of each node pointer. Return the new head. Time: O(n), Space: O(1).',
                'youtube_link': 'https://www.youtube.com/watch?v=G0_I-ZF0S38',
                'constraints': 'The number of nodes is in the range [0, 5000].',
            },
            {
                'title': 'Valid Parentheses',
                'description': 'Given a string containing just the characters (, ), {, }, [ and ], determine if the input string is valid. An input string is valid if open brackets must be closed by the same type and in the correct order.',
                'difficulty': 'Easy',
                'topic': 'Stack & Queue',
                'sample_input': 's = "()[]{}"',
                'sample_output': 'true',
                'explanation': 'Use a stack to track opening brackets. For each closing bracket, check if it matches the top of the stack. If the stack is empty at the end, the string is valid. Time: O(n), Space: O(n).',
                'youtube_link': 'https://www.youtube.com/watch?v=WTzjTft5MgM',
                'constraints': '1 <= s.length <= 10^4',
            },
            {
                'title': 'Maximum Subarray',
                'description': 'Given an integer array nums, find the contiguous subarray which has the largest sum, and return its sum.',
                'difficulty': 'Medium',
                'topic': 'Dynamic Programming',
                'sample_input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
                'sample_output': '6',
                'explanation': 'Kadanes Algorithm: Keep track of maximum sum ending at current position. If current sum becomes negative, reset it to zero. Track the maximum sum seen so far. Time: O(n), Space: O(1).',
                'youtube_link': 'https://www.youtube.com/watch?v=5WZl3MMT0Eg',
                'constraints': '1 <= nums.length <= 10^5',
            },
            {
                'title': 'Merge Intervals',
                'description': 'Given an array of intervals where intervals[i] = [start, end], merge all overlapping intervals, and return an array of the non-overlapping intervals.',
                'difficulty': 'Medium',
                'topic': 'Arrays',
                'sample_input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]',
                'sample_output': '[[1,6],[8,10],[15,18]]',
                'explanation': 'Sort intervals by start time. Iterate through intervals and merge overlapping ones. If current interval overlaps with previous, merge them by updating end time. Time: O(n log n), Space: O(n).',
                'youtube_link': 'https://www.youtube.com/watch?v=44H3cEC2fFM',
                'constraints': '1 <= intervals.length <= 10^4',
            },
            {
                'title': 'Trapping Rain Water',
                'description': 'Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.',
                'difficulty': 'Hard',
                'topic': 'Arrays',
                'sample_input': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]',
                'sample_output': '6',
                'explanation': 'Two pointer approach: Maintain leftMax and rightMax while moving pointers from both ends. Water at any position = min(leftMax, rightMax) - height[i]. Move the pointer with smaller max. Time: O(n), Space: O(1).',
                'youtube_link': 'https://www.youtube.com/watch?v=ZI2z5pq0TqA',
                'constraints': 'n == height.length\n1 <= n <= 2 * 10^4',
            },
            {
                'title': 'Longest Substring Without Repeating Characters',
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'difficulty': 'Medium',
                'topic': 'Strings',
                'sample_input': 's = "abcabcbb"',
                'sample_output': '3',
                'explanation': 'Sliding Window: Use a set to track characters in current window. Expand window by moving right pointer. If character already in set, shrink from left. Track maximum window size. Time: O(n), Space: O(min(n,m)).',
                'youtube_link': 'https://www.youtube.com/watch?v=wiGpQwVHdE0',
                'constraints': '0 <= s.length <= 5 * 10^4',
            },
            {
                'title': '3Sum',
                'description': 'Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.',
                'difficulty': 'Medium',
                'topic': 'Arrays',
                'sample_input': 'nums = [-1,0,1,2,-1,-4]',
                'sample_output': '[[-1,-1,2],[-1,0,1]]',
                'explanation': 'Sorting + Two Pointers: Sort the array. Fix first element, use two pointers for remaining. Skip duplicates. If sum < 0, move left; if sum > 0, move right. If sum == 0, add triplet. Time: O(n^2).',
                'youtube_link': 'https://www.youtube.com/watch?v=jzZsG8n2R9A',
                'constraints': '3 <= nums.length <= 3000',
            },
            {
                'title': 'Container With Most Water',
                'description': 'You are given an integer array height of length n. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water.',
                'difficulty': 'Medium',
                'topic': 'Arrays',
                'sample_input': 'height = [1,8,6,2,5,4,8,3,7]',
                'sample_output': '49',
                'explanation': 'Two Pointers: Start with pointers at both ends. Calculate area = min(height[left], height[right]) * (right - left). Move the pointer with smaller height inward. Track maximum area. Time: O(n).',
                'youtube_link': 'https://www.youtube.com/watch?v=UuiTKBwPgAo',
                'constraints': 'n == height.length\n2 <= n <= 10^5',
            },
            {
                'title': 'Best Time to Buy and Sell Stock',
                'description': 'You are given an array prices where prices[i] is the price of a given stock on the ith day. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.',
                'difficulty': 'Easy',
                'topic': 'Arrays',
                'sample_input': 'prices = [7,1,5,3,6,4]',
                'sample_output': '5',
                'explanation': 'One Pass: Track the minimum price seen so far. For each day, calculate potential profit (current_price - min_price). Track maximum profit. Update minimum price if current price is lower. Time: O(n), Space: O(1).',
                'youtube_link': 'https://www.youtube.com/watch?v=1pkOgXD63Eg',
                'constraints': '1 <= prices.length <= 10^5',
            },
            {
                'title': 'Number of Islands',
                'description': 'Given an m x n 2D binary grid which represents a map of 1s (land) and 0s (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.',
                'difficulty': 'Medium',
                'topic': 'Graphs',
                'sample_input': 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]',
                'sample_output': '3',
                'explanation': 'DFS: Iterate through each cell. When land is found, increment island count and perform DFS to mark all connected land as visited. Mark visited cells as 0 to avoid counting again. Time: O(m*n), Space: O(m*n).',
                'youtube_link': 'https://www.youtube.com/watch?v=pV2kpPD66nE',
                'constraints': 'm == grid.length\nn == grid[i].length',
            },
            {
                'title': 'Validate Binary Search Tree',
                'description': 'Given the root of a binary tree, determine if it is a valid binary search tree. A valid BST: left subtree contains only nodes with keys less than the node key, right subtree contains only nodes with keys greater.',
                'difficulty': 'Medium',
                'topic': 'Trees',
                'sample_input': 'root = [2,1,3]',
                'sample_output': 'true',
                'explanation': 'DFS with Bounds: Use helper function with min and max bounds. For root: bounds are (-inf, +inf). For left child: update max to current value. For right child: update min to current value. Check if current value is within bounds. Time: O(n).',
                'youtube_link': 'https://www.youtube.com/watch?v=Q6LcKZOtwEI',
                'constraints': 'The number of nodes is in the range [1, 10^4].',
            },
            {
                'title': 'Coin Change',
                'description': 'You are given an integer array coins representing coins of different denominations and an integer amount. Return the fewest number of coins that you need to make up that amount. If impossible, return -1.',
                'difficulty': 'Medium',
                'topic': 'Dynamic Programming',
                'sample_input': 'coins = [1,2,5], amount = 11',
                'sample_output': '3',
                'explanation': 'Bottom-up DP: Create dp array of size amount+1, initialize with infinity. dp[0] = 0. For each coin, update dp array: dp[i] = min(dp[i], dp[i-coin] + 1). Return dp[amount] or -1. Time: O(amount*n), Space: O(amount).',
                'youtube_link': 'https://www.youtube.com/watch?v=H9bfqozjoqs',
                'constraints': '1 <= coins.length <= 12\n0 <= amount <= 10^4',
            },
        ]

        created_count = 0
        for q_data in questions:
            question, created = CodingQuestion.objects.get_or_create(
                title=q_data['title'],
                defaults=q_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {question.title} ({question.difficulty})'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {question.title}'))

        total = CodingQuestion.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nCreated {created_count} new questions'))
        self.stdout.write(self.style.SUCCESS(f'Total questions: {total}'))
