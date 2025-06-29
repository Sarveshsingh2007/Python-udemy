student_scores = [105, 154, 150, 142, 120, 185, 171, 184, 149, 24, 59, 68, 199, 78, 65, 89, 86, 55, 91, 64, 89]

total_score = sum(student_scores)
# print(total_score)

sum = 0
for score in student_scores:
    sum += score

# print(sum)  

# print(max(student_scores)) # finds maximum value in the list

max_score = 0
for score in student_scores:
    if score > max_score:
        max_score = score

print(max_score)        