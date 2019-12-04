from typing import List


def has_decreasing(input: List[int], maxV: int = 0) -> bool:
    if len(input) == 0:
        return False
    else:
        head, *tail = input
        if int(head) < maxV:
            return True
        else:
            return has_decreasing(tail, max(maxV, int(head)))


def has_double(input: List[int]) -> bool:
    if len(input) == 1:
        return False
    else:
        head1, head2, *tail = input
        if head1 == head2:
            return True
        else:
            return has_double([head2]+tail)


def has_double_but_not_larger(input: List[int], count: int = 0) -> bool:
    if len(input) == 1 and count == 1:
        return True
    elif len(input) == 1:
        return False
    else:
        head1, head2, *tail = input
        if not head1 == head2 and count == 1:
            return True
        elif head1 == head2:
            return has_double_but_not_larger([head2]+tail,count+1)
        else:
            return has_double_but_not_larger([head2]+tail)


def is_password(input: List[int]) -> bool:
    return has_double(input) and not has_decreasing(input) and has_double_but_not_larger(input)


testcase = "112233"
print(has_double_but_not_larger(list(testcase)))
print(is_password(list(testcase)))

start = 231832
end = 767346

count = 0
for pw in range(start, end):
    if is_password(list(str(pw))):
        count += 1
print(count)