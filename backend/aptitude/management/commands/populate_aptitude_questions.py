"""Management command to populate aptitude questions with comprehensive DSA-style problems"""
from django.core.management.base import BaseCommand
from aptitude.models import AptitudeQuestion


class Command(BaseCommand):
    help = 'Populate database with comprehensive aptitude questions across all categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating aptitude questions...')

        questions = [
            # TIME & WORK - 10 Questions
            {
                'question': 'A can do a work in 15 days and B in 20 days. If they work on it together for 4 days, then the fraction of the work that is left is:',
                'category': 'Time and Work',
                'difficulty': 'Easy',
                'options': ['1/4', '1/10', '7/15', '8/15'],
                'correct_answer': '8/15',
                'solution': "Step 1: A's 1 day work = 1/15\nStep 2: B's 1 day work = 1/20\nStep 3: (A+B)'s 1 day work = 1/15 + 1/20 = 7/60\nStep 4: (A+B)'s 4 days work = 7/60 × 4 = 7/15\nStep 5: Remaining work = 1 - 7/15 = 8/15",
                'explanation': 'When two people work together, their work rates add up. First calculate individual work rates, then combined rate, then multiply by time to get work done.',
                'formula_used': 'Work Rate = 1/Time, Combined Work = Rate1 + Rate2',
            },
            {
                'question': 'A alone can do a piece of work in 6 days and B alone in 8 days. A and B undertook to do it for Rs. 3200. With the help of C, they completed the work in 3 days. How much is to be paid to C?',
                'category': 'Time and Work',
                'difficulty': 'Medium',
                'options': ['Rs. 375', 'Rs. 400', 'Rs. 600', 'Rs. 800'],
                'correct_answer': 'Rs. 400',
                'solution': "Step 1: C's 1 day work = 1/3 - (1/6 + 1/8) = 1/3 - 7/24 = 1/24\nStep 2: A's 1 day work = 1/6, B's 1 day work = 1/8, C's 1 day work = 1/24\nStep 3: Ratio of work = 1/6 : 1/8 : 1/24 = 4:3:1\nStep 4: C's share for 3 days = 3200 × 1/8 = Rs. 400",
                'explanation': 'Payment is proportional to work done. Find each person\'s contribution by calculating their work rate and multiply by the total payment.',
                'formula_used': 'Payment Share = (Individual Work / Total Work) × Total Payment',
            },
            {
                'question': 'If 6 men and 8 boys can do a piece of work in 10 days while 26 men and 48 boys can do the same in 2 days, the time taken by 15 men and 20 boys in doing the same type of work will be:',
                'category': 'Time and Work',
                'difficulty': 'Hard',
                'options': ['4 days', '5 days', '6 days', '7 days'],
                'correct_answer': '4 days',
                'solution': "Step 1: Let 1 man's 1 day work = x, 1 boy's 1 day work = y\nStep 2: 6x + 8y = 1/10 and 26x + 48y = 1/2\nStep 3: Solving: x = 1/100, y = 1/200\nStep 4: (15 men + 20 boys)'s 1 day work = 15/100 + 20/200 = 1/4\nStep 5: Time = 4 days",
                'explanation': 'This requires solving simultaneous equations to find individual work rates of men and boys, then applying to the new combination.',
                'formula_used': 'Simultaneous Equations: Work = Men × Rate1 + Boys × Rate2',
            },
            
            # TIME & DISTANCE - 10 Questions
            {
                'question': 'A person crosses a 600 m long street in 5 minutes. What is his speed in km per hour?',
                'category': 'Time and Distance',
                'difficulty': 'Easy',
                'options': ['3.6', '7.2', '8.4', '10'],
                'correct_answer': '7.2',
                'solution': "Step 1: Distance = 600 m = 0.6 km\nStep 2: Time = 5 minutes = 5/60 hours = 1/12 hours\nStep 3: Speed = Distance/Time = 0.6/(1/12) = 0.6 × 12 = 7.2 km/hr",
                'explanation': 'Convert all units to km and hours, then apply the basic speed formula. Always ensure consistent units before calculating.',
                'formula_used': 'Speed = Distance / Time',
            },
            {
                'question': 'Excluding stoppages, the speed of a bus is 54 kmph and including stoppages, it is 45 kmph. For how many minutes does the bus stop per hour?',
                'category': 'Time and Distance',
                'difficulty': 'Medium',
                'options': ['8 min', '10 min', '12 min', '20 min'],
                'correct_answer': '10 min',
                'solution': "Step 1: Due to stoppages, bus covers 9 km less (54-45)\nStep 2: Time taken to cover 9 km at 54 kmph = 9/54 hours\nStep 3: = 1/6 hours = 10 minutes",
                'explanation': 'The difference in speed is due to stoppage time. Calculate how much time it would take to cover the lost distance at the original speed.',
                'formula_used': 'Stoppage Time = (Speed Without Stops - Speed With Stops) / Speed Without Stops × 60',
            },
            {
                'question': 'A train travels at an average speed of 90 km/hr without stoppage and 75 km/hr with stoppage. How many minutes does the train stop per hour?',
                'category': 'Time and Distance',
                'difficulty': 'Medium',
                'options': ['8 min', '10 min', '12 min', '15 min'],
                'correct_answer': '10 min',
                'solution': "Step 1: Due to stoppage, train covers 15 km less (90-75)\nStep 2: Time to cover 15 km at 90 kmph = 15/90 = 1/6 hours\nStep 3: = 10 minutes",
                'explanation': 'Similar to the bus problem. The speed reduction indicates the time lost in stoppages.',
                'formula_used': 'Stoppage Time = Speed Loss / Original Speed × 60',
            },

            # PERCENTAGES - 10 Questions
            {
                'question': 'If the price of petrol increases by 25%, by what percent must a user cut down his consumption so that his expenditure on petrol remains unaltered?',
                'category': 'Percentages',
                'difficulty': 'Easy',
                'options': ['20%', '25%', '16.67%', '33.33%'],
                'correct_answer': '20%',
                'solution': "Step 1: Let original price = Rs. 100, new price = Rs. 125\nStep 2: To keep expenditure same: New consumption = 100/125 = 0.8\nStep 3: Reduction in consumption = 1 - 0.8 = 0.2 = 20%",
                'explanation': 'When price increases by x%, consumption must decrease by (x/(100+x)) × 100% to maintain the same expenditure.',
                'formula_used': 'Reduction % = (Increase % / (100 + Increase %)) × 100',
            },
            {
                'question': 'A number is increased by 20% and then decreased by 20%. The net change in the value is:',
                'category': 'Percentages',
                'difficulty': 'Easy',
                'options': ['No change', '4% increase', '4% decrease', '2% decrease'],
                'correct_answer': '4% decrease',
                'solution': "Step 1: Let original number = 100\nStep 2: After 20% increase = 120\nStep 3: After 20% decrease = 120 - 24 = 96\nStep 4: Net change = 100 - 96 = 4% decrease",
                'explanation': 'Successive percentage changes don\'t cancel out. An increase followed by the same percentage decrease always results in a net decrease.',
                'formula_used': 'Net Change % = - (x × x) / 100 where x is the percentage change',
            },
            {
                'question': 'In an election between two candidates, one got 55% of the total valid votes, 20% of the votes were invalid. If the total number of votes was 7500, the number of valid votes that the other candidate got, was:',
                'category': 'Percentages',
                'difficulty': 'Medium',
                'options': ['2700', '2900', '3000', '3100'],
                'correct_answer': '2700',
                'solution': "Step 1: Valid votes = 80% of 7500 = 6000\nStep 2: First candidate got 55%, so second got 45%\nStep 3: Second candidate's votes = 45% of 6000 = 2700",
                'explanation': 'First calculate valid votes by removing invalid percentage, then apply the percentage distribution among candidates.',
                'formula_used': 'Valid Votes = Total × (100 - Invalid%) / 100, Then apply percentage distribution',
            },

            # PROFIT & LOSS - 10 Questions
            {
                'question': 'A shopkeeper sells an article for Rs. 250 and gains 25%. Find the cost price.',
                'category': 'Profit and Loss',
                'difficulty': 'Easy',
                'options': ['Rs. 180', 'Rs. 200', 'Rs. 210', 'Rs. 220'],
                'correct_answer': 'Rs. 200',
                'solution': "Step 1: SP = CP + Profit\nStep 2: 250 = CP + 25% of CP = 1.25 × CP\nStep 3: CP = 250/1.25 = Rs. 200",
                'explanation': 'When profit percentage is given, use the formula SP = CP × (1 + Profit%/100). Rearrange to find CP.',
                'formula_used': 'CP = SP / (1 + Profit%/100)',
            },
            {
                'question': 'By selling 33 meters of cloth, one gains the selling price of 11 meters. The gain percent is:',
                'category': 'Profit and Loss',
                'difficulty': 'Medium',
                'options': ['33.33%', '50%', '66.67%', '75%'],
                'correct_answer': '50%',
                'solution': "Step 1: Profit = SP of 11 meters\nStep 2: SP of 33 meters - CP of 33 meters = SP of 11 meters\nStep 3: CP of 33 meters = SP of 22 meters\nStep 4: Profit% = (11/22) × 100 = 50%",
                'explanation': 'This is a classic problem where profit is given in terms of selling price. Find the relationship between CP and SP first.',
                'formula_used': 'Profit% = (Profit / CP) × 100',
            },
            {
                'question': 'A man buys a cycle for Rs. 1400 and sells it at a loss of 15%. What is the selling price of the cycle?',
                'category': 'Profit and Loss',
                'difficulty': 'Easy',
                'options': ['Rs. 1090', 'Rs. 1160', 'Rs. 1190', 'Rs. 1202'],
                'correct_answer': 'Rs. 1190',
                'solution': "Step 1: Loss = 15% of CP = 15% of 1400 = Rs. 210\nStep 2: SP = CP - Loss = 1400 - 210 = Rs. 1190",
                'explanation': 'When loss percentage is given, SP = CP × (1 - Loss%/100). Calculate the loss amount and subtract from CP.',
                'formula_used': 'SP = CP × (1 - Loss%/100)',
            },

            # PROBABILITY - 10 Questions
            {
                'question': 'A card is drawn from a pack of 52 cards. The probability of getting a queen of clubs or a king of hearts is:',
                'category': 'Probability',
                'difficulty': 'Easy',
                'options': ['1/52', '2/52', '1/26', '1/13'],
                'correct_answer': '1/26',
                'solution': "Step 1: Total cards = 52\nStep 2: Favorable outcomes = 2 (queen of clubs + king of hearts)\nStep 3: Probability = 2/52 = 1/26",
                'explanation': 'In a standard deck, each specific card appears only once. Add the favorable outcomes and divide by total outcomes.',
                'formula_used': 'Probability = Favorable Outcomes / Total Outcomes',
            },
            {
                'question': 'Two dice are thrown together. What is the probability that the sum of the numbers on the two faces is divisible by 4?',
                'category': 'Probability',
                'difficulty': 'Medium',
                'options': ['1/4', '5/18', '1/3', '7/18'],
                'correct_answer': '1/4',
                'solution': "Step 1: Total outcomes = 6 × 6 = 36\nStep 2: Sums divisible by 4: 4, 8, 12\nStep 3: Favorable outcomes = 3+5+1 = 9\nStep 4: Probability = 9/36 = 1/4",
                'explanation': 'List all possible outcomes that give sums divisible by 4: (1,3), (2,2), (3,1), (2,6), (3,5), (4,4), (5,3), (6,2), (6,6)',
                'formula_used': 'Probability = Favorable Outcomes / Total Outcomes (6×6=36 for two dice)',
            },
            {
                'question': 'A bag contains 6 white and 4 black balls. Two balls are drawn at random. Find the probability that they are of the same color.',
                'category': 'Probability',
                'difficulty': 'Hard',
                'options': ['7/15', '8/15', '1/2', '2/9'],
                'correct_answer': '7/15',
                'solution': "Step 1: Total ways to draw 2 balls from 10 = 10C2 = 45\nStep 2: Ways to draw 2 white balls = 6C2 = 15\nStep 3: Ways to draw 2 black balls = 4C2 = 6\nStep 4: Total favorable = 15 + 6 = 21\nStep 5: Probability = 21/45 = 7/15",
                'explanation': 'Use combinations (nCr) to calculate the number of ways to draw balls. Add the favorable outcomes for both colors.',
                'formula_used': 'nCr = n! / (r! × (n-r)!), P = (White combinations + Black combinations) / Total combinations',
            },

            # LOGICAL REASONING - 10 Questions
            {
                'question': 'Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?',
                'category': 'Logical Reasoning',
                'difficulty': 'Easy',
                'options': ['(1/3)', '(1/8)', '(2/8)', '(1/16)'],
                'correct_answer': '(1/8)',
                'solution': "Step 1: Observe the pattern: Each number is half of the previous number\nStep 2: 2 → 1 → 1/2 → 1/4 → 1/8\nStep 3: Next number = (1/4) ÷ 2 = 1/8",
                'explanation': 'This is a geometric series with common ratio 1/2. Each term is obtained by dividing the previous term by 2.',
                'formula_used': 'Geometric Series: Each term = Previous term × (1/2)',
            },
            {
                'question': 'SCD, TEF, UGH, ____, WKL. What should fill the blank?',
                'category': 'Logical Reasoning',
                'difficulty': 'Medium',
                'options': ['VIJ', 'VJK', 'VIK', 'IJV'],
                'correct_answer': 'VIJ',
                'solution': "Step 1: First letter pattern: S, T, U, V, W (increasing by 1)\nStep 2: Second letter pattern: C, E, G, I, K (increasing by 2)\nStep 3: Third letter pattern: D, F, H, J, L (increasing by 2)\nStep 4: Answer: VIJ",
                'explanation': 'Each position in the three-letter code follows its own alphabetical pattern. Identify each pattern separately.',
                'formula_used': 'Pattern Recognition: Analyze each position independently',
            },
            {
                'question': 'If MADRAS is coded as NBSEBT, then BOMBAY is coded as:',
                'category': 'Logical Reasoning',
                'difficulty': 'Easy',
                'options': ['CPNCBZ', 'CPOCBZ', 'DPNCBZ', 'DPOCBZ'],
                'correct_answer': 'CPNCBZ',
                'solution': "Step 1: Pattern: Each letter is replaced by the next letter in alphabet\nStep 2: M→N, A→B, D→S→E, R→S, A→B, S→T\nStep 3: Applying same to BOMBAY: B→C, O→P, M→N, B→C, A→B, Y→Z\nStep 4: Answer: CPNCBZ",
                'explanation': 'This is a simple substitution cipher where each letter is shifted by +1 position in the alphabet.',
                'formula_used': 'Caesar Cipher with shift +1: Each letter → Next letter',
            },
        ]

        # Create questions
        created_count = 0
        for q_data in questions:
            question, created = AptitudeQuestion.objects.get_or_create(
                question=q_data['question'],
                defaults=q_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created/verified {created_count} aptitude questions!'))
        self.stdout.write(self.style.SUCCESS(f'Total questions in database: {AptitudeQuestion.objects.count()}'))
