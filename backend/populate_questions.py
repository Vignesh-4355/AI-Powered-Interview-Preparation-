import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interview_portal.settings')
django.setup()

from coding_practice.models import CodingQuestion

questions_data = [
    {
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.',
        'difficulty': 'Easy',
        'topic': 'Arrays',
        'sample_input': 'nums = [2,7,11,15], target = 9',
        'sample_output': '[0,1]',
        'explanation': 'Use a hash map to store the complement of each number. For each number, check if its complement (target - num) exists in the map. If yes, return the indices. Time complexity: O(n), Space complexity: O(n).',
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
        'explanation': 'Iterative approach: Use three pointers (prev, current, next). Traverse the list, reversing the direction of each nodes pointer. Return the new head. Time complexity: O(n), Space complexity: O(1).',
        'youtube_link': 'https://www.youtube.com/watch?v=G0_I-ZF0S38',
        'constraints': 'The number of nodes in the list is the range [0, 5000].',
    },
    {
        'title': 'Valid Parentheses',
        'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid. An input string is valid if: open brackets must be closed by the same type of brackets, open brackets must be closed in the correct order.',
        'difficulty': 'Easy',
        'topic': 'Stack & Queue',
        'sample_input': 's = "()[]{}"',
        'sample_output': 'true',
        'explanation': 'Use a stack to track opening brackets. For each closing bracket, check if it matches the top of the stack. If the stack is empty at the end, the string is valid. Time complexity: O(n), Space complexity: O(n).',
        'youtube_link': 'https://www.youtube.com/watch?v=WTzjTft5MgM',
        'constraints': '1 <= s.length <= 10^4',
    },
    {
        'title': 'Maximum Subarray',
        'description': 'Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum, and return its sum.',
        'difficulty': 'Medium',
        'topic': 'Dynamic Programming',
        'sample_input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
        'sample_output': '6',
        'explanation': 'Kadanes Algorithm: Keep track of maximum sum ending at current position. If current sum becomes negative, reset it to zero. Track the maximum sum seen so far. Time complexity: O(n), Space complexity: O(1).',
        'youtube_link': 'https://www.youtube.com/watch?v=5WZl3MMT0Eg',
        'constraints': '1 <= nums.length <= 10^5',
    },
    {
        'title': 'Merge Intervals',
        'description': 'Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.',
        'difficulty': 'Medium',
        'topic': 'Arrays',
        'sample_input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]',
        'sample_output': '[[1,6],[8,10],[15,18]]',
        'explanation': 'Sort intervals by start time. Iterate through intervals and merge overlapping ones. If current interval overlaps with previous, merge them by updating end time. Time complexity: O(n log n), Space complexity: O(n).',
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
        'explanation': 'Two pointer approach: Maintain leftMax and rightMax while moving pointers from both ends. Water at any position = min(leftMax, rightMax) - height[i]. Move the pointer with smaller max. Time complexity: O(n), Space complexity: O(1).',
        'youtube_link': 'https://www.youtube.com/watch?v=ZI2z5pq0TqA',
        'constraints': '1 <= n <= 2 * 10^4',
    },
]

print('Populating coding questions...')
for q_data in questions_data:
   question, created = CodingQuestion.objects.get_or_create(
       title=q_data['title'],
       defaults=q_data
    )
    if created:
        print(f'✓ Created: {question.title}')
   else:
        print(f'Already exists: {question.title}')

print(f'\nTotal questions: {CodingQuestion.objects.count()}')
print('Successfully populated coding questions!')
